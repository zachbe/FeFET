from fefet_model import FeFET
import math
import numpy as np
import scipy
import random
import matplotlib.pyplot as plt
from scipy import stats

fefet1 = FeFET("fefet1")

counts = [[], [], [], []]
ts = [0.01, 0.02, 0.03, 0.04]
for t in range(4):
    for i in range(10000):
        fefet1.reset_hvt()
        for pulse in range(1000):
            fefet1.send_pos_pulse(1, ts[t])
            if(fefet1.read_value() == False):
                counts[t].append(pulse)
                break

# print(counts)
plt.hist(counts, bins = 50)
plt.show()

logmeans = []
logvars = []
for count in counts:
    logmeans.append(np.log10(sum(count)/len(count)))
    logvars.append(np.log10(np.var(count)))

lv = np.array(logvars)
lm = np.array(logmeans)
logn = np.mean(2*lm - lv)
n = (10**logn)
print(n)

slope, intercept, r_value, p_value, std_err = stats.linregress(lm, lv)
print(slope)

lam = fefet1.lam_not * math.exp(fefet1.pol_coef / \
    (scipy.constants.Boltzmann * 300))

us_ex = []
vars_ex = []
for t in ts:
    us_ex.append(fefet1.pos_nuc_count / (lam * t))
    vars_ex.append(fefet1.pos_nuc_count / (lam * t)**2)

us = []
vars = []
for count in counts:
    us.append((sum(count)/len(count)))
    vars.append((np.var(count)))

print("Expected Means")
print(us_ex)
print("Actual Means")
print(us)

print("Expected Vars")
print(vars_ex)
print("Actual Vars")
print(vars)


plt.plot(logmeans, logvars, 'ro')
plt.show()
