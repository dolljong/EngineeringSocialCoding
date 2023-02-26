import json
import inspect

from Materials import *
from ProjInfo import *

projinfo = ProjectInfo("ESC bridge","Seoul city","Eng E&C","Hangang","Han Construction")
conc30 = ConcMaterial(f_ck=30, m_c=2300)

datadict = { "projinfo": projinfo.__dict__, "conc30" : conc30.__dict__}
dataobj = {"projinfo": projinfo, "conc30" : conc30}

print(datadict)

print(datadict["projinfo"]["client"])
print(dataobj["projinfo"].client)

json1 = json.dumps(datadict)



proji1 =  ProjectInfo(**datadict["projinfo"])
print(proji1.__dict__)

args = inspect.getfullargspec(ConcMaterial.__init__).args[1:]
print(args)
conc301 =  ConcMaterial(**{a:datadict["conc30"][a] for a in args})
print(conc301.__dict__)
# conc30에는 다른 __dict__가 있기 때문에 그대로 instance로 만들수가 없다. 없는 key가 있다.
# 따라서 __init__의 argument에 해당하는 key:value만 전달해야 한다.
