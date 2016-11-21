from setup import simulationSetup
from simulation import *
from analysis import *

# Number of agents
N = 1000
# Number of simulation steps
T = 4000
# Initial asset price
P0 = 100.
# Initial money count of agents
M0 = 30000.
# Initial asset count of agents
A0 = 300

def main():
	"""Main function of the simulation, containing simulation loop"""

	# Setup
	[agents, market] = simulationSetup(N, P0, M0, A0)

	# Run simulation
	for i in range(0, T):
		#if i % 100 == 0:
		# 	saveDistributionToFile(agents, market, "dist" + str(i) + ".png")
		simulationStep(agents, market)

	# Analyze End results
	plotStrategyDistribution(agents, market)


if __name__ == "__main__":
	main()
