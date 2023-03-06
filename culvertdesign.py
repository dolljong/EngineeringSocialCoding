import json
import inspect
import pprint


from Materials import *
from ProjInfo import *

def instance2json(listobj , file_path):
    #file_path = "./test.json"
    dictobj = {i.__class__.__name__ : 
               #i.__dict__
               {k:i.__dict__[k] for k in inspect.getfullargspec(globals()[i.__class__.__name__].__init__).args[1:] if k in i.__dict__} 
               for i in listobj }
    
    for obj in listobj:
        args1 = inspect.getfullargspec(globals()[obj.__class__.__name__].__init__).args[1:]
        dict1 = obj.__dict__
        dictobj[obj.__class__.__name__]={k:dict1[k] for k in args1 if k in dict1}

    print(json.dumps(dictobj,indent=4))

    pretty_print_json = pprint.pformat(dictobj).replace("'", '"')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_print_json)
    

def test_instance2json():
    projinfo = ProjectInfo("ESC bridge","Seoul city","Eng E&C","Hangang","Han Construction")
    conc30 = ConcMaterial(f_ck=30, m_c=2300)
    listobj = [projinfo,conc30]
    instance2json(listobj,"./test.json")

def instance_from_json(file_path):
    with open(file_path) as json_file:
        json_data = json.load(json_file)
    return json_data
    

def main():
    test_instance2json()
    json_data=instance_from_json('./test.json')
    print(json.dumps(json_data,indent=4))
    objs={}
    for i in json_data:
        print(i,json_data[i])
        print(type(json_data[i]))
        arg_data=json_data[i]
        objs[i]=globals()[i](**arg_data)

    print(objs["ConcMaterial"].f_ck)

    exit()
    
    projinfo = ProjectInfo("ESC bridge","Seoul city","Eng E&C","Hangang","Han Construction")
    conc30 = ConcMaterial(f_ck=30, m_c=2300)

    datadict = { projinfo.__class__.__name__: projinfo.__dict__, 
                conc30.__class__.__name__ : conc30.__dict__}
    #dataobj = {"projinfo": projinfo, "conc30" : conc30}

    print(datadict)

    print(datadict["ProjectInfo"]["client"])
    #print(dataobj["projinfo"].client)

    json1 = json.dumps(datadict)
    print("json" , json1)

    file_path = "./test.json"

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(datadict, file)

    proji1 =  ProjectInfo(**datadict["ProjectInfo"])
    print(proji1.__dict__)

    args = inspect.getfullargspec(ConcMaterial.__init__).args[1:]
    print(args)
    conc301 =  ConcMaterial(**{a:datadict["ConcMaterial"][a] for a in args})
    print(conc301.__dict__)
    # conc30에는 다른 __dict__가 있기 때문에 그대로 instance로 만들수가 없다. 없는 key가 있다.
    # 따라서 __init__의 argument에 해당하는 key:value만 전달해야 한다.

if __name__=="__main__":
    main()