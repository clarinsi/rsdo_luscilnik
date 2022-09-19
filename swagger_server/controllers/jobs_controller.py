import datetime
import os.path

import peewee
import asyncio
import concurrent.futures as cf
from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server.requets_db.models.vrsta import (Job)
from threading import Thread
from swagger_server.classla import cl_utils
from swagger_server.utils import txt_utils
from werkzeug.datastructures import FileStorage
import threading
import time

CLASSLA_CONCURANCE_LIMIT = 3
DOC2TEXT_CONCURANCE_LIMIT = 4

classla_sem = threading.Semaphore(CLASSLA_CONCURANCE_LIMIT)
doc2text_sem = asyncio.Semaphore(DOC2TEXT_CONCURANCE_LIMIT)


def delete_job(job_id):  # noqa: E501
    """Izbriše job

     # noqa: E501

    :param job_id:
    :type job_id: int

    :rtype: str
    """
    return 'Endpoint currently disabled'


def get_job_status(job_id):  # noqa: E501
    """Vrne status

     # noqa: E501

    :param job_id:
    :type job_id: int

    :rtype: JobResponse
    """
    try:
        job = Job.get_by_id(job_id)
        if job.started_on is None:
            return JobResponse(job_status="waiting in que", created_on=job.created_on), 200
        if job.started_on is not None and job.finished_on is None:
            return JobResponse(job_status="currently processing", created_on=job.created_on,
                               started_on=job.started_on), 200
        if job.started_on is not None and job.finished_on is not None:
            return JobResponse(job_status="finished processing", created_on=job.created_on, started_on=job.started_on,
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
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(try_do_jobs_classla)
        ex.submit(try_do_jobs_doc2text)


### Job looping
def try_do_jobs_classla():
    time.sleep(15)  # wait for tokenizers to load for classla ...
    while True:
        try:
            if cl_utils.nlp_loaded:
                if classla_sem._value > 0:
                    unfinished_jobs_txt = Job.select() \
                        .where(Job.finished_on.is_null(), Job.job_type == 2,
                               Job.input_file.is_null(False)) \
                        .limit(classla_sem._value)

                    unfinished_jobs_no_txt = Job.select() \
                        .where(Job.finished_on.is_null(), Job.started_on.is_null(), Job.job_type == 2,
                               Job.input_file.is_null()) \
                        .limit(classla_sem._value)

                    unfinished_jobs = [j for j in unfinished_jobs_txt] + [j for j in unfinished_jobs_no_txt]
                    unfinished_jobs = unfinished_jobs[:classla_sem._value]
                    with cf.ThreadPoolExecutor(max_workers=CLASSLA_CONCURANCE_LIMIT) as ex:
                        [ex.submit(execute_classla_job, job) for job in unfinished_jobs]

        except Exception as e:
            print(f"Exception in {__name__}: {e}")
        finally:
            time.sleep(3)


### Job looping
def try_do_jobs_doc2text():
    while True:
        try:
            if doc2text_sem._value > 0:
                unfinished_jobs = Job.select() \
                    .where(Job.finished_on.is_null(), Job.started_on.is_null(), Job.job_type << [1, 12, 3, 32]) \
                    .limit(doc2text_sem._value)
                with cf.ThreadPoolExecutor(max_workers=DOC2TEXT_CONCURANCE_LIMIT) as ex:
                    [ex.submit(execute_doc2text_job, job) for job in unfinished_jobs]
        except Exception as e:
            print(f"Exception in {__name__}: {e}")
        finally:
            time.sleep(3)


async def prep_jobs(tasks):
    await asyncio.gather(*tasks)


def execute_doc2text_job(job: Job):
    try:
        doc2text_sem.acquire()
        del_file = False
        job.started_on = datetime.datetime.utcnow()
        job.save()

        tmp_file_path = job.input_file
        if not os.path.exists(tmp_file_path):
            job.finished_on = datetime.datetime.utcnow()
            job.job_output = "ERROR - Temporary file went missing, couldn't properly finish job"
            job.save()
            return

        with open(tmp_file_path, 'rb+') as f:
            file = FileStorage(f)
            jtype = job.job_type
            text = ""
            if jtype in [1, 12]:
                text = txt_utils.extract_text_prepResp(file)
            elif jtype in [3, 32]:
                text = txt_utils.ocr_text_prepResp(file)

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

    except:
        job.started_on = None
        job.save()
    finally:
        doc2text_sem.release()


def execute_classla_job(job: Job):
    try:
        classla_sem.acquire()
        job.started_on = datetime.datetime.utcnow()
        job.save()
        conllu, _ = cl_utils.raw_text_to_conllu(job.job_input)
        job.job_output = conllu
        job.finished_on = datetime.datetime.utcnow()
        job.save()
    finally:
        classla_sem.release()


clear_up_unfinished_jobs()
loop = asyncio.get_event_loop()


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(try_do_jobs())


t = Thread(target=loop_in_thread, args=(loop,))
t.start()
