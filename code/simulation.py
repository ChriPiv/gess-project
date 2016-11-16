from __future__ import print_function

import numpy as np
from numpy.random import rand, randint, normal
import random
import matplotlib.pyplot as plt
import sys

import time

def clamp(x, minval, maxval):
	return max(minval, min(x, maxval))



def simulationStep(agents, market):

	N = len(agents)
	# Orders are tuples [amount, limitPrice] 
	# amount can be negative, thus representing a sell order
	orders = [[]] * N

	# Make buy + sell orders
	start_time = time.time()
	for i in range(0, N):
		agent = agents[i]

		Amu = 1. + (market.assetPrice - 100.) * agent.fundamentalism + market.priceMomentum * agent.influencability
		Astd = agent.riskiness * 10
		amount = agent.assets - int(np.rint(normal(Amu*agent.assets, Astd)))
		amount = clamp(amount, -agent.assets, float("inf"))

		if amount > 0: # buy
			Pmu = market.assetPrice * 0.99
		else: # sell
			Pmu = market.assetPrice * 1.01
		# TODO this is arbitrary. We could use market volatility (?)
		# or justify why this gives a good result.
		Pstd = 7.
		price = normal(Pmu, Pstd)
		if amount > 0: # buy
			price = clamp(price, 0.01, agent.money / amount)
		else: #sell
			price = clamp(price, 0.01, float("inf"))

		orders[i] = [amount, price]

	bidding_time = time.time()

	def f(p):
		retval = 0
		for amount, price in orders:
			if amount > 0 and price >= p:
				retval += amount
		return retval
	def g(p):
		retval = 0
		for amount, price in orders:
			if amount < 0 and price <= p:
				retval -= amount
		return retval

	# PLOT THE BUY/SELL ORDER CURVE
	if False:
		plt.figure()
		x = np.linspace(1., 200., 1000)
		fx = np.linspace(1., 200., 1000)
		gx = np.linspace(1., 200., 1000)
		for i in range(0, 1000):
			fx[i] = f(x[i])
			gx[i] = g(x[i])
		plt.plot(x, fx, label="buy orders")
		plt.plot(x, gx, label="sell orders")
		plt.legend(loc="best")
		plt.show()

	# Set the new price
	pstar = market.assetPrice
	direction = np.sign(f(pstar) - g(pstar))
	# TODO lol do that better 
	# Note: careful that pstar not 0
	while direction != 0 and direction == np.sign(f(pstar) - g(pstar)):
		pstar += 0.01*direction

	if pstar <= 0.1:
		pstar = 0.1
	market.setNewPrice(pstar)
	print("market price + momentum: ", pstar, market.priceMomentum)

	for i in range(0, N):
		if orders[i][0] > 0 and orders[i][1] <= market.assetPrice:
			orders[i] = [0, 0.]
		if orders[i][0] < 0 and orders[i][1] >= market.assetPrice:
			orders[i] = [0, 0.]

	if f(pstar) > g(pstar):
		for _ in range(0, f(pstar)-g(pstar)):
			i = randint(N)
			while orders[i][0] <= 0 or orders[i][1] <= pstar:
				i = randint(N)
			orders[i][0] -= 1
	else:
		for _ in range(0, g(pstar)-f(pstar)):
			i = randint(N)
			while orders[i][0] >= 0 or orders[i][1] >= pstar:
				i = randint(N)
			orders[i][0] += 1

	for i in range(0, N):
		agents[i].assets += orders[i][0]
		agents[i].money -= orders[i][0]*orders[i][1]
	price_formation_time = time.time()
	
	print('time for agents: {}, time for market equilibrium: {}'
		.format(bidding_time-start_time, price_formation_time-bidding_time))


def simulationStepPaper(agents, market):
	"""
	Run one simulation time step with agents and market, as described
	by 'Agent-based simulation of a financial market'
	"""

	N = len(agents)
	# Orders are tuples [amount, limitPrice]
	buy_orders = [[]] * N
	sell_orders = [[]] * N

	# Make buy + sell orders
	for i in range(0, N):
		agent = agents[i]
		if rand() > 0.5:
			# buy
			price = market.assetPrice / normal(1.01, 3.5*market.volatility)
			price = clamp(price, 0.01, float("inf"))
			amount = int(rand() * agent.money / price)

			buy_orders[i] = [amount, price]
			sell_orders[i] = [0, 0.]
		else:
			# sell
			price = market.assetPrice * normal(1.01, 3.5*market.volatility)
			price = clamp(price, 0.01, float("inf"))
			amount = int(rand() * agent.assets)
						
			buy_orders[i] = [0, 0.]
			sell_orders[i] = [amount, price]

	# define functions f and g as in the paper
	def f(p):
		retval = 0
		for amount, price in buy_orders:
			if price >= p:
				retval += amount
		return retval
	def g(p):
		retval = 0
		for amount, price in sell_orders:
			if price <= p:
				retval += amount
		return retval

	# PLOT THE BUY/SELL ORDER CURVE
	if False:
		plt.figure()
		x = np.linspace(1., 200., 1000)
		fx = np.linspace(1., 200., 1000)
		gx = np.linspace(1., 200., 1000)
		for i in range(0, 1000):
			fx[i] = f(x[i])
			gx[i] = g(x[i])
		plt.plot(x, fx, label="buy orders")
		plt.plot(x, gx, label="sell orders")
		plt.legend(loc="best")
		plt.show()

	# Set the new price
	pstar = market.assetPrice
	direction = np.sign(f(pstar) - g(pstar))
	# TODO lol do that better. Ideas: secant method? fitting some polynomial?
	# Note: careful that pstar not 0
	while direction != 0 and direction == np.sign(f(pstar) - g(pstar)):
		pstar += 0.01*direction

	if pstar <= 0.1:
		pstar = 0.1
	print("New market price: ", pstar)
	market.setNewPrice(pstar)

	
	for i in range(0, N):
		if buy_orders[i][1] <= market.assetPrice:
			buy_orders[i] = [0, 0.]
		if sell_orders[i][1] >= market.assetPrice:
			sell_orders[i] = [0, 0.]
	
	# TODO: do this better aswell
	#print('having to fix leftovers: ', abs(f(pstar)-g(pstar)))
	if f(pstar) > g(pstar):
		for _ in range(0, f(pstar)-g(pstar)):
			i = randint(N)
			while buy_orders[i][0] == 0 or buy_orders[i][1] <= pstar:
				i = randint(N)
			buy_orders[i][0] -= 1
	else:
		for _ in range(0, g(pstar)-f(pstar)):
			i = randint(N)
			while sell_orders[i][0] == 0 or sell_orders[i][1] >= pstar:
				i = randint(N)
			sell_orders[i][0] -= 1

	
	# Update agent stats
	for i in range(0, N):
		agents[i].assets += buy_orders[i][0]
		agents[i].assets -= sell_orders[i][0]
		agents[i].money -= buy_orders[i][0]*buy_orders[i][1]
		agents[i].money += sell_orders[i][0]*sell_orders[i][1]

