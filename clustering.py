import numpy as np
from modeles import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import DBSCAN




class ModelDiversity :
    
    def __init__(self, model, nbreDocs = 100):
        self.model = model
    
class RandomDiversityModel(ModelDiversity):
    
    def __init__(self, model, nbDocs):
        
        super(RandomDiversityModel, self).__init(model)
        self.nbDocs = nbDocs
        
    def getRanking(self, query):
        # prendre les documents aleatoirement ( ne pas prendre en compte le resultat de model 
        pass
        
        
        
class ClusteringModel(ModelDiversity):

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
        #choisir un ranking pour les cluster 
        
        
        # utiliser le rang avant 
        docsScore = self.model.getRanking(query)
        #print(len(docsScore))
        ndocs = [tuple_[0] for tuple_ in docsScore][: self.nbrDocs] #  les n docs ordonnées
        #docsId = list(docsScore.keys())
        
        # apliquer un algorithme de clustering 
        docs_representation = [self.index.getTfdForDocs(ndocs[i]) for i in range(len(ndocs))]
        
        sparse_mtx = self._vectorizer(docs_representation)

        clusters = self.clusteringAlgo.fit_predict(sparse_mtx)
        #print("clusters", clusters)
        #print("docs", ndocs)
        #print("labels", self.clusteringAlgo.labels_)
        clusterDocs = self._getClustersDocs(clusters, ndocs)
        #print("aaaaaa", clusterDocs)
        result = []
        
        orderclusters = list(set(clusters))
        orderclusters.sort(key=lambda x: list(clusters).index(x))
        #print("orderclusters", orderclusters)

        
        while( len(result) != len(ndocs)):            
            for cluster in orderclusters:

                if ( (len (clusterDocs[cluster])) == 0) :                    
                    continue
                result.append(clusterDocs[cluster][0])
                
                clusterDocs[cluster].pop(0)
        #print("result", result)
        return result
    
    def _getClustersDocs(self, clusters, docs, rank = "rang"):
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
    