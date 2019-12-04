from fefet_model import FeFET
import math
import numpy as np
import scipy
import random
import matplotlib.pyplot as plt
from scipy import stats
import scipy.integrate as integrate
from scipy.special import gamma

gamma = -1
c = 1
conc_si_avg = 1
E = 1
r_max = -gamma / (c * conc_si_avg * E)

def p_g_v_dr(r, g):
    lam_vol = conc_si_avg * 4 * math.pi * r**2
    k_vol = g/(2*c*E)
    if(k_vol > -1):
        vol_energy = (lam_vol**k_vol) * math.exp(-lam_vol) / scipy.special.gamma(k_vol + 1)
    else:
        vol_energy = 0

    return vol_energy

def p_g_s_dr(r, g):
    lam_surf = conc_si_avg * 8 * math.pi * r
    k_surf = g / gamma
    if(k_surf > -1):
        surf_energy = (lam_surf**k_surf) * math.exp(-lam_surf) / scipy.special.gamma(k_surf + 1)
    else:
        surf_energy = 0

    return surf_energy

def p_g_dr(r, g):
    def integrand(r, g, x):
        vol_energy = p_g_v_dr(r, x)
        surf_energy = p_g_s_dr(r, g - x)
        return vol_energy * surf_energy
    return integrate.quad(lambda y: integrand(r, g, y), -100, 100)[0]

n = 125
conc_si_avg_list = [conc_si_avg]*n
conc_si_list = [conc_si_avg]*n #temp
for i in range(0, 25):
    conc_si_list[i] += 5
for i in range(25, 100):
    conc_si_list[i] -= 0.5
deltag_avg = []
deltag = []
rs = []
curr_avg = 0

rs_prob = []
gs_prob = []
rv_prob = []
gv_prob = []

r_prob = []
g_prob = []

g_vol = []
g_surf = []

for rad in range(1, n+1):
    r = rad/100
    rs.append(r)
    deltag_avg.append((2 * c * conc_si_avg * E) * (4 * math.pi * r**2) +\
                        gamma * (8 * math.pi * r))

    oldball = (4/3) * math.pi * ((rad-1)/1000)**3
    newball = (4/3) * math.pi * (r)**3
    newv = newball - oldball
    curr_avg = (oldball * curr_avg + newv * conc_si_list[rad-1])/(newball)
    # print(curr_avg)
    #avgsofar = sum(sofar)/len(sofar) #is this how this should work?
    deltag.append((2 * c * curr_avg * E) * (4 * math.pi * r**2) +\
                        gamma * (8 * math.pi * r))

    g_vol.append((2 * c * conc_si_avg * E) * (4 * math.pi * r**2))
    g_surf.append(gamma * (8 * math.pi * r))

    for g in np.linspace(-30, 40, 50):
        p = p_g_s_dr(r, g)
        if(p > .1):
            rs_prob.append(r)
            gs_prob.append(g)
        p = p_g_v_dr(r, g)
        if(p > .1):
            rv_prob.append(r)
            gv_prob.append(g)
        p = p_g_dr(r, g)
        # print(p)
        if(p > .1):
            r_prob.append(r)
            g_prob.append(g)

# plt.subplot(2, 1, 1)
# plt.plot(rs, conc_si_list)
# plt.plot(rs, conc_si_avg_list)
# plt.subplot(2, 1, 2)
# plt.plot(rs, deltag)
plt.plot(rs, deltag_avg)
plt.plot(rs, g_vol)
plt.plot(rs, g_surf)
plt.plot(r_max, 0, 'ro')
plt.plot(rs_prob, gs_prob, 'bo', alpha=0.1)
plt.plot(rv_prob, gv_prob, 'ro', alpha=0.1)
plt.plot(r_prob, g_prob, 'go', alpha=0.5)
plt.show()
