#%%
import numpy as np
from numpy.linalg import solve
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
        y1_d[i+1:, i] = -y1[:-(i+1)]
        y2_d[i+1:, i] = -y2[:-(i+1)]

    # Regressor vectors
    phi = np.concatenate((u_d, y1_d), axis = 1)
    zeta = np.concatenate((u_d, y2_d), axis = 1)

    # Removing extra zeros
    xtra = 1 + max(npo, nze+nk)
    phi = phi[xtra:,:]
    zeta = zeta[xtra:,:]
    y1 = y1[xtra:]

    A = zeta.T@phi
    b = zeta.T@y1

    # Least squares
    theta = np.linalg.lstsq(A, b, rcond = None)[0] # np.linalg.lstsq?

    # Defining identified transfer function
    num = np.concatenate((theta[:nze+1].T, np.zeros([npo-nze])))
    den = np.concatenate(([1], theta[nze+1:].T, np.zeros(nk)))
    G = tf(num,den,Ts)

    return G, theta

# Example

import matplotlib.pyplot as plt

Ts = 1
t = np.arange(1,50)
u = np.ones(len(t))
u[0] = 0

z = tf('z')
z.dt = Ts
G = 1/(z-0.9)

nze, npo, nk = 0, 1, 1

y = lsim(G,u)[0]

Gr, theta = lima_arx(y,y,u,nze,npo,nk,Ts)
Gr

yr = lsim(Gr,u)[0]

fig, ax = plt.subplots()
ax.plot(t,u,label='Input data')
ax.plot(t,y, 'k', label='Output data')
ax.plot(t,yr, 'r--',label='Model output')
ax.legend()
# %%
