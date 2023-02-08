class ConcMaterial:
    def __init__(self, f_ck, m_c=2300):
        self.f_ck = f_ck
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

