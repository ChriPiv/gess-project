import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
import sys
import os

"""
Take a npz file as parameter. Fit a gaussian distribution to its
agent influencability distribution and print mean+std.
"""


if len(sys.argv) < 2:
	print("Usage: 'strategydist_fitgaussian.py dist299.npz'")
	sys.exit(1)
infile = os.path.abspath(sys.argv[1])

plt.rcParams.update({'font.size': 22})
data = np.load(infile)
infl = data['infl']

hist, bin_edges = np.histogram(infl, density=True, bins=np.linspace(-3,12,100))
bin_centres = (bin_edges[:-1] + bin_edges[1:])/2
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))
p0 = [100., 4., 1.]
coeff, var_matrix = curve_fit(gauss, bin_centres, hist, p0=p0)
A = coeff[0]
mu = coeff[1]
std = coeff[2]

print mu, std
plt.figure()
t = np.linspace(-3, 12, 1000)
plt.hist(infl, bins=np.linspace(-3,12,60), normed=True)
plt.plot(bin_centres, hist)
plt.plot(bin_centres, gauss(bin_centres, *coeff))
#plt.show()
plt.close()
