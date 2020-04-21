from pymongo import MongoClient

class Search:
    def __init__(self,num_results):
        self.client = MongoClient()
        self.db = self.client['med_articles']
        self.coll = self.db.articles_text
        self.num_results = num_results

    def __del__(self):
        self.client.close()
    
    def search_articles(self,search_token):
        m_search = {"$text" : {"$search":search_token}}
        res = self.coll.find(m_search)
        ids = []
        for i in range(self.num_results):
            ids.append(res[i]['article_id'])
        return ids

