import numpy as np
import matplotlib.pyplot as plt

def plotStrategyDistribution(agents, market):
	"""
	Plot the frequencies of the different strategy parameter ranges
	angents: 	agents objects having gone through the simulation
	market: 	market state at the end of the simulation
	"""

	# TODO: sth correct
	value = []
	for a in agents:
		value.append(a.assets*market.assetPrice + a.money)
	plt.hist(value, range=(0, 30000), bins=20)
	plt.show()

	T = len(market.history)
	time = np.linspace(0, T, T)
	plt.figure()
	plt.plot(time, market.history)
	plt.ylim([0, 300])
	plt.show()


	total_assets = 0
	for agent in agents:
		total_assets += agent.assets
	print "assets owned: ", total_assets
	print "(at beginning it was 30000)"
