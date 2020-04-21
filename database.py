import sqlite3
import numpy as np
import time

class Db:
    def __init__(self,db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cur  = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_user(self,user_id):
        sql = 'select 1 from users where user_id = ?;'
        self.cur.execute(sql,(user_id,))
        return self.cur.fetchall()
    
    def add_user(self,uname,pw_hash):
        sql = 'insert into users (username,pw_hash,time_created) ' \
              'values (?,?,?);'
        try:
            self.cur.execute(sql,(uname,pw_hash,int(time.time())))
        except sqlite3.IntegrityError as e:
            return -1
        self.conn.commit()
        user_id = self.cur.lastrowid
        return user_id

    def get_user_info(self,uname):
        sql = 'select * from users where username = ?;'
        self.cur.execute(sql,(uname,))
        return self.cur.fetchall()

    def add_article_to_lib(self,user_id,article_id):
        sql = 'insert into library (article_id,user_id,update_time) ' \
              'values (?,?,?);'
        self.cur.execute(sql,(article_id,user_id,int(time.time())))
        self.conn.commit()
        return self.cur.lastrowid

    def remove_article_from_lib(self,user_id,article_id):
        sql = 'delete from library where ' \
              '(user_id = ? and article_id = ?);'
        self.cur.execute(sql,(user_id,article_id))
        self.conn.commit()
        return None

    def get_articles_by_id(self,user_id,article_ids):
        # we join on the user table to get the status of each 
        # article, i.e. saved or unsaved - this info is used to 
        # decorate buttons next to article links 

        sql = 'select title,url,articles.article_id,t.lib_id ' \
              'from articles ' \
              'left join (select * from library where user_id = ?) as t ' \
              'on articles.article_id = t.article_id ' \
              'where articles.article_id in ({seq});' \
              .format(seq=','.join(['?']*len(article_ids)))
        
        args = [user_id]
        args.extend(article_ids)
        self.cur.execute(sql,args)
        rows = self.cur.fetchall()
        return rows

    def get_articles_by_time(self,user_id,num_articles):
        sql = 'select title,url,articles.article_id,t.lib_id ' \
              'from articles ' \
              'left join (select * from library where user_id = ?) as t ' \
              'on articles.article_id = t.article_id ' \
              'order by articles.create_time desc ' \
              'limit ?;'
        
        self.cur.execute(sql,(user_id,num_articles))
        return self.cur.fetchall()

    def get_article_counts(self):
        sql  = 'select * from article_counts;'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows[0]['num_articles']

    def get_user_articles(self,user_id):
        sql = 'select title,url,articles.article_id,lib_id ' \
              'from library ' \
              'left join articles ' \
              'on articles.article_id = library.article_id ' \
              'where library.user_id = ?;'

        self.cur.execute(sql,(user_id,))
        rows = self.cur.fetchall()
        return rows


