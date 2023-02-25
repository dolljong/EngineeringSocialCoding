#import json

class CulvertDims:
    #__spanlist = []
    def __init__(self,nspan=1,lwallt=0.3,rwallt=0.3,tslabt=0.3,bslabt=0.3):
        """
        Culvert Dimensions

        :param nspan : number of span
        :param lwallt : thickness of left wall (m)
        :param rwallt : thickness of right wall (m)
        :param tslabt : thickness of top slab (m)
        :param bslabt : thickness of bottom slab (m) 
        """
        self.nspan = nspan
        self.lwallt = lwallt
        self.rwallt = rwallt
        self.tslabt = tslabt
        self.bslabt = bslabt
        self.__spanlist = []
        self.mwalltlist = []

    def set_spanlist(self,spanlist):
        self.__spanlist=spanlist
        self.nspan=len(spanlist)    

    def get_spanlist(self):
        #self.spanlist=spanlist
        #self.nspan=len(spanlist)
        return self.__spanlist   
    
    
if __name__=="__main__":

    clv1dims = CulvertDims(nspan=2)
    clv1dims.__spanlist = [4.5,4.5]
    #clv1dims.set_spanlist=[4.5,4.5]
    clv1dims.mwalltlist =[]
    #clv1dims._spanlist = [5]
    print(clv1dims.nspan)
    print(clv1dims.__spanlist)
    
    
    #print(json.dumps(clv1dims.__dict__))


    # print(proj1.client)
    # print(proj1.engfirm)
    # print(proj1.sitename)
    # print(proj1.contractor)
