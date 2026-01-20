import json

from CulvertDims import * 
from materials import *
from projinfo import *

projinfo = ProjectInfo(projname="ESC Bridge")
conc40 = ConcMaterial(30)
clv1dims = CulvertDims(nspan=2,clearanceb=2.5, clearanceh=2.5,
                 lwallt=0.3, mwallt=0.3, rwallt=0.3, tslabt=0.3,bslabt=0.3,
                 soildepth=3,watertable=1.0)

clv1dims.__spanlist= [4.5]
print(clv1dims.__spanlist)

print(json.dumps(projinfo.__dict__))
print(json.dumps(conc40.__dict__))
print(json.dumps(clv1dims.__dict__))

