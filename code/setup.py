from agent import Agent, consFromInfl
from market import Market
from numpy.random import *

def simulationSetup(N, P0, M0, A0, OneD=False):
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
		noisiness = 0.05
		# Our space we are interested in is 
		# [0,4] for influencability
		# [0,0.1] for conservativeness
		# so we link them by infl + 800*consvs = 4
		# but we allow agents outside aswell
		influencability = normal(5., 3.)
		if OneD:
			conservativeness = consFromInfl(influencability)
		else:
			conservativeness = normal(0.001, 0.0025)
		agents.append(Agent(M0, A0, noisiness, influencability, conservativeness))

	market = Market(P0)

	return agents, market


def resetSimulation(agents, market, P0, M0, A0):
	for agent in agents:
		agent.money = M0
		agent.assets = A0
	market = Market(P0)
