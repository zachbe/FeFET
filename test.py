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
# plt.hist(counts, bins = 50)
# plt.show()

logmeans = []
logvars = []
for count in counts:
    logmeans.append(np.log10(sum(count)/len(count)))
    logvars.append(np.log10(np.var(count)))

plt.plot(logmeans, logvars, 'ro')
plt.show()
