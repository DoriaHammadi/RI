
class IRList():
    
    def __init__(self, query, model):

        self.query = query
        self.model = model

    def getQuery(self): 
        
        #print(self.query.get_revelant())
        return self.query
    
    def getRanking(self): 
        
        res = self.model.getRanking(self.query.get_query(), 0.001)
        return list(res.items())