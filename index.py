import Document
import porter
import TextRepresenter
import Parser
import ParserCACM
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


class Index:
    def __init__(self, parser_name, Parser = ParserCACM.ParserCACM(), TextRepresenter = TextRepresenter.PorterStemmer()):

        self.name = parser_name
        self.parser = Parser
        self.porter = TextRepresenter
        #self.index_f = None
        self.index = "index/" + self.name + "_index"
        self.index_inverted = "index/" + self.name + "_inverted"
        self.docsPositionIndex_File = "index/" + self.name + "_docsPositionIndex"
        self.stemsPositionIndexInv_File = "index/" + self.name + "_stemsPositionIndex"
        self.docsPositionIndex = None
        self.stemsPositionIndexInv = None

    def indextion(self, source):
        
        cpt = 0
        self.parser.initFile(source)

        index_file = open(self.index, "w")       
        doc = self.parser.nextDocument()
        docsPositionIndex=dict()
        lengthDocs = dict()
        listID = []
        while (doc != None):
            
            id_ = doc.getId()
            listID.append(id_)
                    
            to_w = (str(id_) + ":")
            docTextRep = self.porter.getTextRepresentation(doc.getText())
            lengthDocs[id_] = sum(docTextRep.values() )
            for w in docTextRep.items():
                to_w += str(w)+";"
            index_file.write(to_w)

            docsPositionIndex[id_] = (cpt,len(to_w) )
            cpt += len(to_w)
            doc = self.parser.nextDocument()
        index_file.close()
        
        save_obj(lengthDocs, 'index/' + self.name + '_lengthDocs')
        save_obj(docsPositionIndex,self.docsPositionIndex_File)
        
              
    def indextion_inverse(self,source):
        
        ### a completer
        cpt = 0
        self.parser.initFile(source)

        index_file = open(self.index_inverted, "w")
        #self.stems_docs = "index/" + self.name + "_inverted"

        dico_length = dict()
        stemsPositionIndexInv = dict()
        doc = self.parser.nextDocument()
        while (doc != None):
            id_ = doc.getId()

            for w in self.porter.getTextRepresentation(doc.getText()).items():
                if w[0] not in dico_length.keys():
                    dico_length[w[0]] =- 1
                    
               # print(str((id_.split("\r")[0],w[1])))
                dico_length[w[0]] += len(str((id_.split("\r")[0],w[1])))+1
            doc = self.parser.nextDocument()

        dico_place = dict()
        cpt = 0
        for w in dico_length.keys():
                dico_place[w] = cpt + len(w) + 2
                stemsPositionIndexInv[w] = (dico_place[w],dico_length[w])
                index_file.write(";" + str(w) + ":")
                index_file.write("0"*(dico_length[w]))
                cpt += dico_length[w] + len(w) + 2
                
        save_obj(stemsPositionIndexInv, self.stemsPositionIndexInv_File)
        self.parser.initFile(source)
        doc = self.parser.nextDocument()
                
        while(doc != None):

            id_ = doc.getId()

            for w in self.porter.getTextRepresentation(doc.getText()).items():
                index_file.seek(dico_place[w[0]],0)
                index_file.write(str((id_.split("\r")[0],w[1],))+";")
                dico_place[w[0]]+=len(str((id_.split("\r")[0],w[1])))+1
            doc = self.parser.nextDocument()

    def getTfdForDocs(self,doc):
        '''
        doc: numero de document
        return : dict d'items
        '''
        #returner les termes d'un document
        index_file = open(self.index, "r")
        if ( self.docsPositionIndex == None):
            self.docsPositionIndex = load_obj(self.docsPositionIndex_File)
        index_ind = self.docsPositionIndex[doc]

        index_file.seek(index_ind[0],0)
        rd = index_file.read()
        dict_doc = dict()
        for w in rd[:index_ind[1]].split(":")[1].split(";")[:-1] :
            item = w.split(',')

            dict_doc[item[0][2:-1]]=int(item[1][:-1])

        return dict_doc

    def getTsForStem(self,stem):
        '''
        stems
        return: dict of docs
        '''
        ############################################## A verifier ######################################################
        index_file = open(self.index_inverted, "r")
        if ( self.stemsPositionIndexInv == None):
            self.stemsPositionIndexInv = load_obj(self.stemsPositionIndexInv_File)
        index_ind_d = self.stemsPositionIndexInv
        #index_ind_d = load_obj(self.stems_docs)
        if stem not in index_ind_d.keys():
            return dict()

        index_ind =index_ind_d[stem]

        index_file.seek(index_ind[0],0)
        rd = index_file.read()[:index_ind[1]]
        dict_stem = dict()
        for w in rd.split(';'):
            item = w.split(',')
            dict_stem[item[0][2:-1]]=int(item[1][:-1])
        return dict_stem
    
    def getListDocs(self):
        if ( self.docsPositionIndex == None):
            self.docsPositionIndex = load_obj(self.docsPositionIndex_File)
        return self.docsPositionIndex.keys()
    
    def getListStems(self):
        
        if ( self.stemsPositionIndexInv == None):
            self.stemsPositionIndexInv = load_obj(self.stemsPositionIndexInv_File)
        return stemsPositionIndexInv.keys()
        
    def getLengthDocs(self):
            return load_obj('index/' + self.name + '_lengthDocs')     