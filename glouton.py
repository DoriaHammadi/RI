import numpy as np
from modeles import *
import copy

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

def GetBest(l_keys):
    r
    return
class GloutonModel(ModelDiversity):

    def __init__(self, index, model , orderGlouton = '', orderDocs = '', nbrDocs = 100, alpha = 0.9):

        """
        model : IRModel
        clusteringAlgo : algo de clustering
        orderClusters : Order des Clusters { rang, similarité Requette, nombre de docs Croissant, nbre de docs décroissant}
        orderDocs : Order des documents { rang, similarité docs}
        nbrDocs : numbre de documents a retourner
        """
        self.alpha = alpha
        self.index = index
        self.model = model
        self.nbrDocs = nbrDocs
        self.orderGlouton = orderGlouton
        self.orderDocs = orderDocs

    def getSim1(self, doc, query, norm = False) :
        res = 0
        for k in query.keys():
            if k in doc.keys():
                res+=1
        return res

    def getBest(self,l_keys, query, docs_representation, rank, alpha = 0.1):
        valmax = None
        res = None
        for du in l_keys :
            tmp_l_keys = copy.deepcopy(rank)
            sim1 = self.getSim1(docs_representation[du], query)
            l_sim2 = []
            for di in rank:
                l_sim2.append(self.getSim1(docs_representation[du], docs_representation[di]))
            if not l_sim2:
                sim2 = 0
            else :
                sim2 = max(l_sim2)
            val  = alpha*sim1 - (1 - alpha)*sim2
            if (valmax == None) or (valmax < val):
                valmax = val
                res = du

        return res
    def getRanking(self, query):
        #choisir un ranking pour les cluster

        # utiliser le rang avant
        docsScore = self.model.getRanking(query)
        #print(len(docsScore))
        ndocs = [tuple_[0] for tuple_ in docsScore][: self.nbrDocs] #  les n docs ordonnées
        #docsId = list(docsScore.keys())

        docs_representation = dict()
        for k in ndocs :
            docs_representation[k] = self.index.getTfdForDocs(k)
        l_keys = list(docs_representation.keys())
        rank = []
        while(len(l_keys) > 1):
            a = self.getBest(l_keys,query, docs_representation,rank, self.alpha)
            rank.append(a)
            l_keys.remove(a)
        rank.append(l_keys[0])

        return rank

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
