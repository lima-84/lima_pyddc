from control.freqplot import nyquist_plot
from control.matlab.wrappers import dcgain
import numpy as np
from control.lti import zero, pole
import matplotlib.pyplot as plt
import warnings
from IPython.display import display, Math, Latex

def lima_zpk(sys):

    sys_poles = pole(sys)
    sys_zeros = zero(sys)

    sys_gain = dcgain(sys) / ( np.prod(-sys_zeros)/np.prod(-sys_poles) )
    sys_gain = np.real(sys_gain)

    str_poles = ''
    str_zeros = ''

    for p in sys_poles:
        str_poles = str_poles + '(s + ' + "{:.2f}".format(-p) + ')'
        
    for z in sys_zeros:
        str_zeros = str_zeros + '(s + ' + "{:.2f}".format(-z) + ')'

    display(Math(r'\frac{' + "{:.2f}".format(sys_gain) + str_zeros + '}{' \
         + str_poles + '}'))

# Plots Nyquist Diagrams for the family of transfer functions gain_range*sys

def lima_nyquist(sys,freq,gain_range,lim_x):
    plt.figure(1)    
    plt.grid()
    leg = []
    for gain in gain_range:
        nyquist_plot(gain*sys,freq,arrowhead_width=0.005,arrowhead_length=0.008)
        leg.extend(['K = ' + str(gain),'_','_'])
    
    plt.xlim(lim_x)
    warnings.filterwarnings("ignore")
    plt.legend(leg)    
    warnings.filterwarnings("default")
    plt.xlabel('Real')
    plt.ylabel('Imaginário')
    plt.title('Diagrama de Nyquist')

