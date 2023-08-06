from ldc.lisa.noise import get_noise_model
import tdi
import numpy as np
import matplotlib.pyplot as plt


fig, ax1 = plt.subplots()#figsize=(8,7)) 
plt.subplots_adjust(left=0.13, right=0.98, top=0.9, bottom=0.12)

Tobs  = 126230400.0 # secs

f     = np.linspace(1e-4,1e-1,1000)      # The frequency array
sens1 = tdi.lisasens(f, noiseModel='SciRDv1', includewd=None)
sens2 = get_noise_model('SciRDv1', frq=f).sensitivity() # wd=Tobs/LC.year

plt.loglog(f, np.sqrt(f * sens1), 'k-', linewidth=4, label='from ldc1')
plt.loglog(f, np.sqrt(f * sens2), linestyle= '--', color='crimson', lw=4, label='from ldc2') 

plt.xlabel(r'Frequency f (Hz)',fontsize=24)
plt.ylabel(r'Characteristic strain $h$',fontsize = 24)
plt.ylim([5e-22,1e-16])
plt.xlim([1e-4,1e-1])

plt.yscale('log')
plt.xscale('log')
plt.tick_params(axis='both', which='major', labelsize=18) 
plt.legend(fontsize=20,frameon=False,loc='upper left')
plt.show()
