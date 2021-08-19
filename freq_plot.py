#%%
import numpy as np
from control.matlab import *
from control import nyquist_plot
import matplotlib.pyplot as plt
from lima_controle import *

# Definições
G = tf([2,2],[1,10,25])
H = tf([1],[1,2,10])
L = tf([2,-2],[1,0,-4])

w1 = 0.1
w2 = 10000
step = 100000
w = np.linspace(w1,w2,step)

# %%
lima_zpk(G)
lima_zpk(H)
lima_zpk(L)

# %%
K = np.array(range(1,5))
# lim_x = np.array([-0.075,K[-1]*0.2+0.1])
lima_nyquist(G,w,K)

# %%
# # Diagramas de Bode
# plt.figure(1)
# bode(G,w)
# mag = bode(H,w,color='red')
# plt.legend(['G(s)','H(s)'])

# dB = 20*np.log10(mag[0])

# # Diagramas de Nyquist
# plt.figure(2)
# nyquist_plot(G,w,arrowhead_width=0.005,arrowhead_length=0.008)
# nyquist_plot(H,w,color='red',arrowhead_width=0.005,arrowhead_length=0.008)

# plt.xlim(-0.075,0.25)
# plt.grid()
# plt.legend(['G(s)','_','_','H(s)'])
# plt.xlabel('Real')
# plt.ylabel('Imaginário')
# plt.title('Diagrama de Nyquist')

