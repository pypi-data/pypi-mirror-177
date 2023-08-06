""" Provide time domain window functions. 
"""

import numpy as np
from scipy import signal

def window(tm, xl=1000.0, kap=0.005, show=False):
    """Return time domain window function to remove the first and last xl
    sec. 
    """
    ind_r = np.argwhere(tm[-1]-tm <= xl)[0][0]
    xr = tm[ind_r]
    winl = 0.5*(1.0 + np.tanh(kap*(tm-xl)))
    winr = 0.5*(1.0 - np.tanh(kap*(tm-xr)))
    if show:
        import matplotlib.pyplot as plt
        plt.plot(tm, winl)
        plt.plot(tm, winr)
        plt.grid(True)
        plt.show()
    return (winl*winr)

def tukey(N, alpha):
    """ Return time domain window function of size N. 
    """
    # alpha -- parameter the defines the shape of the window
    w         = np.zeros(N, dtype=float)
    i         = np.arange(0,N,1)
    r         = (2.0*i)/(alpha*(N-1))
    l1        = int(np.rint((alpha*(N-1))/2.0))
    l2        = int(np.rint((N-1)*(1.0-alpha/2.0)))
    w[0:l1]   = 0.5*(1.0 + np.cos(np.pi*(r[0:l1] - 1.0)))
    w[l1:l2]  = 1.0
    w[l2:N-1] = 0.5*(1+np.cos(np.pi*(r[l2:N-1] - 2.0/alpha + 1.0)))
    return w

def butter_lowpass_filter(data, cutoff, fs, order=4, show=False):
    """ Return low pass filtered data
    """
    #nyq = 0.5 * fs  # Nyquist Frequency
    #normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = signal.butter(order, cutoff, btype='low', analog=False)
    y = signal.filtfilt(b, a, data)

    if show:
        import matplotlib.pyplot as plt
        w, h = signal.freqz(b, a)
        plt.figure()
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    return y


def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low, high = lowcut / nyq, highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    y = signal.filtfilt(b, a, data)
    return y
