from __future__ import print_function

import numpy as np
from numpy.random import rand, randint, normal
import random
import matplotlib.pyplot as plt
import sys

def optimizeNaive(agents, market, saveToFile=None):
	agents = sortAgents(agents, market)
	N = len(agents)
	for i in range(0, N):
		agent = agents[i]
		agent.influencability += normal(0., 0.00001+1.*(N-i)/N) # Mean = 0, Std = 0.00001, i = index of the agent
		agent.conservativeness = (9. - agent.influencability) / 400.
	if saveToFile is not None:
		influencability = []
		wealth = []
		conservativeness = []
		for agent in agents:
			influencability.append(agent.influencability)
			wealth.append(agent.netWorth(market))
			conservativeness.append(agent.conservativeness)
		plt.figure()
		plt.scatter(influencability, conservativeness, c=wealth)
		plt.xlabel("influencability")
		plt.ylabel("conservativeness")
		plt.savefig("out/" + saveToFile)

def optimizeGradient(agents, market, saveToFile=None):
	agents = sortAgents(agents, market)
	N = len(agents)

	scatterx = []
	scattery = []
	scatterc = []
	for i in range(0, N):
		agent = agents[i]
		gradient = 0.
		weight = 0.
		for a2 in agents:
			dist = a2.influencability - agent.influencability
			# Don't consider the same agent
			if dist == 0:
				dist = float("inf")
			weight += np.exp(-abs(dist))
			gradient += np.exp(-abs(dist)) * (a2.money-agent.money + market.assetPrice*(a2.assets-agent.assets)) * np.sign(dist) * ((a2.money+a2.assets*market.assetPrice)/(agents[-1].money+agents[-1].assets*market.assetPrice))
			#print(np.exp(-100.*abs(dist)) * (a2.money-agent.money + market.assetPrice*(a2.assets-agent.assets)) / (0.0001+dist))
		agent.gradient = gradient / weight
		agent.gradient *= (1. - 1.*i/N)
		scatterx.append(agent.influencability)
		scattery.append(agent.gradient)
		scatterc.append(agent.money+agent.assets*market.assetPrice)
	if saveToFile != None:
		plt.figure()
		plt.scatter(scatterx, scattery, c=scatterc)
		plt.savefig("out/" + saveToFile)

	for agent in agents:
		bef = agent.influencability
		agent.influencability += normal (agent.gradient/2000., 0.2) #TODO BETTER
		agent.conservativeness = (9. - agent.influencability) / 400.
		

def optimizeEvolutionary(agents, market):
	return

"""
return agent array sorted by their wealth, ascending 
"""
def sortAgents(agents, market):
	return sorted(agents, key=lambda a:[a.money+a.assets*market.assetPrice])
