import pathlib

import werkzeug.datastructures
from peewee import *
from datetime import datetime
import os
from swagger_server.util import get_random_filename
from werkzeug.utils import secure_filename

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
    id = AutoField(index=True)
    job_type = IntegerField()
    job_input = TextField(index=True, null=True)
    job_output = TextField(null=True)
    created_on = DateTimeField(default=datetime.utcnow)
    finished_on = DateTimeField(null=True)
    started_on = DateTimeField(null=True)
    input_size = IntegerField()
    input_file = TextField(index=True, null=True)


db.drop_tables([Job])  # TODO: After pushing this, comment it and push again
db.create_tables([Job])


class JobManager:
    @staticmethod
    def create_job(job_type, job_input) -> Tuple(Job, bool):
        """
        :param: job_type
        :possibilities:
        # 1 = pretvori datoteko v besedilo, 2 = oznaci besedilo, 12 = oboje
        # 3 = pretvori dat v besedilo OCR, 2 = oznaci besedilo, 32 = oboje
        # 4 = izlusci async

        :return: Job object, Did already exist boolean
        """
        try:
            if job_type in [2, 4]:
                job, is_new = Job.get_or_create(job_type=job_type, job_input=job_input, input_size=len(job_input))
            elif job_type in [1, 3, 12, 32]:
                tmp_file = ""
                while True:
                    # just in case a VERY rare chance of a same generate name happens
                    tmp_file = "tmp/" + secure_filename(get_random_filename() + "_" + job_input.filename)
                    if not os.path.exists(tmp_file):
                        break
                pathlib.Path('tmp').mkdir(exist_ok=True)
                job_input: werkzeug.datastructures.FileStorage
                job_input.save(tmp_file)
                job, is_new = Job.get_or_create(job_type=job_type, input_file=tmp_file, input_size=-1)
            return job, is_new

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
