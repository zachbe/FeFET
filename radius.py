from fefet_model import FeFET
import math
import numpy as np
import scipy
import random
import matplotlib.pyplot as plt
from scipy import stats
import scipy.integrate as integrate

gamma = -1
c = 1
conc_si_avg = 1
E = 1
r_max = -gamma / (c * conc_si_avg * E)

n = 1250
conc_si_avg_list = [conc_si_avg]*n
conc_si_list = [conc_si_avg]*n #temp
for i in range(0, 500):
    conc_si_list[i] += 1
for i in range(500, 1000):
    conc_si_list[i] -= 1
deltag_avg = []
deltag = []
rs = []
for rad in range(1, n+1):
    r = rad/1000
    rs.append(r)
    deltag_avg.append((2 * c * conc_si_avg * E) * (4 * math.pi * r**2) +\
                        gamma * (8 * math.pi * r))

    sofar = conc_si_list[0:rad]
    avgsofar = sum(sofar)/len(sofar) #is this how this should work?
    deltag.append((2 * c * avgsofar * E) * (4 * math.pi * r**2) +\
                        gamma * (8 * math.pi * r))


plt.subplot(2, 1, 1)
plt.plot(rs, conc_si_list)
plt.plot(rs, conc_si_avg_list)
plt.subplot(2, 1, 2)
plt.plot(rs, deltag)
plt.plot(rs, deltag_avg)
plt.plot(r_max, 0, 'ro')
plt.show()
