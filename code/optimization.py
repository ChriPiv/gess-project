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
		plt.close()

	for agent in agents:
		bef = agent.influencability
		agent.influencability += normal (agent.gradient/2000., 0.2) #TODO BETTER
		agent.conservativeness = (9. - agent.influencability) / 400.
		

def optimizeEvolutionary(agents, market):
	return

def optimizeMLS(agents, market, saveToFile=None):

	sigma = np.asarray([2, 1])
	D = 1

	influencabilities = []
	gradients = []
	assetPrices = []
	for agent in agents:
		sumPhiXX = np.zeros((D+1, D+1), dtype=float)
		sumPhiXF = np.zeros((D+1), dtype=float)

		x = np.asarray([agent.influencability, 1])
		for otherAgent in agents:
			x_i = np.asarray([otherAgent.influencability, 1])

			phi = np.exp(-np.linalg.norm((x - x_i)/sigma)**2)

			sumPhiXX += phi*np.outer(x_i, x_i)
			sumPhiXF += phi*x_i*otherAgent.netWorth(market)
		EPSILON = 1e-9
		if(np.abs(np.linalg.det(sumPhiXX)) >= EPSILON):
			c = np.linalg.inv(sumPhiXX).dot(sumPhiXF)
		else:
			# this can happen if no other agents are close enough. Assign 0 gradient.
			# maybe instead, the agent should move closer to the mean? not sure.
			c = np.zeros((D+1), dtype=float)

		agent.gradient = c[0]

		influencabilities.append(agent.influencability)
		gradients.append(agent.gradient)
		assetPrices.append(agent.netWorth(market))

	if saveToFile != None:
		plt.figure()
		plt.scatter(influencabilities, gradients, c=assetPrices)
		plt.savefig("out/" + saveToFile)

	learningRate = 1./2000.
	for agent in agents:
		# TODO: maybe compare this with random movement, as in optimizeGradient
		agent.influencability += learningRate*agent.gradient
		agent.conservativeness = (9. - agent.influencability) / 400.

"""
return agent array sorted by their wealth, ascending 
"""
def sortAgents(agents, market):
	return sorted(agents, key=lambda a:[a.money+a.assets*market.assetPrice])
