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
            irlist = IRList(query, self.model)
            #print(irlist)
            evaluation = self.evaluation(irlist)
            l.append(evaluation)
            
        return np.mean(l)  
    def precision(self):
        l = []
        for query in self.queries:
            irlist = IRList(query, self.model)
            
            evaluation = self.precision_(irlist)
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

    def precision_(self, irlist):
        docs = irlist.getRanking()
        revelants = irlist.getQuery().get_revelant() 
        
        pertRet = [ tuple_[0] for tuple_ in revelants]
        precision = []
        tp = 0.0
        i = 0
        while i < len(docs) and tp < len(pertRet):
            (doc, score) = docs[i]
            if doc in pertRet:
                tp += 1
                precision.append( tp / (i + 1))
            i += 1
        return precision
    
    def rappel_(self, irlist):
        docs = irlist.getRanking()

        revelants = irlist.getQuery().get_revelant() 
        pertRet = [ tuple_[0] for tuple_ in revelants]
        rappel = []
        tp = 0.0
        i = 0
        while i < len(docs) and tp < len(pertRet):
            (doc, score) = docs[i]
            if doc in pertRet:
                tp += 1
                rappel.append( tp / len(pertRet) )
            i += 1
        return rappel 
    
    
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
        
        docs = irlist.getRanking()[: self.n]
        #print("evaluation", docs)
            
        revelants = irlist.getQuery().get_revelant()
        #print(" text of query:::::",irlist.getQuery().get_text())
        pertRet = [ tuple_[0] for tuple_ in revelants]
        
        nbPertRet = 0
        
        for doc in docs :
            if (doc in pertRet) :
                nbPertRet += 1
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
        """
        resulution de tous les parametres 
        """
        
        #nbrSousThemes = irlist.getQuery().getSubthemesCount()
        docs = irlist.getRanking()[: self.n]
        #print("docs", docs)
        #docs = [tuple_[0] for tuple_ in docsRanking_n]
            
        revelants = irlist.getQuery().get_revelant()
        sousThemes = [tuple_[1][1] for tuple_ in revelants]
        #print(sousThemes)
        nbrSousThemes = len(set(sousThemes))
        dic = {tuple_[0]: tuple_[1][1] for tuple_ in revelants}       
        subThemes = []
        
        for doc in docs :
            if (doc in dic.keys()) :
                subThemes.append(dic[doc])
                #print("in boucle", doc)
        """        
        print("subThemes", subThemes) 
        print("###docs", docs)
        print("documents in requette", dic.keys())
        print("sousThemes", set(sousThemes))
        print("########################result", len(set(subThemes)) / float(nbrSousThemes)) 
        """
        return len(set(subThemes)) / float(nbrSousThemes)
        

    