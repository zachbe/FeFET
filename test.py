from fefet_model import FeFET
import math
import numpy as np
import scipy
import random
import matplotlib.pyplot as plt
from scipy import stats
import scipy.integrate as integrate

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

lam = fefet1.lam_not * math.exp(fefet1.pol_coef / \
    (scipy.constants.Boltzmann * 300))

def sim_dist(t, fet):
    return 100*(lam*fet.pos_nuc_count*math.exp(-1*lam*t)*\
            ((1-math.exp(-1*lam*t))**(fet.pos_nuc_count-1)))

time = np.linspace(0, 1, 10000)
prob = []
for t in time:
    prob.append(sim_dist(t, fefet1))

plt.plot(time, prob)
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

tot_tim_sim = integrate.quad(lambda x: x*sim_dist(x, fefet1), 0, 100)[0]/100
# print(tot_tim_sim)
us_sim = []
for t in ts:
    us_sim.append(tot_tim_sim / t)

print("Expected Means (Seq)")
print(us_ex)
print("Expected Means (Sim)")
print(us_sim)
print("Actual Means")
print(us)

print("Expected Vars (Seq)")
print(vars_ex)
print("Actual Vars")
print(vars)


plt.plot(logmeans, logvars, 'ro')
plt.show()
