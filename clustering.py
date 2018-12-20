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
        docsScore = self.model.getRanking(query)
        ndocs = [tuple_[0] for tuple_ in docsScore][: self.nbrDocs] #  les n docs ordonnées
        #docsId = list(docsScore.keys())
        #print("ndocs", ndocs)
        # apliquer un algorithme de clustering 
        docs_representation = [self.index.getTfdForDocs(ndocs[i]) for i in range(len(ndocs))]
        
        sparse_mtx = self._vectorizer(docs_representation)
        
        clusters = self.clusteringAlgo.fit_predict(sparse_mtx)
        #print("clusters", clusters)
        clustersDocs = self._getClustersDocs(clusters, ndocs)
        #print("clustersdocs", clustersDocs)
        #print("labels", self.clusteringAlgo.labels_)
        result = []
        orderclusters = list(set(clusters))
        orderclusters.sort(key=lambda x: list(clusters).index(x))
        
        while( len(result) != len(ndocs)):
            for cluster in orderclusters:

                if ( (len (clustersDocs[cluster])) == 0) :
                    
                    continue

                result.append(clustersDocs[cluster][0])
                
                clustersDocs[cluster].pop(0)
        #print(result)
        return result
    
    def _getClustersDocs(self, clusters, docs, rank = "rang"):
        if (rank == "rang"):
            clustersDocs = { cluster : [] for cluster in set(clusters) }
            for i, cluster in enumerate(clusters):
                clustersDocs[cluster].append(docs[i])
            return clustersDocs
        if (rang == "similarity"):
            pass
    
        
    def rank(self):
        """
        utiliser le order cluster et le order docs 
        """
        pass
    
    
    
    def _vectorizer(self, list_):
        
        v = DictVectorizer(sparse = True)
        return  v.fit_transform(list_)
    
        
        
        
        
        
