from sklearn import svm
import pickle
import numpy as np

class Rec():
    
    def __init__(self,db,xfile,num_recs):
        self.db = db
        self.X = pickle.load(open(xfile,'rb'))
        self.num_recs = num_recs

    def _get_user_yvec(self,user_id):
        rows = self.db.get_user_articles(user_id)
        if len(rows) == 0: return None
        articles = np.array([rows[i]['article_id'] - 1 for i in range(len(rows))])
        num_articles = self.db.get_article_counts()
        y = np.zeros(num_articles)
        y[articles] = 1
        return y
    
    def _train_svm(self,y):
        clf = svm.LinearSVC(class_weight = 'balanced', verbose = False,
                            max_iter=10000,tol=1e-6,C=0.1)
        clf.fit(self.X,y)
        return clf
        
    def get_user_recs(self,user_id):
        yvec = self._get_user_yvec(user_id)
        if yvec is None: return None
        clf = self._train_svm(yvec)
        scores = clf.decision_function(self.X)
        # we don't want to recommend already saved articles - push these
        # to the bottom of the recommendations
        scores[np.where(yvec == 1)] = float('-inf')
        recs = np.argsort(-scores)[:self.num_recs] + 1
        return recs.tolist()



