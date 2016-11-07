from agent import Agent
from market import Market

def simulationSetup(N, P0, M0, A0):
	"""
	Sets up the simulation objects.
		N: 		Number of agents
		P0: 	Initial asset price
		M0: 	Initial money of agents
		A0: 	Initial asset count of agents

	Returns [agents, market] where
		agent:  array of agent objects in our market
		market: market object of our market
	"""

	agents = []
	for _ in range(0, N):
		# All agents are initially the same
		agents.append(Agent(M0, A0, 0.5, 0.5))

	market = Market(P0)

	return agents, market
