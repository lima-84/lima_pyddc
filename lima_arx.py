#%%
import numpy as np
from numpy.linalg import inv, pinv
from control.matlab import *

def lima_arx(y1,y2,u,nze,npo,nk,Ts):

    # Defining input delayed vector
    u_d = np.zeros([len(u), nze+1])
    for i in range(0, nze+1):
        u_d[i+nk:, i] = u[:-(i+nk)]

    # Defining output delayed vectors
    y1_d = np.zeros([len(y1), npo])
    y2_d = np.zeros([len(y2), npo])
    for i in range(0, npo):
        y1_d[i+1:, i] = y1[:-(i+1)]
        y2_d[i+1:, i] = y2[:-(i+1)]

    # Least squares
    phi = np.concatenate((u_d, y1_d), axis = 1)
    zeta = np.concatenate((u_d, y2_d), axis = 1)
    theta = inv(zeta.T@phi)@(zeta.T@y1)

    # Defining identified transfer function
    num = theta[:nze+1].T
    den = np.concatenate(([1],theta[nze+1:].T))
    G = tf(num,den,Ts)

    return G, theta

Ts = 1
t = np.arange(1,50)
u = np.ones(len(t))

z = tf('z')
z.dt = Ts
G = 0.5*z/(z-0.9)/(z-0.8)

y = lsim(G,u)[0]

G = lima_arx(y,y,u,1,2,1,Ts)[0]
# %%
