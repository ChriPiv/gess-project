import numpy as np
import matplotlib.pyplot as plt

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
	plt.plot(infl, val, '*')
	fit = np.polyfit(infl, val, 1)
	print 'Fit value vs influencability:', fit
	fit_fn = np.poly1d(fit) 
	plt.plot(infl, fit_fn(infl)) 
	plt.show()

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
	print "assets owned: ", total_assets
	print "(at beginning it was 30000)"
