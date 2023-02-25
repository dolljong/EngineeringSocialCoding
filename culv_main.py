import json

from CulvertDims import * 
from Materials import *
from ProjInfo import *

projinfo = ProjectInfo(projname="ESC Bridge")
conc40 = ConcMaterial(30)
clv1dims = CulvertDims(nspan=1)

clv1dims.__spanlist= [4.5]
print(clv1dims.__spanlist)

print(json.dumps(clv1dims.__dict__))