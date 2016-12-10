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
