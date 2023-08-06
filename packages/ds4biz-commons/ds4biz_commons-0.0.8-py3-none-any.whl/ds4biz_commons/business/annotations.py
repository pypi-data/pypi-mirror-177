class TypeAnn:
    def __init__(self,type,description):
        self.type = type
        self.description = description
    
    def __str__(self):
        return "%s: %s"%(self.type,self.description)
