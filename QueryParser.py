from Document import Document
import porter
import TextRepresenter
from Parser import Parser
import pickle

class Query():
    def __init__(self, id, text, revelant, porter): #, pertinance, sousclasse):
        """id : id Query(Int)
            revelant : (IdDoc,(pertinence, idSubtopic) (Int(Int,Int))
        """
        self.id = id
        self.text = text
        self.revelant = revelant
        self.query = porter.getTextRepresentation(text)
        #self.pertinance = pertinance
        #self.sousclasse = sousclasse

    def get_id(self): return self.id
    def get_text(self): return self.text
    def get_revelant(self): return self.revelant
    def get_query(self): return self.query
    
class QueryParser(Parser):
    
    def __init__(self, porter):

        Parser.__init__(self,".I")
        self.porter = porter
        
    def initQry(self, qry) :
        self.qry = qry
        self.initFile(qry)

    def initRel(self, rel) :
        self.rel = rel

    def nextQuery(self):
                
        qry = self.nextDocument()
        rel = []
        if qry == None:
            return None
                   
        file = open(self.rel, 'r')

        line = file.readline()
        line = line.replace('  ',' ')

        while(line):
            l = line.split(' ')
            try :
                if (int(l[0]) == int(qry.getId())) :
                    rel.append((l[1],(int(l[2]),int(l[3]))))
            except  ValueError:
                ...
            line = file.readline()
            line = line.replace('  ',' ')

        res = Query(qry.getId(),qry.getText(),rel, self.porter)

        return res
    def getDocument(self, text):

        other={};
        modeT=False;
        modeA=False;
        modeK=False;
        modeW=False;
        modeX=False;
        info=""
        identifier=""
        author=""
        kw=""
        links=""
        title=""
        texte=""

        st=text.split("\n");
        s=""
        for s in st:
            if(s.startswith(".I")):
                identifier=s[3:]
                continue

            if(s.startswith(".")):
                if(modeW):
                    texte=info
                    info=""
                    modeW=False

                if(modeA):
                    author=info
                    info=""
                    modeA=False

                if(modeK):
                    kw=info;
                    info="";
                    modeK=False;

                if(modeT):
                    title=info;
                    info="";
                    modeT=False

                if(modeX):
                    other["links"]=links;
                    info="";
                    modeX=False;



            if(s.startswith(".W")):
                modeW=True;
                info=s[2:];
                continue;

            if(s.startswith(".A")):
                modeA=True;
                info=s[2:];
                continue;

            if(s.startswith(".K")):
                modeK=True;
                info=s[2:];
                continue;

            if(s.startswith(".T")):
                modeT=True;
                info=s[2:];
                continue;

            if(s.startswith(".X")):
                modeX=True
                continue;

            if(modeX):
                l=s.split("\t");
                if(l[0]!=identifier):
                    if(len(l[0])>0):
                        links+=l[0]+";";

                continue;

            if((modeK) or (modeW) or (modeA) or (modeT)):
                #print "add "+s
                info+=" "+s



        if(modeW):
            texte=info;
            info="";
            modeW=False;

        if(modeA):
            author=info;
            info="";
            modeA=False;

        if(modeK):
            kw=info;
            info="";
            modeK=False;

        if(modeX):
            other["links"]=links;
            info=""
            modeX=False;

        if(modeT):
            title=info;
            info="";
            modeT=False;

        other["title"]=title
        other["text"]=texte
        other["author"]=author
        other["keywords"]=kw

        doc=Document(identifier,title+" \n "+author+" \n "+kw+" \n "+texte,other);

        return doc
