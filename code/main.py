import os

from setup import *
from simulation import *
from analysis import *
from optimization import *

# Number of agents
N = 1000
# Number of learning steps
L = 10
# Number of simulation steps (per learning process)
T = 1000
# Initial asset price
P0 = 100.
# Initial money count of agents
M0 = 30000.
# Initial asset count of agents
A0 = 300

def main():
	"""Main function of the simulation, containing simulation loop"""

	# Create output directory if it doesn't already exist
	if not os.path.exists('out/'):
		os.makedirs('out/')

	[agents, market] = simulationSetup(N, P0, M0, A0)

	# Run simulation
	for l in range(0, L):
		resetSimulation(agents, market, P0, M0, A0)
		for t in range(0, T):
			#saveDistributionToFile(agents, market, "dist" + str(i) + ".png")
			simulationStep(agents, market)
		print ("finished current simulation round")

		saveStrategyDistributionToFile(agents, market, "dist" + str(l) + ".png")
		# optimizeGradient(agents, market, saveToFile="gradient"+str(l)+".png")
		optimizeNaive(agents, market, saveToFile="wealth"+str(l)+".png")

if __name__ == "__main__":
	main()
