import numpy as np
import sys
import os

# All the initial setups we want to try
setups = []
for mean in np.linspace(2., 8., 7):
	for std in np.linspace(1., 5., 5):
		setups.append([mean, std])

# Note: endpoint is one bigger than last index executed
startpoint = 0
endpoint = len(setups)
if len(sys.argv) > 1:
	startpoint = int(sys.argv[1])
if len(sys.argv) > 2:
	endpoint = int(sys.argv[2])

for i in range(startpoint, endpoint):
	print("Running simulation " + str(i))
	[mean, std] = setups[i]
	a = os.system("python main.py out"+str(i)+" "+str(mean)+" "+str(std))
	if a > 0:
		print("There was an error.")
		sys.exit(1)

