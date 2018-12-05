import numpy as np
import pandas as pd
from QueryParser import *
from IRList import * 

class EvalMeasure:
#s """ utilisation des class de traitement des imanges """   
    def __init__(self, model, queries):
        self.model = model
        self.queries = queries

    def Evaluation_queries(self):
        l = []
        for query in self.queries:
            print('boucle')
            irlist = IRList(query, self.model)
            #print(irlist)
            evaluation = self.Eval(irlist)
            l.append(evaluation)
        df = pd.DataFrame(l)
            
        return df.mean()
    
    def precesion(self):
        l = []
        for query in self.queries:
            irlist = IRList(query, self.model)
            evaluation = self.precesion_(irlist)
            l.append(evaluation)
        df = pd.DataFrame(l)
            
        return df.mean()
    
    def rappel(self):
        l = []
        for query in self.queries:
            irlist = IRList(query, self.model)
            evaluation = self.rappel_(irlist)
            l.append(evaluation)
        df = pd.DataFrame(l)
            
        return df.mean()
    
class Pn(EvalMeasure):
    
    def __init__(self, model, queries, n):
        
        '''
        model : Model
        queries : list of query
        n : Int
        return P@n
        '''
        
        super().__init__(model, queries)
        self.n = n
    
    def evaluation(self, irlist):
        
        docsRanking = irlist.getRanking()[: self.n]
        docs = [tuple_[0] for tuple_ in docsRanking]
        revelants = irlist.getQuery().get_revelant()
        pertRet = [ tuple_[0] for tuple_ in revelants]
        
        nbPertRet = 0
        
        for doc in docs :
            if (doc in pertRet) :
                nbPertRet += 1
        print(nbPertRet)       
        return nbPertRet / float(self.n)  
    
class CRn(EvalMeasure):
    
    def __init__(self, model, queries, n):
        
        '''
        model : Model
        queries : list of query
        n : Int
        return P@n
        '''
        
        super().__init__(model, queries)
        self.n = n
    
    def evaluation(self, irlist):
        # calculer le nombre de sous themes total !!!!!
        docsRanking = irlist.getRanking()[: self.n]
        docs = [tuple_[0] for tuple_ in docsRanking]
        revelants = irlist.getQuery().get_revelant()
        dic = {tuple_[0]: tuple_[1][1] for tuple_ in revelants}       
        subTerms = []
        
        for doc in docs :
            if (doc in dic.keys()) :
                subTerms.append(dic[doc])
                
        print(subTerms)   
        
        return len(set(subTerms)) 
        #return len(set(subTerms)) / float(nb)
        

    