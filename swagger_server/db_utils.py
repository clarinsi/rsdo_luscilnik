import mariadb
import sys


# todo: DO NOT PUSH THIS TO GIT
database_info = {
    'database': '...',
    'host': '...',
    'port': 0000,
    'user': '...',
    'password': '...'
}

# PUT THIS IN INSTEAD WHEN COMMITING, THIS IS ONLY TEMPORARY UNTIL AN .env FILE IS ADDED
database_info_tmp = {
    'database': '...',
    'host': '...',
    'port': 0000,
    'user': '...',
    'password': '...'
}

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(**database_info)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

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
