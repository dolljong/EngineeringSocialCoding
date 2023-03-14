
from math import pi
class SectionRect:
    """
    Section property of Rectangle
    """
    def __init__(self,B : float, H : float):
        self.A = B*H
        self.Ixx = B*H**3/12.0
        self.Iyy = H*B**3/12.0

class SectionCircle:
    """
    Section property of Circle
    """
    def __init__(self,D : float):
        self.A = pi*D**2/4.0
        self.Ixx = pi*D**4/64.0
        self.Iyy = self.Ixx

class SectionIGirder:
    """
    Section property of HBeam
    """
    def __init__(self,B : float,H : float, tw : float, tf : float):
        self.A = B*H - (B-tw)*(H-2*tf)
        self.Ixx = B*H**3/12.0 - (B-tw)*(H-2*tf)**3/12.0
        self.Iyy = 2*tf*B**3/12.0 + (H-2*tf)*tw**3/12.0


if __name__ == "__main__":
    B=1.0
    H=0.35
    rect1 = SectionRect(B=B,H=H)
    print(f"B:{B} H:{H}  A={rect1.A} Ixx={rect1.Ixx} Iyy={rect1.Iyy}")

    D=1.0
    cir1 = SectionCircle(D=D)
    print(f"D:{D}  A={cir1.A} Ixx={cir1.Ixx} Iyy={cir1.Iyy}")

    B=0.8
    H=1.2
    tf=0.016
    tw=0.010
    igirder = SectionIGirder(B=B,H=H,tf=tf,tw=tw)
    print(f"B:{B} H:{H} tw:{tw} tf:{tf} A={igirder.A} Ixx={igirder.Ixx} Iyy={igirder.Iyy}")    