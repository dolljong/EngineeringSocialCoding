import numpy as np
import matplotlib.pyplot as plt

#%% Input truss structure data
E = 1e4
A = 0.111

nodes = []
bars = []

nodes.append([0,120])
nodes.append([120,120])
nodes.append([240,120])
nodes.append([360,120])
nodes.append([0,0])
nodes.append([0,120])
nodes.append([0,240])
nodes.append([0,360])

bars.append([0,1])
bars.append([1,2])
bars.append([2,3])
bars.append([4,5])
bars.append([5,6])
bars.append([6,7])

bars.append([5,1])
bars.append([6,2])
bars.append([7,3])

bars.append([0,5])
bars.append([4,1])
bars.append([1,6])
bars.append([5,2])
bars.append([2,7])
bars.append([6,3])

nodes = np.array(nodes).astype(float)
bars = np.array(bars)

#Applied forces
P = np.zeros_like(nodes)
P[7,1]=-10

#Support Displacement
Ur = [0,0,0,0]

#Condition of DOF (1 = free, 0 = fixed)
DOFCON = np.ones_like(nodes).astype(int)
DOFCON[0,:] = 0
DOFCON[4,:] = 0

#%% Truss structural analysis
def TrussAnalysis():
    NN = len(nodes)
    NE = len(bars)
    DOF = 2
    NDOF = DOF*NN

    #structural analysis
    d = nodes[bars[:,1],:] - nodes[bars[:,0],:]
    L = np.sqrt((d**2).sum(axis=1))
    angle = d/L
    print(angle)

TrussAnalysis()
