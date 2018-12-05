import numpy as np


class Weighter:
    
    def __init__(self, index):
        self.index = index 
        
        self.docsNorm = None
    
    def normalisedDocs(self):
        docNormalizedd=dict()
        for d in self.index.getListDocs():
            docNormalizedd[d] = 0
            stems=self.getDocWeightsForDoc(d)
            for t in stems:
                docNormalizedd[d] += stems[t]**2
            docNormalizedd[d] = np.sqrt(docNormalizedd[d])               
        return docNormalizedd
    


    def getDocWeightsForDoc(self,idDoc):
        pass

    def getWeightsForQuery(self, query):
        pass
    
    def idf(self, stem):
        
        n = len(self.index.getListDocs())
        df = len(self.index.getTsForStem(stem).keys())
        return np.log((1 + n) / float(1 + df))


class Weighter_01(Weighter):

    def getDocWeightsForDoc(self, idDoc): 
        
        return self.index.getTfdForDocs(idDoc)
    
    def getDocWeightsForStem(self, stem):
        
        return self.index.getTsForStem(stem)
    
    def getWeightsForQuery(self, query):
        return {key : 1 for key in query.keys()}

class Weighter_02(Weighter):

    def getDocWeightsForDoc(self, idDoc):
        
        return self.index.getTfdForDocs(idDoc)
    
    def getDocWeightsForStem(self, stem):
        
        return self.index.getTsForStem(stem)
    
    def getWeightsForQuery(self, query):     
        
        return query
 

class Weighter_03(Weighter):

    def getDocWeightsForDoc(self, idDoc):
        
        return self.index.getTfdForDocs(idDoc)
    
    def getDocWeightsForStem(self, stem):
        
        return self.index.getTsForStem(stem)
    
        
    def getWeightsForQuery(self, query):     
 
        return {key : self.idf(key) for (key, value) in query.items() }

         
class Weighter_04(Weighter):
    
    def getDocWeightsForDoc(self, idDoc):
        
        return {key : (1 + np.log(value)) for (key, value) in self.index.getTfdForDocs(idDoc).items() }
       
    def getDocWeightsForStem(self, stem):
        
        return {key : (1 + np.log(value)) for (key, value) in self.index.getTsForStem(stem).items() }

        
    def getWeightsForQuery(self, query):     
 
        return {key : self.idf(key) for (key, value) in query.items() }
    
class Weighter_05(Weighter):
    
    def getDocWeightsForDoc(self, idDoc):
        
        return {key : (1 + np.log(value)) * self.idf(key) for (key, value) in self.index.getTfdForDocs(idDoc).items() }
    
    def getDocWeightsForStem(self, stem):
        
        return {key : (1 + np.log(value)) * self.idf(key) for (key, value) in self.index.getTsForStem(stem).items() }

        
    def getWeightsForQuery(self, query):     
 
        return {key : (1 + np.log(value)) * self.idf(key) for (key, value) in query.items() }
    

                