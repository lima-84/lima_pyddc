#%%
import numpy as np
from control.matlab import *
from numpy.linalg import inv, pinv

def lima_vrft(y1,y2,u,Td,C_bar,L,nk):

    z = tf('z')
    z.dt = Td.dt

    # Filtering input and output signals
    u_L = lsim(L,u)[0]
    y2_L = lsim(L,y1)[0]
    y1_L = lsim(L,y2)[0]

    # Computing virtual errors
    e1 = lsim((1-Td)/(z**(1+nk)*Td),y1_L)[0]
    e1 = e1[1+nk:]

    e2 = lsim((1-Td)/(z**(1+nk)*Td),y2_L)[0]
    e2 = e2[1+nk:]

    # Defining regressor vectors (NOT FUNCTIONAL YET)
    phi = lsim(C_bar,e1)[0]
    zeta = lsim(C_bar,e2)[0]

    # Least squares
    p = inv(zeta.T@phi)@(zeta.T@u_L)
    C = (p.T)*C_bar

    return C,p

Ts = 1
t = np.arange(1,50)
u = np.ones(t.shape[0])

z = tf('z')
z.dt = Ts
G = 0.5/(z-0.9)

y = lsim(G,u)[0]

Td = 0.2/(z-0.8)
L = Td*(1-Td)

C_bar = np.array([z,1])/(z-1)

C, p = lima_vrft(y,y,u,Td,C_bar,L,0)
# %%
