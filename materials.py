from math import sin, pi
import pandas as pd

class ConcMaterial:
    '''
      concrete material class
    '''
    def __init__(self, f_ck:float, m_c:float=2300):
        '''
        initialize instance 
        :param f_ck : f_ck of concrete (MPa)
        :param m_c : unit weight of concrete(kg/m3) default:2300
        '''
        self.f_ck = f_ck
        self.m_c = m_c
        self.f_cm = self.calc_f_cm(f_ck)
        self.E_c = self.calc_E_c(f_ck, m_c)["val"]
        self.E_c_latex = self.calc_E_c(f_ck, m_c)["latex"]
        
    def calc_E_c(self,f_ck,m_c):
        if m_c == 2300:
            val = 8500 * self.calc_f_cm(f_ck) ** (1.0/3.0)
            return { "val" :  val,
                    "latex" : f"$E_{{c}}=8500 \\times \\root {{3}} \\of {{f_{{cm}} }}  " + 
                    f"= 8500 \\times \\root {{3}} \\of {{ {self.calc_f_cm(f_ck)} }} = {val} \\; \\mathrm{{MPa}}$"}
        val = 0.077 * m_c ** (1.5) * self.calc_f_cm(f_ck) ** (1.0/3.0)
        return {"val" : val ,
                "latex" : f"0.077 \\times {m_c} ^ (1.5) \\times {self.calc_f_cm(f_ck)} ^ {1.0/3.0} = {val} \\; \\mathrm{{MPa}}$"}
        
    def calc_f_cm(self,f_ck):
        deltaf = (f_ck - 40)*2.0/20
        if f_ck <= 40 :
            deltaf = 4.0
        if f_ck >= 60 :
            deltaf = 6.0    
        return f_ck + deltaf
        
    def __str__(self):
        return f"f_ck = {self.f_ck}, f_cm = {self.f_cm}, E_c = {self.E_c}"
        
    def latex(self):
        #latex_fck = f"$$f_ck = {self.f_ck}$$"
        latex_fck = f"f_{{ck}} = {self.f_ck} \\; \\mathrm{{MPa}}  "
        latex_f_cm = f"f_{{cm}} = {self.f_cm} \\; \\mathrm{{MPa}}  "
        latex_E_c = f"E_{{c}} = {self.E_c} \\; \\mathrm{{MPa}}"
        return "$" + latex_fck + "\\\\" + latex_f_cm + "\\\\" + latex_E_c + "$"
        #return latex_fck + latex_f_cm + latex_E_c
          
                
class RebarMaterial:
    def __init__(self,f_y):
        self.f_y = f_y
        self.E_s = 200000
        
    def __str__(self):
        return f"f_y = {self.f_y}, E_s = {self.E_s}"

class TendonMaterial:
    def __init__(self,f_y):
        self.E_ps = 200000
        
    def __str__(self):
        return f"E_ps = {self.E_ps}"
    
class SoilMaterial:
    def __init__(self,gamma_t,phi):
        """
        Args:
            gamma_t (float) : unit weight (total) of soil (kN/m3)
            phi (float) : angle of internal friction (degree)

        Attributes:
            gamma_sub (float) : unit weight (submerged) of soil (kN/m3)
            phirad (float) : phi radian (radian)
            coef_epressa (float) : ka earth pressure coefficient (active)
            coef_epressp (float) : kp earth pressure coefficient (passive)
            coef_epresso (float) : ko earth pressure coefficient (at rest)

        """
        self.gamma_t = gamma_t
        self.phi = phi
        self.phirad = phi / 180 * pi
        self.gamma_sub = gamma_t - 10.0
        self.coef_epressa = (1-sin(self.phirad))/(1+sin(self.phirad)) 
        self.coef_epressp = (1+sin(self.phirad))/(1-sin(self.phirad)) 
        self.coef_epresso = 1 - sin(self.phirad)
        self.coef_epressa_txt = f"ka = (1 - sin({self.phi})) / (1 + sin({self.phi})) = {self.coef_epressa}"
        self.coef_epressp_txt = f"kp = (1 + sin({self.phi})) / (1 - sin({self.phi})) = {self.coef_epressp}"
        self.coef_epresso_txt = f"ko = 1 - sin({self.phi}) = {self.coef_epresso}"

class SteelMaterial:
    """
    Steel Material : KDS 143105 Table 3.4-1
    """
    def __init__(self,steelgrade: str, thick: int):
        steelgrades_1    =["SS235","SS275","SM275","SMA275","SS315","SM355","SMA355","SS410","SM420","SS450","SM460","SMA460","SS550"]
        Fylist_1_16mm    =[    235,    275,    275,     275,    315,    355,     355,    410,    420,    450,    460,     460,    550]
        Fylist_1_16_40mm =[    225,    265,    265,     265,    305,    345,     345,    400,    410,    440,    450,     450,    540]
        Fylist_1_40_75mm =[    205,    245,    255,     255,    295,    335,     335,    None,   400,   None,    430,     430,   None]
        Fylist_1_75_100mm =[    205,    245,    245,     245,    295,    325,     325,   None,   390,   None,    420,     420,   None]
        Fylist_1_100mm    =[    195,    235,    235,     235,    275,    305,     305,   None,   380,   None,   None,    None,   None]
        Fulist_1          =[    330,    410,    410,     410,    490,    490,     490,    540,   520,    590,    570,     570,    690]  

        steelgrades_2 =["HSB380","HSM500","HSB460","HSB690","HSA650","SM275-TMC","SM355-TMC","SM420-TMC","SM460-TMC"]
        Fylist_2_100mm  =[   380,     380,     460,     690,     650,        275,        355,        420,        460]
        Fulist_2        =[   500,     500,     600,     800,     800,        410,        490,        520,        570]

        steelgrades_3 =["SN275","SN355","SN460","SHN275","SHN355","SHN420","SHN460"]
        Fylist_3_40mm     =[   275,     355,    460,     275,     355,     420,     460]
        Fylist_3_40_100mm =[   255,     335,    440,     275,     355,     420,     460]
        Fulist_3          =[   410,     490,    570,     410,     490,     520,     570]

        df1 = pd.DataFrame([Fylist_1_16mm],columns=steelgrades_1)
        df1.loc[len(df1.index)] = Fylist_1_16_40mm
        df1.loc[len(df1.index)] = Fylist_1_40_75mm
        df1.loc[len(df1.index)] = Fylist_1_75_100mm
        df1.loc[len(df1.index)] = Fylist_1_100mm
        df1.loc[len(df1.index)] = Fulist_1

        df2=pd.DataFrame([Fylist_2_100mm],columns=steelgrades_2)
        df2.loc[len(df2.index)] = Fulist_2

        df3=pd.DataFrame([Fylist_3_40mm],columns=steelgrades_3)
        df3.loc[len(df3.index)] = Fylist_3_40_100mm
        df3.loc[len(df3.index)] = Fulist_3

        self.steel_mat_table1=df1
        self.steel_mat_table2=df2
        self.steel_mat_table3=df3

        if steelgrade in steelgrades_1:
            #print("grade1")
            if thick <= 16:
                thickindex = 0
            elif thick > 16 and thick < 40:
                thickindex = 1
            elif thick > 40 and thick < 75:
                thickindex = 2
            elif thick > 75 and thick < 100:
                thickindex = 3
            else:
                thickindex = 4
            self.F_y = df1.loc[thickindex,steelgrade]
            self.F_u = df1.loc[5,steelgrade]
        elif steelgrade in steelgrades_2:
            #print("grade2")
            self.F_y = df2.loc[0,steelgrade]
            self.F_u = df2.loc[1,steelgrade]
        else:
            #print("grade3")
            if thick > 6 and thick <= 40:
                thickindex = 0
            elif thick > 40 and thick < 100:
                thickindex = 1
            #print(f"thickindex:{thickindex}")
            self.F_y = df3.loc[thickindex,steelgrade]
            self.F_u = df3.loc[2,steelgrade]
            
        #self.F_y = 0
        #self.F_u = 0

class PipeMaterial:
    """
    Steel Pipe Material : KDS 143105 3.4-2
    """
    def __init__(self, pipegrade: str, thick: int):
        pipegrades_1    =["SGT275","SRT275","STP275","SGT355","SRT355","STP355","SGT410","SRT410","STP380","STKM500","SGT450","SRT450","STP450"]
        Fylist_1        =[     275,     275,     275,     355,     355,     355,     410,     410,     380,      380,    450,     450,      450]
        Fulist_1        =[     410,     410,     410,     500,     500,     500,     540,     540,     500,      500,    590,     590,      590]
        pipegrades_1   +=["SGT550","SRT550","STP550","SHT410","SHT460","SKY400","SKY490"]
        Fylist_1       +=[     550,     550,     550,     410,     460,     235,     315]
        Fulist_1       +=[     690,     690,     690,     550,     590,     400,     490]     

        pipegrades_2      =["SNT275E","SNT275A","SNT355E","SNT355A","SNT460E","SNT460A","SNRT295E","SNRT360E","SNRT275A","SNRT355A"]
        Fylist_2_40mm     =[     275,      275,      355,      355,      460,      460,       295,      360,       275,      355]
        Fylist_2_40_100mm =[     255,      255,      335,      335,      440,      440,      None,     None,      None,     None]
        Fulist_2          =[     410,      410,      490,      490,      570,      570,       410,      490,       410,      490]


        df1 = pd.DataFrame([Fylist_1],columns=pipegrades_1)
        df1.loc[len(df1.index)] = Fulist_1

        df2=pd.DataFrame([Fylist_2_40mm],columns=pipegrades_2)
        df2.loc[len(df2.index)] = Fylist_2_40_100mm
        df2.loc[len(df2.index)] = Fulist_2

        self.pipe_mat_table1 = df1
        self.pipe_mat_table2 = df2

        if pipegrade in pipegrades_1:
            #print("grade1")
            self.F_y = df1.loc[0,pipegrade]
            self.F_u = df1.loc[1,pipegrade]
        else:
            #print("grade3")
            if thick <= 40:
                thickindex = 0
            elif thick > 40 and thick < 100:
                thickindex = 1
            #print(f"thickindex:{thickindex}")
            self.F_y = df2.loc[thickindex,pipegrade]
            self.F_u = df2.loc[2,pipegrade]

class BoltMaterial:
    """
    Bolt Material : KDS 143105 3.4-4
    """    
if __name__=="__main__":

    conc30 = ConcMaterial(f_ck=30)

    print(conc30.f_ck, conc30.E_c, conc30.f_cm)

    print(conc30.calc_E_c(40, 2300))
    print(conc30.calc_f_cm(40))

    conc40 = ConcMaterial(f_ck=40, m_c=2400)
    print(conc40.f_ck, conc40.E_c, conc40.f_cm)
    
    print(conc40.E_c_latex)

    conc45 = ConcMaterial(f_ck=45, m_c=2400)
    print(conc45.f_ck, conc45.E_c, conc45.f_cm)

    print(conc30)
    print(conc40)
    print(conc45)

    print(conc30.latex())

    soil30 = SoilMaterial(gamma_t=20, phi=30)
    print(soil30.__dict__)

    steelmat1= SteelMaterial(steelgrade="SM275",thick=10)
    print(f"Fy:{steelmat1.F_y:.0f} Fu:{steelmat1.F_u:.0f}")

    pipemat1= PipeMaterial(pipegrade="SGT355",thick=10)
    print(f"Fy:{pipemat1.F_y:.0f} Fu:{pipemat1.F_u:.0f}")