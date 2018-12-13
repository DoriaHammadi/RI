
class IRList():
    
    def __init__(self, query, model):

        self.query = query
        self.model = model

    def getQuery(self): 
        
        #print(self.query.get_revelant())
        return self.query
    
    def getRanking(self): 
        res = self.model.getRanking(self.query.get_query())
        if (type(res[0]) == str):
            docs = res
        else :
            docs = [tuple_[0] for tuple_ in res]
            
        return res