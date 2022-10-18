import mariadb
import os
import sys

database_info = {
    'database': os.getenv("MDB_DATABASE", "oss"),
    'host': os.getenv("MDB_HOST", "localhost"),
    'port': int(os.getenv("PORT", 3306)) ,
    'user': os.getenv("MDB_USER", "root"),
    'password': os.getenv("MDB_PASSWORD", "root"),
}

cur = None
# Connect to MariaDB Platform

def get_files_by_udc(udc):
    ret = []

    try:
        print(database_info)
        conn = mariadb.connect(**database_info)
        cur = conn.cursor()
        where_in = ','.join(['%s'] * len(udc))
        print(where_in)
        sql = "select distinct xml_id from metadata_udc where udk IN (%s)" % (where_in)
        print(sql)
        cur.execute(sql,udc)
        #cur.execute(f'SELECT COUNT(*) FROM os2022_ngrams')
        ret = list(cur)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    

    return ret

def vrni_oss_dokumente(leta, vrste, kljucnebesede, udk):
    ret = []
  
    try:
        print(database_info)
        conn = mariadb.connect(**database_info)
        cur = conn.cursor()
        
        
        
        sql = "select distinct xml_id from metadata"
        where=""
        params=[]
        if (udk):
            where_in_udk = ','.join(['%s'] * len(udk))
            where=" udk IN (%s) " % (where_in_udk)
            params=udk
        
        if (leta):

            where_in_leta = ','.join(['%s'] * len(leta))
            if (where):
                where=where+ " AND "
            where=where + " leto IN (%s) " % (where_in_leta)
            params=params+leta
        
        if (vrste):
            if (where):
                where=where+ " AND "
            where_in_vrste = ','.join(['%s'] * len(vrste))
            where=where + " tipologija IN (%s) " % (where_in_vrste)
            params=params+vrste

        if (kljucnebesede):
            if (where):
                where=where+ " AND "
            where_in_kb = ','.join(['%s'] * len(kljucnebesede))
            where=where + " kljucnabeseda IN (%s) " % (where_in_kb)
            params=params+kljucnebesede

        if(where):
            sql=sql+" where " + where
        
        print(sql)
        print(params)
        
        cur.execute(sql,params)
        
        ret = list(cur)
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


#class Ngrams_Manager:
    #@staticmethod
    #def get_by_file_id(file_id):
        #try:
            # cur.execute(f'SELECT * from os2022_ngrams WHERE file_id = {file_id}')
            # cur.execute(f'SELECT COUNT(*) FROM os2022_ngrams')
            # return list(cur)
         #   return 1
        #except Exception as e:
            #print(e, 'EXC')
        #return 0
