from peewee import *
from datetime import datetime
import os

LOCAL_PATH = "requets_db/dbs"
SERVER_PATH = "swagger_server/requets_db/dbs"

if not os.path.exists(LOCAL_PATH):
    if os.path.exists('requets_db'):
        os.makedirs(LOCAL_PATH, exist_ok=True)
    elif os.path.exists('swagger_server/requets_db'):
        os.makedirs(SERVER_PATH, exist_ok=True)

DB = f'{LOCAL_PATH}/jobs.db'
if not os.path.exists(LOCAL_PATH):
    DB = f'{SERVER_PATH}/jobs.db'
db = SqliteDatabase(DB, pragmas={
    # 'journal_mode': 'wal',
    'cache_size': -1 * 128 * 1024,  # 128MB
    'foreign_keys': 1
})


class BaseModel(Model):
    class Meta:
        database = db


class Job(BaseModel):
    id = AutoField()
    job_type = IntegerField()  # 1 = oznaci besedilo
    job_input = TextField(index=True)
    job_output = TextField(null=True)
    created_on = DateTimeField(default=datetime.utcnow)
    finished_on = DateTimeField(null=True)
    input_size = IntegerField()
    started_on = DateTimeField(null=True)


# db.drop_tables([Job])
db.create_tables([Job])


class JobManager:
    @staticmethod
    def create_job(job_type, job_input) -> Tuple(Job, bool):
        """
        :param: job_type
        :possibilities:
        1 = txt to classla
        2 = file to txt and then mark with classla
        3 = file with ocr then to classla

        :return: Job object, Did already exist boolean
        """
        try:
            job, is_new = Job.get_or_create(job_type=job_type, job_input=job_input, input_size=len(job_input))
            return job, not is_new
        except Exception as e:
            print(f'Exception at creating a job: {e}')
            return None, False

        # try:
        #     job = Job.get_or_none(Job.job_input == job_input, Job.job_type == job_type)
        #     if job:
        #         return job, True
        #     job = Job.create(job_type=job_type, job_input=job_input, input_size=len(job_input))
        #     return job, False
        # except Exception as e:
        #     print(f'Exception at creating a job: {e}')
        #     return None, False
