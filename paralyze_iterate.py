import numpy as np
from numpy import log as ln, exp 



def find_n(m, dead_time):
    trials = 100

    n_peak = 1/dead_time # Maximum n could be before m starts going back down again

    t = dead_time
    n_max = n_peak
    n_min = m / (1- m*t)
    
    n = (n_max + n_min) / 2
    # bisection algorithm
    for i in range(trials):
        n = (n_max + n_min) / 2
        new_m = n*exp(-n*t)

        if (new_m > m): # That n was too high, because it should result in a lower count rate than what we actually observed
            n_max = n
        else:
            n_min = n
    return n

def find_t(m1, m2, m12):
    tmin = 0
    tmax = 1/(m12*exp(1))
    t = (tmin + tmax) / 2
    n1 = 0
    n2 = 0
    n12 = 0
    for i in range(100):
        t = (tmin + tmax) / 2
        n1 = find_n(m1, t)
        n2 = find_n(m2, t)
        n12 = find_n(m12, t)

        if n12 > n1 + n2: # Overestimated dead time
            tmax = t
        else:
            tmin = t
    # print(f"Final n: {n1}, {n2}, {n12}")
    return t

# Experimental data, s^-1
M1 = 1.756
M2 = 1.700
M12 = 3.400
E1 = 0.112
E2 = 0.111
E12 = 0.147

print(f"Observed rates: m1 of {M1}+-{E1}, m2 of {M2}+-{E2}, m12 of {M12}+-{E12}")
print("All dead time (t) estimates in seconds.")
print(f"t: {find_t(M1, M2, M12)}")

dm = 0.001 #s^-1
dt_dm1 = (find_t(M1+dm, M2, M12) - find_t(M1-dm, M2, M12)) / (2*dm)
print(f'dt_dm1: {dt_dm1} s')
dt_dm2 = (find_t(M1, M2+dm, M12) - find_t(M1, M2-dm, M12)) / (2*dm)
print(f'dt_dm2: {dt_dm2} s')
dt_dm12 = (find_t(M1, M2, M12+dm) - find_t(M1, M2, M12-dm)) / (2*dm)
print(f'dt_dm2: {dt_dm12} s')

def sq(x):
    return x*x
ET = np.sqrt(sq(dt_dm1)*sq(E1) + sq(dt_dm2)*sq(E2) + sq(dt_dm12)*sq(E12))
print(f'Dead time error: {ET}')
