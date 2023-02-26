from Materials import SoilMaterial
#

def earthpressure(gamma_t:float,phi:float,waterz:float,z:float,eptype:str) -> float: 
    """
    Args:
        gamma_t (float) : unit weight (total) of soil (kN/m3)
        phi (float) : angle of internal friction (degree)
        waterz (float) : water table from surface (m)
        z (float) : z from surface (m)
        eptype (str) : "a" / "p" / "o"

    Returns:
        epressure : earth pressure (kN/m2)

    """
    soilm = SoilMaterial(gamma_t,phi)
    if eptype == "a":
        coef_epressure = soilm.coef_epressa
        txt = soilm.coef_epressa_txt
    elif eptype == "p":
        coef_epressure =  soilm.coef_epressp
        txt = soilm.coef_epressp_txt
    elif eptype == "o":
        coef_epressure =  soilm.coef_epresso
        txt = soilm.coef_epresso_txt
    
    return {"val": coef_epressure , "txt": txt}

if __name__=="__main__":
    coefep = earthpressure(gamma_t=20,phi=30,waterz=1.0,z=5.0,eptype="o")
    print(coefep["val"],coefep["txt"])
    
    