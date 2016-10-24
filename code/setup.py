from agent import Agent
from market import Market

def simulationSetup(N):
	"""
	Sets up the simulation objects.
		N:  Number of agents

	Returns [agents, market] where
		agent:  array of agent objects in our market
		market: market object of our market
	"""

	agents = []
	for _ in range(0, N):
		agents.append(Agent(10, 10, 10, 10))

	market = Market(1000)

	return agents, market
