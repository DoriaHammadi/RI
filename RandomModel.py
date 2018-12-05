from weighter import *
import numpy as np
import operator
import pandas as pd
import random

class randomWalk:
    
    def __init__(self,index, model, n, k):
        self.index = index
        self.model = model
        self.linksIn = dict()
        self.linksOut = dict()
        self.n = n
        self.k = k
    
    def graph(self, query):
        ''' 
        mise a jour les documents et des liens de graph        
        '''
        linksDocsCorpusIn = self.index.getLinksDocsIn()
        linksDocsCorpusOut = self.index.getLinksDocsOut()
        docsSeeds = list(self.model.getRanking(query, -100).keys())[:self.n]
        self.V = docsSeeds
        
        for doc in docsSeeds : 
            
            if(len(linksDocsCorpusIn[doc]) > 0):  
                
                if (len(linksDocsCorpusIn[doc]) < self.k):

                    self.V = list(set(self.V) | set(linksDocsCorpusOut[doc]) | set(random.sample(linksDocsCorpusIn[doc], self.k)))
                else:
                    self.V = list(set(self.V) | set(linksDocsCorpusOut[doc]) | set(linksDocsCorpusIn[doc]))  
                       
        #print('ok')
        for doc in self.V :
            self.linksIn[doc] = []
            self.linksOut[doc] = []
            
            for docj in linksDocsCorpusOut[doc] :
                #print("out", doc, docj)
                if(docj in self.V):
                    #if (docj in self.linksIn[doc]):
                     self.linksOut[doc].append(docj)
                                        
            for docj in linksDocsCorpusIn[doc]:

                if(docj in self.V):
                    if (docj in self.linksIn[doc]):
                         self.linksIn[doc].append(docj)
                    else:
                        self.linksIn[doc] = [docj]
                  
                
class PageRank(randomWalk):
    
    def __init__(self, index, model, n, k, d, maxIter) :
        super(PageRank, self).__init__(index, model, n, k)
        self.d = d
        self.maxIter = maxIter
        
    def getScores(self):       
        #create A
        A = pd.DataFrame(0.0, index = self.V, columns = self.V)
        N = float(len(self.linksOut.keys()))
        #### 
        for doci in self.linksIn:
            for docj in self.linksIn[doci]:

                if (len(self.linksOut[docj]) == 0):
                    A.loc[doci][docj] = 1 / N
                else:
                    A.loc[doci][docj] = 1 / float(len(self.linksOut[docj]))
        u = pd.DataFrame(1/N, index=self.linksOut.keys(), columns=[''])
        one = pd.DataFrame(1., index=self.linksOut.keys(), columns=[''])
        for it in range(0, self.maxIter):
            u = (1 - self.d) / N * one + self.d * (A.dot(u))
            
        final_scores = dict()
        for doc in self.linksOut:
            final_scores[doc] = u.loc[doc]['']
        return  final_scores

    # A VERIVIER
class hits(randomWalk):
    
    def __init__(self, index, model, n, k):
        super(Hits, self).__init__(index, model, n, k)
        self.index = index 
        self.linksIn = index.getLinksDocsIn()
        self.linksOut = index.getLinksDocsOut()
        
    def normalize(self, df):
        #A voir pour un  dataframe 
        return np.linalg.norm(df,2, axis = 1)
        
    def getScores(self, maxIter):
        
        a = pd.DataFrame(1., index=self.linksOut.keys(), columns=[''])
        h = pd.DataFrame(1., index=self.linksOut.keys(), columns=[''])
        # normaliser selon la norme L2 
        for i in range(maxIter):
            for i in a.index :
                ai = a
                for doc in self.linksOut[i]:
                    a.loc[i] +=  h.loc[doc] 
                    
                    for doc in self.linksIn[i]:
                        h.loc[i] += ai.loc[doc]
                 
            # voir comment normaliser une DataFrame !!!!!!
            '''
            print( a,h)
            a = self.normalize(a)
            h = self.normalize(h)
            print('after normalize')
            print(a,h)
            '''

        return a,h
    
                    