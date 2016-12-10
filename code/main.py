import os
import sys

from setup import *
from simulation import *
from analysis import *
from optimization import *

# Number of agents
N = 1000
# Number of learning steps
L = 500
# Number of simulation steps (per learning process)
T = 3000
# Initial asset price
P0 = 100.
# Initial money count of agents
M0 = 30000.
# Initial asset count of agents
A0 = 300

def main():
	"""Main function of the simulation, containing simulation loop"""

	# Create output directory if it doesn't already exist
	if len(sys.argv) == 2:
		outdir = sys.argv[1]
	else:
		outdir = 'out/'
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	[agents, market] = simulationSetup(N, P0, M0, A0, OneD=True)

	# Run simulation
	for l in range(0, L):
		print("Running learning step " + str(l) +"/" + str(L))
		resetSimulation(agents, market, P0, M0, A0)
		for t in range(0, T):
			simulationStep(agents, market)

		serializeStrategyDistribution(agents, market, outdir + "dist" + str(l) + ".npz")
		saveStrategyDistributionToFile(agents, market, outdir + "dist" + str(l) + ".png", OneD=True)
		optimizeGradient(agents, market, saveToFile=outdir + "gradient"+str(l)+".png", OneD=True)

if __name__ == "__main__":
	main()
