from agent import Agent
from market import Market
from numpy.random import *

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
	# Generate inital agents
	for _ in range(0, N):
		agents.append(Agent(M0, A0, 0.05, uniform(0.,4.), uniform(0.003, 0.006)))

	market = Market(P0)

	return agents, market
