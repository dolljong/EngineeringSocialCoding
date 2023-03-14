from Materials import SoilMaterial
from enum import Enum, auto

class EarthPressureType(Enum):
    """
    type of earth pressure
    ACTIVE / PASSIVE / ATREST
    """
    ACTIVE = auto()
    PASSIVE = auto()
    ATREST = auto()

def earthpressure(gamma_t:float,phi:float,waterz:float,z:float,eptype:EarthPressureType) -> float: 
    """
    Args:
        gamma_t (float) : unit weight (total) of soil (kN/m3)
        phi (float) : angle of internal friction (degree)
        waterz (float) : water table from surface (m) 1.0
        z (float) : z from surface (m) ex) 3.0
        eptype (EarthPressureType) : ACTIVE / PASSIVE / ATREST

    Returns:
        { "val" : epressure, "txt" : txt}
        epressure : earth pressure (kN/m2) : float
        txt : equation : str

    """


    soilm = SoilMaterial(gamma_t,phi)
    txt = ""
    if eptype == EarthPressureType.ACTIVE:
        coef_epressure = soilm.coef_epressa
        #txt = soilm.coef_epressa_txt
    elif eptype == EarthPressureType.PASSIVE:
        coef_epressure =  soilm.coef_epressp
        #txt = soilm.coef_epressp_txt
    elif eptype == EarthPressureType.ATREST:
        coef_epressure =  soilm.coef_epresso
        #txt = soilm.coef_epresso_txt
    gamma_sub = gamma_t - 10.0
    if z <= waterz:
        epressure = coef_epressure * gamma_t * z
        txt += f"p = {coef_epressure:.3f} * {gamma_t:.3f} * {z:.3f}= {epressure:.3f}" 
    else:
        epressure = coef_epressure * (gamma_t*waterz + gamma_sub*(z-waterz))
        #txt += f"\n"
        txt += f"p = {coef_epressure:.3f} * ({gamma_t:.3f} * {waterz:.3f}"
        txt += f"+{gamma_sub:.3f}*({z:0.3f} - {waterz:.3f})) = {epressure:.3f}"
        
    return {"val": epressure , "txt": txt}


def surface_live(D : float, B_o : float ):
    """
    노면활하중(kN/m2) KDS 291400 table 4.1-4, table 4.1-5
    param : D : depth (m)
    param : B_o : width of span (m)
    return 
    """
    surflive_table1={1.0: 39.0, 1.5:25.0, 2.0:18.0, 2.5:14.0, 3.0:11.0, 3.5:10.0}
    surflive_table2={0.1: 17.0, 0.2:27.0 , 0.3:33.0, 0.4:36.0}
    DoverB_o = D /B_o
    if DoverB_o >= 0.5:
        if D >= 3.5: 
            p_v1 = 10.0
        else:
            p_v1=surflive_table1[int(D/0.5)*0.5]     
    else:
        if DoverB_o >=0.4:
            p_v1=36.0/D
        else:
            p_v1=surflive_table2[round(int(DoverB_o/0.1)*0.1,1)]/D
    return p_v1


if __name__=="__main__":
    earthmat = SoilMaterial(gamma_t=20, phi=30)
    
    epress = earthpressure(gamma_t=20, phi=30, waterz=1.0, z=5.0, 
                           eptype=EarthPressureType.ATREST)
    print(epress["val"])
    print(epress["txt"])
    epressvdic={}
    epresstxtdic={}
    print(earthmat.coef_epresso_txt)
    for iz in [1.0,1.5,3.0,4.0,5.0]:
        epress = earthpressure(gamma_t=20, phi=30, waterz=1.0, z=iz, 
                           eptype=EarthPressureType.ATREST)
        epressvdic[iz] = epress["val"]
        epresstxtdic[iz] = epress["txt"]
        print(epress["txt"])

    print(epresstxtdic)

    print(surface_live(D=3.0, B_o=3.0))
    print(surface_live(D=1.0, B_o=3.0))

        

         
    
    