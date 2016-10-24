from setup import simulationSetup
from simulation import simulationStep

# Number of agents
N = 1000
# Number of simulation steps
T = 100


def main():
	"""Main function of the simulation, containing simulation loop"""

	# Setup
	[agents, market] = simulationSetup(N)

	# Run simulation
	for i in range(0, T):
		if i % 10 == 0:
			print 'asdf'
			# TODO ranking + mutation
		simulationStep(agents, market)

	# Analyze End results
	analyze(agents, market)


if __name__ == "__main__":
	main()
