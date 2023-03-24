import json

class CulvertDims:
    #__spanlist = []
    def __init__(self,nspan:int,clearanceb, clearanceh,
                 lwallt, mwallt, rwallt, tslabt,bslabt,
                 soildepth,watertable):
        """
        Culvert Dimensions
        
        :param nspan : number of span
        :param clearanceb : clearance width (m)
        :param clearanceh : clearance height (m)
        :param lwallt : thickness of left wall (m)
        :param mwallt : thickness of middle wall (m)
        :param rwallt : thickness of right wall (m)
        :param tslabt : thickness of top slab (m)
        :param bslabt : thickness of bottom slab (m) 
        :param soildepth : depth of soil from slab top to surface
        :param watertable : water table from surface
        """
        self.nspan = nspan
        self.clearanceb=clearanceb
        self.clearanceh=clearanceh
        self.lwallt = lwallt
        self.rwallt = rwallt
        self.tslabt = tslabt
        self.bslabt = bslabt
        self.soildepth = soildepth
        self.watertable = watertable
        #self.__spanlist = []
        self.mwallt= mwallt
        self.totalb = self.nspan*self.clearanceb + \
                    (self.nspan-1) * self.mwallt + self.lwallt + self.rwallt
        self.totalh = clearanceh + tslabt + bslabt

    def set_spanlist(self,spanlist):
        self.__spanlist=spanlist
        self.nspan=len(spanlist)    

    def get_spanlist(self):
        #self.spanlist=spanlist
        #self.nspan=len(spanlist)
        return self.__spanlist   
    
    
if __name__=="__main__":

    clv1dims = CulvertDims(nspan=2,clearanceb=4.5,clearanceh=4.5,
                           lwallt=0.4, mwallt=0.4, rwallt=0.4,tslabt=0.45,bslabt=0.45,
                           watertable=2,soildepth=3)
    clv1dims.__spanlist = [4.5,4.5]
    #clv1dims.set_spanlist=[4.5,4.5]
    #clv1dims.mwallt =[]
    #clv1dims._spanlist = [5]
    print(clv1dims.nspan)
    print(clv1dims.__spanlist)
    
    
    print(json.dumps(clv1dims.__dict__))


    # print(proj1.client)
    # print(proj1.engfirm)
    # print(proj1.sitename)
    # print(proj1.contractor)
