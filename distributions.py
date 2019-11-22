import numpy as np
import scipy
import scipy.constants
import random
from sympy import *
from sympy.stats import *
from sympy.utilities.lambdify import lambdastr
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import mcint
# from mpmath import *

random.seed(1)

lam_u = 1#symbols('lam_u')
lam_s = 0.1#symbols('lam_s')

u_nsi = 1

x = symbols('x')
y = symbols('y')

#Nsi = Poisson("Nsi", u_nsi)

Lam_old = Normal('Lam_old', lam_u, lam_s)

Lam = 1/(sqrt(2*pi*lam_s**2)) * exp(-(x-lam_u)**2 / (2*lam_s**2))
normal = lambdify(x, Lam, "math")
#Exp = l * exp(-l * y)

def expdist(l):
    return l * exp(-l*y)
print(Lam_old)
print(density(Lam_old)(x))
print(expdist(density(Lam_old)(x)) * density(Lam_old)(x))

f_exp = expdist(density(Lam_old)(x)) * density(Lam_old)(x)
# pprint(f_exp)

f = lambdify((x,y), f_exp, "math")

print("{}".format(f(1, 1)))

def n_one_dist(y):
    return integrate.quad(lambda x: f(x, y), -100, 100)[0]

def simul_dist(n, y):
    surv = 0
    num = 1
    t = symbols('t')
    tup = [t]
    for i in range(0,n):
        new_l = symbols('l_'+str(i))
        new = density(Lam_old)(new_l)
        num = num * (1 - exp(-new * t))
        surv = surv + ((new * exp(-new*t)/(1 - exp(-new * t))))
        tup.append(new_l)
    surv = surv*num
    for i in range(0,n):
        new_l = symbols('l_'+str(i))
        new = density(Lam_old)(new_l)
        surv = surv*new
    # pprint((surv))
    tup = tuple(tup)
    simul = lambdify(tup, surv, "math")
    # simulstr = lambdastr(tup, surv, "math")
    # print(simulstr)
    def sampler(n, y):
        while True:
            tup = [y]
            for i in range(0,n):
                tup.append(random.uniform(-100,100))
            tup = tuple(tup)
            yield tup
    def unpacker(tup):
        # print(*tup)
        return simul(*tup)
    # return integrate.quad(lambda x: simul(y,x), -100, 100)[0]
    return mcint.integrate(unpacker, sampler(n, y), n=100000)[0]

    # for i in range(0,n):

    #return integrate.quad(lambda x: f(x, y), -100, 100)[0]

# simul_dist(2,2)

probs = []
eprobs = []
sprobs = []
# rang = np.linspace(0, 10, 1000)
rang = (1,2)
for i in rang:
    probs.append(n_one_dist(i))
    eprobs.append(3 * exp(-3*i))
    sprobs.append(simul_dist(1,i))
#
print(sprobs)
print(probs)
# plt.plot(rang, probs, 'r')
# plt.plot(rang, eprobs, 'b')
# plt.plot(rang, sprobs, 'g')
# plt.show()

# print(quad(expdist(density(Lam_old)(x)) * density(Lam_old)(x), x))
