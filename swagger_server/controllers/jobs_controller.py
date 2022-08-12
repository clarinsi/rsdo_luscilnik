import datetime
import random

import connexion
import peewee
import six
import asyncio

from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server import util
from swagger_server.requets_db.models.vrsta import (Job, JobManager)
from threading import Semaphore, Thread
from swagger_server.classla import cl_utils

CLASSLA_CONCURANCE_LIMIT = 4
classla_sem = asyncio.Semaphore(CLASSLA_CONCURANCE_LIMIT)


def get_job_status(job_id, show_estimated_completion=None):  # noqa: E501
    """Vrne status

     # noqa: E501

    :param job_id:
    :type job_id: int
    :param show_estimated_completion: Calculate estimate time remaining based on various factors (could be inaccurate)
    :type show_estimated_completion: bool

    :rtype: JobResponse
    """
    try:
        job = Job.get_by_id(job_id)
        if not job.finished_on:
            est_com = None
            # todo: if estimate completion: calculate it and set it to est_com
            return JobResponse(finished_job=False, estimated_completion=est_com), 200
        return JobResponse(finished_job=True, completed_at=job.finished_on, job_result=job.job_output), 200
    except peewee.DoesNotExist as e:
        return "Job with this ID does not exist", 404


def clear_up_unfinished_jobs():
    """
    In case server crashed while jobs were in queue...
    """
    Job.update(started_on=None).where(Job.started_on != None, Job.finished_on == None).execute()


### Job looping
async def try_do_jobs():
    await asyncio.sleep(15)  # wait for tokenizers to load for classla ...
    while True:
        try:
            if cl_utils.nlp_loaded:
                # print(cl_utils.raw_text_to_conllu("Danes je lep soncen dan. Res je!"))
                if classla_sem._value > 0:
                    # classla
                    unfinished_jobs = Job.select() \
                        .where(Job.finished_on == None, Job.started_on == None, Job.job_type == 1) \
                        .limit(classla_sem._value)
                    tasks = [
                        asyncio.ensure_future(execute_classla_job(job))
                        for job in unfinished_jobs
                    ]
                    asyncio.get_event_loop().create_task(prep_classla_jobs(tasks))
                    # await asyncio.gather(*tasks)



            else:
                pass
        except Exception as e:
            print(f"Exception in ... {e}")
        finally:
            await asyncio.sleep(3)


async def prep_classla_jobs(tasks):
    await asyncio.gather(*tasks)


async def execute_classla_job(job: Job):
    async with classla_sem:
        job.started_on = datetime.datetime.utcnow()
        job.save()
        conllu, _ = cl_utils.raw_text_to_conllu(job.job_input)
        job.job_output = conllu
        job.finished_on = datetime.datetime.utcnow()
        job.save()


clear_up_unfinished_jobs()
loop = asyncio.get_event_loop()
def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(try_do_jobs())


t = Thread(target=loop_in_thread, args=(loop,))
t.start()


# clear_up_unfinished_jobs()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(try_do_jobs()) this version seems more at home, but it blocks the thread, fix that?
