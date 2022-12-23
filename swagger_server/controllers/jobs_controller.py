import datetime
import json
import os.path
import sys
import traceback

import peewee
import asyncio
import concurrent.futures as cf
from flask import Response
from swagger_server.controllers.extract_controller import do_izlusci
from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server.requets_db.models.vrsta import (Job)
from threading import Thread
from swagger_server.utils import cl_utils, db_utils
from swagger_server.utils import txt_utils
from werkzeug.datastructures import FileStorage
import threading
import time

CLASSLA_SMALL_SIZE_LIMIT = 500 * 1e3  # 500 KB, aka.: 500 * 10^3

DOC2TEXT_SMALL_SIZE_LIMIT = 10 * 1e6  # 10 MB

ATEAPI_SMALL_SIZE_LIMIT = 2 * 1e6  # 2 MB

########################################
CLASSLA_CONCURANCE_LIMIT_BIG = 2
CLASSLA_CONCURANCE_LIMIT_SMALL = 2

DOC2TEXT_CONCURANCE_LIMIT_BIG = 2
DOC2TEXT_CONCURANCE_LIMIT_SMALL = 2

ATEAPI_CONCURANCE_LIMIT_BIG = 2
ATEAPI_CONCURANCE_LIMIT_SMALL = 2

IZLUSCI_PO_ISKANJU_CONCURANCE_LIMIT = 4
########################################
classla_sem_big = threading.Semaphore(CLASSLA_CONCURANCE_LIMIT_BIG)
classla_sem_small = threading.Semaphore(CLASSLA_CONCURANCE_LIMIT_SMALL)

doc2text_sem_big = threading.Semaphore(DOC2TEXT_CONCURANCE_LIMIT_BIG)
doc2text_sem_small = threading.Semaphore(DOC2TEXT_CONCURANCE_LIMIT_SMALL)

ateapi_sem_big = threading.Semaphore(ATEAPI_CONCURANCE_LIMIT_BIG)
ateapi_sem_small = threading.Semaphore(ATEAPI_CONCURANCE_LIMIT_SMALL)

izluscipoiskanju_sem = threading.Semaphore(IZLUSCI_PO_ISKANJU_CONCURANCE_LIMIT)

running_threads = {}  # dictionary that saves currently running jobs


# from: https://blog.finxter.com/how-to-kill-a-thread-in-python/
class KThread(threading.Thread):
    """A subclass of threading.Thread, with a kill()
  method."""

    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
    trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            # print(f"Killing {self.ident}")
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def delete_job(job_id):  # noqa: E501
    """Izbriše job

     # noqa: E501

    :param job_id:
    :type job_id: int

    :rtype: str
    """
    try:
        job = Job.get_by_id(job_id)
        if job.job_type == 0:
            return Response(f"Job with the ID {job_id} was already removed", 404)

        if job.started_on is not None and job.finished_on is None:
            # return Response("Cancelling ongoing jobs currently not implemented.", 400)
            if job.job_type == 5:
                return Response("Cancelling ongoing izlusciPoIskanjuAsync jobs currently not possible.", 400)

            if job.id in running_threads:
                try:
                    running_threads[job.id].kill()
                except:
                    return Response(f"Something went wrong when trying to delete ongoing job with ID {job.id}", 400)
                finally:
                    try:
                        del running_threads[job.id]
                    except:
                        pass
        job.job_type = 0

        ###############
        # dokler je strežnik v developmentu, naj to ostane, za debugging namene
        # če je kakšen problem z gdprjem ali kaj takega, potem naj se spodnji dve vrstici odkomentirata
        # in tudi se izbriše input in output jobov, ki imajo tip 0 (izbrisano)

        # job.job_input = ""
        # job.job_output = "This job was deleted."

        job.save()
        # job.delete_instance()
        return f"Job with the ID {job_id} was removed"
    except peewee.DoesNotExist:
        return Response("Job with this ID does not exist", 404)


def get_job_status(job_id):  # noqa: E501
    """Vrne status

     # noqa: E501

    :param job_id:
    :type job_id: int

    :rtype: JobResponse
    """
    try:
        job = Job.get_by_id(job_id)
        if job.job_type == 0:
            return "Job with this ID has been deleted.", 410
        if job.started_on is None:
            return JobResponse(job_status="waiting in que", created_on=job.created_on), 200
        if job.started_on is not None and job.finished_on is None:
            return JobResponse(job_status="currently processing", created_on=job.created_on,
                               started_on=job.started_on), 200
        if job.started_on is not None and job.finished_on is not None and not job.job_output.startswith("ERROR -"):
            res = job.job_output
            if job.job_type in [4, 5]:
                try:
                    res = json.loads(job.job_output)
                except:
                    pass
            return JobResponse(job_status="finished processing (OK)", created_on=job.created_on,
                               started_on=job.started_on,
                               finished_on=job.finished_on, job_result=res), 200
        if job.started_on is not None and job.finished_on is not None and job.job_output.startswith("ERROR -"):
            return JobResponse(job_status="finished processing (ERROR)", created_on=job.created_on,
                               started_on=job.started_on,
                               finished_on=job.finished_on, job_result=job.job_output), 200
    except peewee.DoesNotExist:
        return "Job with this ID does not exist", 404


def clear_up_unfinished_jobs():
    """
    In case server crashed while jobs were in queue...
    """
    Job.update(started_on=None).where(Job.started_on.is_null(False), Job.finished_on.is_null()).execute()
    if os.path.exists('tmp'):
        for tmp_file in os.listdir('tmp'):
            if not Job.select().where(Job.input_file == tmp_file).exists():
                os.remove(f'tmp/{tmp_file}')


async def try_do_jobs():
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        ex.submit(try_do_jobs_classla)
        ex.submit(try_do_jobs_doc2text)
        ex.submit(try_do_jobs_ateapi)
        ex.submit(try_do_jobs_izluscipoiskanju)


### Picking jobs for looping
def try_do_jobs_izluscipoiskanju():
    while True:
        try:
            unfinished_jobs = []
            if izluscipoiskanju_sem._value > 0:
                unfinished_jobs = Job.select() \
                    .where(Job.finished_on.is_null(), Job.started_on.is_null(), Job.job_type == 5) \
                    .limit(izluscipoiskanju_sem._value)

                ts = [KThread(target=execute_izluscipoiskanju_job, args=(job, izluscipoiskanju_sem,)) for job in
                      unfinished_jobs]
                for t in ts:
                    running_threads[t._args[0].id] = t
                    t.start()
                # with cf.ThreadPoolExecutor(max_workers=IZLUSCI_PO_ISKANJU_CONCURANCE_LIMIT) as ex:
                #    [ex.submit(execute_izluscipoiskanju_job, job, izluscipoiskanju_sem) for job in unfinished_jobs]
        except Exception as e:
            print(f"Exception in try_do_jobs_izluscipoiskanju\n{traceback.format_exc()}")
        finally:
            time.sleep(3)


### Picking jobs for looping
def try_do_jobs_ateapi():
    while True:
        try:
            unfinished_jobs_big = []
            unfinished_jobs_small = []
            if ateapi_sem_big._value > 0:
                unfinished_jobs_big.extend(Job.select().where(Job.finished_on.is_null(), Job.started_on.is_null(),
                                                              Job.job_type == 4,
                                                              Job.input_size > ATEAPI_SMALL_SIZE_LIMIT) \
                                           .limit(ateapi_sem_big._value))
            if ateapi_sem_small._value > 0:
                unfinished_jobs_small.extend(Job.select().where(Job.finished_on.is_null(), Job.started_on.is_null(),
                                                                Job.job_type == 4,
                                                                Job.input_size <= ATEAPI_SMALL_SIZE_LIMIT) \
                                             .limit(ateapi_sem_small._value))

            ts_s = [KThread(target=execute_ateapi_job, args=(job, ateapi_sem_small,)) for job in
                    unfinished_jobs_small]
            ts_b = [KThread(target=execute_ateapi_job, args=(job, ateapi_sem_big,)) for job in
                    unfinished_jobs_big]
            ts = ts_s + ts_b
            for t in ts:
                running_threads[t._args[0].id] = t
                t.start()

            # if len(unfinished_jobs_big) > 0:
            #     with cf.ThreadPoolExecutor(max_workers=ATEAPI_CONCURANCE_LIMIT_BIG) as ex:
            #         [ex.submit(execute_ateapi_job, job, ateapi_sem_big) for job in unfinished_jobs_big]
            # if len(unfinished_jobs_small) > 0:
            #     with cf.ThreadPoolExecutor(max_workers=ATEAPI_CONCURANCE_LIMIT_SMALL) as ex:
            #         [ex.submit(execute_ateapi_job, job, ateapi_sem_small) for job in unfinished_jobs_small]
        except Exception as e:
            print(f"Exception in try_do_jobs_ateapi\n{traceback.format_exc()}")
        finally:
            time.sleep(3)


### Picking jobs for looping
def try_do_jobs_classla():
    time.sleep(15)  # wait for tokenizers to load for classla ...
    while True:
        try:
            if not cl_utils.nlp_loaded:
                raise Exception("NLP utils not loaded yet.")

            unfinished_jobs_big = []
            unfinished_jobs_small = []

            if classla_sem_big._value > 0:
                unfinished_jobs_txt = Job.select() \
                    .where(Job.finished_on.is_null(), Job.job_type == 2,
                           Job.input_file.is_null(False), Job.input_size > CLASSLA_SMALL_SIZE_LIMIT) \
                    .limit(classla_sem_big._value)

                unfinished_jobs_no_txt = Job.select() \
                    .where(Job.finished_on.is_null(), Job.started_on.is_null(), Job.job_type == 2,
                           Job.input_file.is_null(), Job.input_size > CLASSLA_SMALL_SIZE_LIMIT) \
                    .limit(classla_sem_big._value)

                unfinished_jobs_big = [j for j in unfinished_jobs_txt] + [j for j in unfinished_jobs_no_txt]
                unfinished_jobs_big = unfinished_jobs_big[:classla_sem_big._value]

            if classla_sem_small._value > 0:
                unfinished_jobs_txt = Job.select() \
                    .where(Job.finished_on.is_null(), Job.job_type == 2,
                           Job.input_file.is_null(False), Job.input_size <= CLASSLA_SMALL_SIZE_LIMIT) \
                    .limit(classla_sem_small._value)

                unfinished_jobs_no_txt = Job.select() \
                    .where(Job.finished_on.is_null(), Job.started_on.is_null(), Job.job_type == 2,
                           Job.input_file.is_null(), Job.input_size <= CLASSLA_SMALL_SIZE_LIMIT) \
                    .limit(classla_sem_small._value)

                unfinished_jobs_small = [j for j in unfinished_jobs_txt] + [j for j in unfinished_jobs_no_txt]
                unfinished_jobs_small = unfinished_jobs_small[:classla_sem_small._value]

            ts_s = [KThread(target=execute_classla_job, args=(job, classla_sem_small,)) for job in
                    unfinished_jobs_small]
            ts_b = [KThread(target=execute_classla_job, args=(job, classla_sem_big,)) for job in
                    unfinished_jobs_big]
            ts = ts_s + ts_b
            for t in ts:
                running_threads[t._args[0].id] = t
                t.start()

            # if len(unfinished_jobs_big) > 0:
            #     with cf.ThreadPoolExecutor(max_workers=CLASSLA_CONCURANCE_LIMIT_BIG) as ex:
            #         [ex.submit(execute_classla_job, job, classla_sem_small) for job in unfinished_jobs_big]
            # if len(unfinished_jobs_small) > 0:
            #     with cf.ThreadPoolExecutor(max_workers=CLASSLA_CONCURANCE_LIMIT_SMALL) as ex:
            #         [ex.submit(execute_classla_job, job, classla_sem_small) for job in unfinished_jobs_small]

        except Exception as e:
            print(f"Exception in try_do_jobs_classla\n{traceback.format_exc()}")
        finally:
            time.sleep(3)


### Picking jobs for looping
def try_do_jobs_doc2text():
    while True:
        try:
            unfinished_jobs_big = []
            unfinished_jobs_small = []
            if doc2text_sem_big._value > 0:
                unfinished_jobs_big.extend(Job.select().where(Job.finished_on.is_null(), Job.started_on.is_null(),
                                                              Job.job_type << [1, 12, 3, 32],
                                                              Job.input_size > DOC2TEXT_SMALL_SIZE_LIMIT) \
                                           .limit(doc2text_sem_big._value))
            if doc2text_sem_small._value > 0:
                unfinished_jobs_small.extend(Job.select().where(Job.finished_on.is_null(), Job.started_on.is_null(),
                                                                Job.job_type << [1, 12, 3, 32],
                                                                Job.input_size <= DOC2TEXT_SMALL_SIZE_LIMIT) \
                                             .limit(doc2text_sem_small._value))

            ts_s = [KThread(target=execute_doc2text_job, args=(job, doc2text_sem_small,)) for job in
                    unfinished_jobs_small]
            ts_b = [KThread(target=execute_doc2text_job, args=(job, doc2text_sem_big,)) for job in
                    unfinished_jobs_big]
            ts = ts_s + ts_b
            for t in ts:
                running_threads[t._args[0].id] = t
                t.start()

            # if len(unfinished_jobs_big) > 0:
            #     with cf.ThreadPoolExecutor(max_workers=DOC2TEXT_CONCURANCE_LIMIT_BIG) as ex:
            #         [ex.submit(execute_doc2text_job, job, doc2text_sem_big) for job in unfinished_jobs_big]
            # if len(unfinished_jobs_small) > 0:
            #     with cf.ThreadPoolExecutor(max_workers=DOC2TEXT_CONCURANCE_LIMIT_SMALL) as ex:
            #         [ex.submit(execute_doc2text_job, job, doc2text_sem_small) for job in unfinished_jobs_small]
        except Exception as e:
            print(f"Exception in try_do_jobs_doc2text\n{traceback.format_exc()}")
        finally:
            time.sleep(3)


# async def prep_jobs(tasks):
#     await asyncio.gather(*tasks)


####### JOB EXECUTION LOGIC
def execute_doc2text_job(job: Job, sem: threading.Semaphore):
    try:
        sem.acquire()
        del_file = False
        job.started_on = datetime.datetime.utcnow()
        job.save()

        tmp_file_path = job.input_file
        if not os.path.exists(tmp_file_path):
            job.finished_on = datetime.datetime.utcnow()
            job.job_output = "ERROR - Temporary file went missing, couldn't properly finish job. Please try executing the job again."
            job.save()
            return

        with open(tmp_file_path, 'rb+') as f:
            file = FileStorage(f)
            jtype = job.job_type
            text = ""
            if jtype in [1, 12]:
                text, _ = txt_utils.extract_text_prepResp(file)
            elif jtype in [3, 32]:
                text, _ = txt_utils.ocr_text_prepResp(file)

            if jtype in [1, 3]:
                job.job_output = text
                job.finished_on = datetime.datetime.utcnow()
            elif jtype in [12, 32]:
                job.job_input = text
                job.job_type = 2
                job.input_size = len(text)
                del_file = True
            job.save()
        if del_file:
            try:
                os.remove(tmp_file_path)
            except:
                pass
    except Exception as ex:
        print("EX0")
        print(str(ex))
        job.started_on = None
        job.save()
    finally:
        print("releasing0")
        sem.release()
        try:
            del running_threads[job.id]
        except:
            pass


####### JOB EXECUTION LOGIC
def execute_classla_job(job: Job, sem: threading.Semaphore):
    try:
        print(f"Hello there {sem} - {sem._value}")
        sem.acquire()
        print(f"Hello there again {sem} - {sem._value}")
        job.started_on = datetime.datetime.utcnow()
        job.save()
        conllu, status = cl_utils.raw_text_to_conllu(job.job_input)
        if status != 200:
            conllu = f'ERROR - {conllu}'
        job.job_output = conllu
        job.finished_on = datetime.datetime.utcnow()
        job.save()
    except Exception as ex:
        print("EX1")
        print(str(ex))
        job.job_output = "ERROR - Something unexpected went wrong. Logs have been saved. Please contact the api admin if the problem persists."
        job.finished_on = datetime.datetime.utcnow()
        job.save()
        print(f"Unexpected error at job {job.id}\n{traceback.format_exc()}")
    finally:
        print("releasing1")
        sem.release()
        try:
            del running_threads[job.id]
        except:
            pass


####### JOB EXECUTION LOGIC
def execute_ateapi_job(job: Job, sem: threading.Semaphore):
    try:
        sem.acquire()
        job.started_on = datetime.datetime.utcnow()
        job.save()
        info = json.loads(job.job_input)
        _res = do_izlusci(info['conllus'], info['prepovedane_besede'])
        if type(_res) is tuple:
            ret_json = _res[0]
            if _res[1] != 200:
                ret_json = f'ERROR - {ret_json}'
        else:
            try:
                if type(_res.response) is dict:
                    ret_json = str(_res.response)
                else:
                    try:
                        ret_json = _res.response[0].decode('utf-8')
                    except:
                        ret_json = "ERROR - Unknown exception."

                if _res.status_code != 200:
                    ret_json = f'ERROR - {ret_json}'
            except:
                ret_json = "ERROR - Unknown exception."
        job.job_output = json.dumps(ret_json, ensure_ascii=False)
        job.finished_on = datetime.datetime.utcnow()
        job.save()
    except Exception as ex:
        print("EX2")
        print(str(ex))
        job.job_output = "ERROR - Something unexpected went wrong. Logs have been saved. Please contact the api admin if the problem persists."
        job.finished_on = datetime.datetime.utcnow()
        job.save()
        print(f"Unexpected error at job {job.id}\n{traceback.format_exc()}")
    finally:
        print("releasing2")
        sem.release()
        try:
            del running_threads[job.id]
        except:
            pass


####### JOB EXECUTION LOGIC
def execute_izluscipoiskanju_job(job: Job, sem: threading.Semaphore):
    try:
        sem.acquire()
        job.started_on = datetime.datetime.utcnow()
        job.save()
        info = json.loads(job.job_input)
        terKand = db_utils.vrni_oss_terminoloske_kandidate(info['leta'], info['vrste'], info['kljucne_besede'],
                                                           info['prepovedane_besede'], info['udk'])
        job.job_output = json.dumps(terKand, ensure_ascii=False)
        job.finished_on = datetime.datetime.utcnow()
        job.save()
    except Exception as ex:
        print("EX3")
        print(str(ex))
        job.job_output = "ERROR - Something unexpected went wrong. Logs have been saved. Please contact the api admin if the problem persists."
        job.finished_on = datetime.datetime.utcnow()
        job.save()
        print(f"Unexpected error at job {job.id}\n{traceback.format_exc()}")
    finally:
        print("releasing3")
        sem.release()
        try:
            del running_threads[job.id]
        except:
            pass


clear_up_unfinished_jobs()
loop = asyncio.get_event_loop()


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(try_do_jobs())


t = Thread(target=loop_in_thread, args=(loop,))
t.start()
