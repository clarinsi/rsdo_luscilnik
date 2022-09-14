import datetime

import peewee
import asyncio

from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server.requets_db.models.vrsta import (Job)
from threading import Thread
from swagger_server.classla import cl_utils

CLASSLA_CONCURANCE_LIMIT = 4
classla_sem = asyncio.Semaphore(CLASSLA_CONCURANCE_LIMIT)


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
    # tu more but !=, ne deluje ce je "is not"
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
                        .where(Job.finished_on == None, Job.started_on == None, Job.job_type == 2) \
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
