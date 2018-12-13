import numpy as np
from modeles import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import DBSCAN

class ClusteringModel:

    def __init__(self, index, model, clusteringAlgo , orderClusters = '', orderDocs = '', nbrDocs = 100):
            
        """
        model : IRModel
        clusteringAlgo : algo de clustering
        orderClusters : Order des Clusters { rang, similarité Requette, nombre de docs Croissant, nbre de docs décroissant}
        orderDocs : Order des documents { rang, similarité docs}
        nbrDocs : numbre de documents a retourner        
        """
        
        self.index = index
        self.model = model
        self.clusteringAlgo = clusteringAlgo
        self.nbrDocs = nbrDocs
        self.orderClusters = orderClusters
        self.orderDocs = orderDocs
        
    def getRanking(self, query):
        
        # utiliser le rang avant 
        docsScore = self.model.getRanking(query, 0)
        #docsId = list(docsScore.keys())
        ndocs = list(docsScore.keys())[: self.nbrDocs]#  les n docs ordonnées 
         # apliquer un algorithme de clustering 
        docs_representation = [self.index.getTfdForDocs(ndocs[i]) for i in range(len(ndocs))]
        
        sparse_mtx = self._vectorizer(docs_representation)
        
        clusters = self.clusteringAlgo.fit_predict(sparse_mtx)
        
        
        clustersDocs = self._getClustersDocs(clusters, ndocs)
        result = []
        
        while( len(result) != len(ndocs)):
            for cluster in clustersDocs.keys():

                if ( (len (clustersDocs[cluster])) == 0) :
                    continue

                result.append(clustersDocs[cluster][0])
                
                clustersDocs[cluster].pop(0)
                                
        return result
    
    def _getClustersDocs(self, clusters, docs):
    
        clustersDocs = { cluster : [] for cluster in set(clusters) }
        for i, cluster in enumerate(clusters):
            clustersDocs[cluster].append(docs[i])
        
        return clustersDocs
    
        
    def rank(self):
        """
        utiliser le order cluster et le order docs 
        """
        pass
    
    def _vectorizer(self, list_):
        
        v = DictVectorizer(sparse = True)
        return  v.fit_transform(list_)
    
        
        
        
        
        
