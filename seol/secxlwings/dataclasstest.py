from dataclasses import dataclass

@dataclass
class MatData:
    fck : int
    fy : int

culvert_mat = MatData(30,400)


@dataclass
class MatFacData:
    pic : float
    pis : float

culvert_mat = MatData(30,400)
culvert_mat_fac = MatFacData(0.65,0.7)


print(f"fck:{culvert_mat.fck} fy:{culvert_mat.fy} \
pic:{culvert_mat_fac.pic} pis:{culvert_mat_fac.pis}")

print(culvert_mat, culvert_mat_fac)


