from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

def saveStrategyDistributionToFile(agents, market, filename, OneD=False):
	val = []
	infl = []
	consv = []
	for a in agents:
		val.append(a.assets*market.assetPrice + a.money)
		infl.append(a.influencability)
		consv.append(a.conservativeness)
	if OneD:
		plt.figure()
		plt.xlim([-10, 20])
		plt.ylim([0, 120])
		plt.hist(infl, bins=30)
		plt.savefig(filename)
		plt.close()
	else:
		plt.figure()
		plt.xlim([-10, 20])
		plt.ylim([-0.04, 0.05])
		sc = plt.scatter(infl, consv, c=val)
		plt.colorbar(sc)
		plt.savefig(filename)
		plt.close()

def serializeStrategyDistribution(agents, market, filename):
	val = []
	infl = []
	consv = []
	for a in agents:
		val.append(a.netWorth(market))
		infl.append(a.influencability)
		consv.append(a.conservativeness)
	val = np.asarray(val)
	infl = np.asarray(infl)
	consv = np.asarray(consv)
	np.savez(filename, val=val, infl=infl, consv=consv)

def saveMoneyDistributionToFile(agents, market, filename):
	value = []
	for a in agents:
		value.append(a.assets*market.assetPrice + a.money)
	plt.figure()
	plt.xlim([0, 150000])
	plt.ylim([0, 300])
	plt.hist(value, bins=np.linspace(0, 150000, 60))
	plt.savefig(filename)
	plt.close()



def plotStrategyDistribution(agents, market):
	"""
	Plot the frequencies of the different strategy parameter ranges
	angents: 	agents objects having gone through the simulation
	market: 	market state at the end of the simulation
	"""

	# Plot distribution of money
	value = []
	for a in agents:
		value.append(a.assets*market.assetPrice + a.money)
	plt.hist(value, bins=30)
	plt.show()

	# Plot final value vs influencability
	val = []
	infl = []
	for a in agents:
		val.append(a.assets*market.assetPrice + a.money)
		infl.append(a.influencability)
	plt.figure()
	sc = plt.plot(infl, val, '*')
	plt.show()

	# Plot a color scatter plot: value vs influencability and conservativeness
	#val = []
	#infl = []
	#consv = []
	#for a in agents:
	#	val.append(a.assets*market.assetPrice + a.money)
	#	infl.append(a.influencability)
	#	consv.append(a.conservativeness)
	#plt.figure()
	#sc = plt.scatter(infl, consv, c=val)
	#plt.colorbar(sc)
	#plt.show()

	# Plot price history
	T = len(market.history)
	time = np.linspace(0, T, T)
	plt.figure()
	plt.plot(time, market.history)
	plt.ylim([0, 200])
	plt.show()


	total_assets = 0
	for agent in agents:
		total_assets += agent.assets
	#print("assets owned: ", total_assets)
	#print("(at beginning it was 30000)")


def savePriceHistoryToFile(market, filename):
	"""
	Plot the history of prices
	agents: 	agents objects having gone through the simulation
	market: 	market state at the end of the simulation
	filename: 	file to save the plot
	"""

	# Plot price history
	T = len(market.history)
	time = np.linspace(0, T, T)
	plt.figure()
	plt.plot(time, market.history)
	plt.ylim([0, 200])

	plt.xlabel("Timestep")
	plt.ylabel("Market price p*")
	plt.title("Price Evolution Over Time")
	plt.savefig(filename)
	plt.close()

def saveReturnHistoryToFile(market, filename):
	"""
	Save the return history, ie for r(t)=log(p(t)/p(t-1)), plot r vs t
	market: 	market after a full round of simulation
	filename: 	file to save the plot
	"""

	# Compute returns
	T = len(market.history)
	r = np.empty(T-1, dtype=float)
	for t in range(T-1):
		r[t] = np.log(market.history[t]/market.history[t-1])

	# Plot return history
	time = np.linspace(1, T, T-1)
	plt.figure()
	plt.plot(time, r)
	plt.ylim([-0.15, 0.15])
	plt.xlabel("Time")
	plt.ylabel("Returns")
	plt.title("Return Evolution Over Time")
	plt.savefig(filename)
	plt.close()

def saveReturnDistributionToFile(market, filename):
	"""
	Save the return distribution, ie for r(t)=log(p(t)/p(t-1)), plot the fraction of r greater than x
	market: 	market after a full round of simulation
	filename: 	file to save the plot
	"""

	#market.history = market.history[400:]

	# Compute returns
	T = len(market.history)
	r = np.empty(T-1, dtype=float)
	for t in range(T-1):
		r[t] = np.log(market.history[t]/market.history[t-1])

	# as in Raberto et al, retrend by the mean, rescale by standard deviation, and take abs
	r -= np.mean(r)
	r /= np.std(r)
	r = np.abs(r)

	r = np.sort(r)
	prob = np.linspace(T-1, 1, num=T-1)/T

	# for reference, compare against a variable that is normally distributed
	#normCumSum = 1-gaussianCDF(r)
	# It's hard to approximate the CDF of a gaussian, so instead perform random draws
	numDraws = 1000000
	gaussian = np.random.normal(size=numDraws)
	gaussian = np.abs(gaussian)
	gaussian = np.sort(gaussian)
	gaussianProb = np.linspace(numDraws, 1, num=numDraws)/(numDraws+1)

	# Plot cumulative return distribution
	plt.figure()
	plt.loglog(r, prob, '.', label='Simulated Returns')
	plt.loglog(gaussian, gaussianProb, '-', label='N(0,1)')

	plt.xlim([1e-1, 1e1])
	plt.ylim([1e-4, 1e0])

	plt.xlabel("Log Returns r")
	plt.ylabel("Fraction of Returns > r")
	plt.title("Fat Tail of Return Distribution")
	plt.savefig(filename)
	plt.close()

def gaussianCDF(x):
	return 0.5 * (1 + erf(x/np.sqrt(2)))
def erf(x):
	# copied this from wikipedia
	# see Abramowitz and Stegun
	p = 0.3275911
	a1 = 0.254829592
	a2 = -0.284496736
	a3 = 1.421413741
	a4 = -1.453152027
	a5 = 1.061405429
	t = 1 / (1 + p*x)
	result = 1 - (a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5)*np.exp(-x**2)
	return result

