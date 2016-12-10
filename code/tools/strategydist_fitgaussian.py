import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys
import os

"""
Take a npz file as parameter
"""


if len(sys.argv) < 2:
	print("Usage: 'strategydist_fitgaussian.py dist299.npz'")
	sys.exit(1)
infile = os.path.abspath(sys.argv[1])

plt.rcParams.update({'font.size': 22})
data = np.load(infile)
infl = data['infl']
mu, std = norm.fit(infl)
print mu, std
