import mariadb
import os
import sys

database_info = {
    'database': os.environ.get("MDB_DATABASE", default="true"),
    'host': os.environ.get("MDB_HOST", default="true"),
    'port': os.environ.get("MDB_PORT", default="true"),
    'user': os.environ.get("MDB_USER", default="true"),
    'password': os.environ.get("MDB_PASSWORD", default="true"),
}

cur = None


# Connect to MariaDB Platform


def get_files_by_udc(udc):
    ret = []

    try:
        conn = mariadb.connect(**database_info)
        cur = conn.cursor()
        # cur.execute(f'SELECT * from os2022_ngrams WHERE file_id = {file_id}')
        # cur.execute(f'SELECT COUNT(*) FROM os2022_ngrams')
        # ret = list(cur)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    return ret


# class BaseModel(Model):
#     class Meta:
#         database = db
#
#
# class os2022_ngrams(BaseModel):
#     file_id = IntegerField()
#     sent_id = FloatField()
#     ngram_len = IntegerField()
#     frequency_g_t = IntegerField()
#     gram_text = TextField()
#     lemma_text = TextField()
#     xpos_text = TextField()
#     upos_text = TextField()
#
# db.connect()


class Ngrams_Manager:
    @staticmethod
    def get_by_file_id(file_id):
        try:
            # cur.execute(f'SELECT * from os2022_ngrams WHERE file_id = {file_id}')
            # cur.execute(f'SELECT COUNT(*) FROM os2022_ngrams')
            # return list(cur)
            return 1
        except Exception as e:
            print(e, 'EXC')
        return 0
