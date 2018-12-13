import numpy as np
import operator
import pandas as pd
from IRList import *

class IRmodel:   
    
    def __init__(self,  index):
        self.index = index
        
    def getScores(self, query):
        pass

    def getRanking(self, query, docsNull = 0):
        
        scores = self.getScores(query)
        scores_sorted = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        docs = self.index.getListDocs()
        
        docs_scoresZero = { key : docsNull for key in set(docs).difference(scores.keys())}
        return (scores_sorted + list(docs_scoresZero.items()))
       
    
class Vectoriel(IRmodel) :
    
    def __init__(self,  index, weighter, normalized = False):
        self.index = index
        self.weighter = weighter
        self.normalized = normalized
        
        
    def getScores(self, _query) :
        
        dico = dict()
        query = self.weighter.getWeightsForQuery(_query)
        for w in query.keys() :
            docs = self.weighter.getDocWeightsForStem(w)
            for d in docs.keys() :
                
                if d not in dico.keys(): dico[d]=([],[])
                    
                dico[d][0].append(docs[d])
                dico[d][1].append(query[w])
        res = dict()
        
        if(not self.normalized):
            for k in dico.keys():

                res[k] = np.dot(dico[k][0],dico[k][1])
        else:
            normeDocs = self.weighter.normalisedDocs()
            for k in dico.keys():

                a = [i / float(normeDocs[k]) for i in dico[k][0]]
                b = [i / float(sum(dico[k][1])) for i in dico[k][1]]

                res[k]=np.dot(a, b)
        return res

    
    
class ModelLangue(IRmodel):
    
    def __init__(self,  index, lamda = 0.5):
        
        self.lamda = lamda
        self.index = index
               
    def getScores(self, query):

        scores =dict()
        x = 0        
        for t in query :
            docs = self.index.getTsForStem(t)
            lengthDocs = self.index.getLengthDocs()

            for doc in docs :
                stems = self.index.getTfdForDocs(doc)

                if (doc in scores.keys( )):
                    scores[doc] += query[t] * np.log(self.lamda * (stems[t] / float(lengthDocs[doc])) + (1 - self.lamda) * float(sum(docs.values())) / sum(lengthDocs.values()))
                else:
                    scores[doc] = x + query[t] * np.log(self.lamda * (stems[t] / float(lengthDocs[doc])) + (1 - self.lamda) * float(sum(docs.values())) / sum(lengthDocs.values()))
                    
            for d in set(scores.keys()).difference(docs.keys()):
                scores[doc] += np.log((1 - self.lamda) * float(sum(docs.values())) / sum(lengthDocs.values()))
            
            x += np.log((1 - self.lamda) * float(sum(docs.values())) / sum(lengthDocs.values()))        
        return scores 
    
    def grid_MDL(self, index, train_list, lbd):
        max = -999
        scores = []
        for l in lbd :
            model = ModelLangue(index, l)
            sc = []

            for query in train_list :
                irlist = IRList(query, model.getRanking(query.get_query(), -100))
                sc.append(EvalMeasure.eval_ap(irlist))

            scores.append(np.mean(sc))
            if scores[-1] > max :
                max= scores[-1]
                res = l
        return res, scores




class ModelBM25(IRmodel):
    
    def __init__(self,index, k1 = 0.5, b = 0.75):
        self.index = index
        self.k1 = k1
        self.b = b
        
    def propaIdf(self, stem):
        
        n = len(self.index.getListDocs())
        df = len(self.index.getTsForStem(stem).keys())
        return max( 0,  (np.log((n - df + 0.5) / float(df + 0.5))))
    
    def getScores(self, query):
        
        scores = dict()
        for t in query :
            docs = self.index.getTsForStem(t)
            lengthDocs = self.index.getLengthDocs()
            for doc in docs : 
                stems = self.index.getTfdForDocs(doc)

                fdq = self.propaIdf(t) * ( ((self.k1 + 1) * stems[t]) / 
                                    (self.k1 * ((1 - self.b) +
                                                self.b *
                                                float(lengthDocs[doc]) /
                                                np.mean(list(lengthDocs.values()))) +
                                               stems[t]))
                if (doc in scores.keys()):
                    scores[doc] += fdq 
                else:
                    scores[doc] = fdq                    
        return scores
    
    def grid_BM25(self, index, train_list, lk1,lb):
        max = -999
        scores = []
        for k1 in lk1 :
            for b in lb:
                model = ModelBM25(index, k1=k1, b=b)
                sc = []

                for query in train_list :
                    irlist = IRList(query, model.getRanking(query.get_query()))
                    sc.append(EvalMeasure.eval_ap(irlist))

                scores.append(np.mean(sc))
                if scores[-1] > max :
                    max= scores[-1]
                    res = (k1,b)
        return res, scores

#print(grid_MDL(index, [dat['val'][0],dat['val'][1],dat['val'][2]],[0.1,0.5,0.9]))




