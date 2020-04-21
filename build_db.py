import pandas as pd
import numpy as np
import sqlite3
from pymongo import MongoClient
from config import Config
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# returns sqlite connection 
def make_db_conn(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def make_mongo_conn():
    return MongoClient()

# returns pandas df with relevant columns from the raw medium 
# csv file
def build_articles_df(articles_csv):
    df = pd.read_csv(articles_csv)
    df.drop(df.columns.difference(['url','text','title','createdDatetime']),1,inplace=True)
    df.drop_duplicates(subset = ['url'],inplace = True)
    df.drop_duplicates(subset = ['title'],inplace = True)
    df['createdDatetime'] = pd.to_datetime(df['createdDatetime']).astype(np.int64)/10**9
    df.dropna(inplace=True)
    df = df[df['text'].str.len() > 250]
    df.reset_index(inplace = True)

    return df

# inserts the articles into the sqlite db
# and mongo db
def insert_records_to_db(df,cur,coll):
    for index,row in df.iterrows():
        cur.execute('insert into articles (title,url,create_time) values (?,?,?);',
                  (row['title'],row['url'],row['createdDatetime']))
        article_id = cur.lastrowid
        to_mongo = {'title':row['title'],'text':row['text'],
                    'article_id':article_id}
        coll.insert_one(to_mongo)
    cur.execute('select count(*) from articles;')
    val = cur.fetchall()[0][0]
    cur.execute('insert into article_counts(num_articles) values (?);',(val,))
    return 

# makes the tfidf matrix from the articles in the 
# database
def make_tfidf_from_df(df,cfg):
    vec = TfidfVectorizer(input='content',
            decode_error='replace',strip_accents='unicode',
            stop_words='english',ngram_range=(1,2),
            max_features = 10000,sublinear_tf=True)

    train_recs = list(df['text'].sample(frac=.5).values)
    vec.fit(train_recs)
    records = list(df['text'].values)
    X = vec.transform(records)
    pickle.dump(X,open(cfg.xfile,'wb'))
    return 
     
if __name__ == '__main__':
    
    cfg = Config()
    data_path = cfg.data_path
    print('building articles data frame...')
    df = build_articles_df(data_path)
    print('done')
    conn = make_db_conn(cfg.db_file)
    cur  = conn.cursor()
    mongo_client = make_mongo_conn()
    coll = mongo_client['med_articles'].articles_text
    print('adding articles to sqlite...')
    insert_records_to_db(df,cur,coll)
    conn.commit()
    print('done')
    print('making tfidf vector...')
    make_tfidf_from_df(df,cfg)
    print('done')



