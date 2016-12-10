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
	# map from prices to lists of (amount, agent index)
	# amount can be negative, thus representing a sell order
	buyers_by_price = {}
	sellers_by_price = {}

	# Make buy + sell orders
	start_time = time.time()
	for i in range(0, N):
		agent = agents[i]

		Amu = (100. - market.assetPrice) * agent.conservativeness + market.priceMomentum * agent.influencability
		Astd = agent.noisiness 
		amount = int(np.rint( agent.assets * normal(Amu, Astd) ))
		if amount > 0: # buy
			Pmu = 0.99
		else: # sell
			Pmu = 1.01
		# TODO this is arbitrary. We could use market volatility (?)
		# or justify why this gives a good result.
		Pstd = 0.1
		price = normal(Pmu*market.assetPrice, Pstd*market.assetPrice)

		price = clamp(price, 0.01, float("inf"))
		if amount > 0: # buy
			amount = clamp(amount, 0, int(1. * agent.money / price))
			price_list = buyers_by_price
		else: #sell
			amount = clamp(amount, -agent.assets, 0)
			price_list = sellers_by_price

		if price not in price_list:
			price_list[price] = []
		price_list[price].append((amount, i))
	
	bidding_time = time.time()
	
	pstar, accepted_orders = formOrders(buyers_by_price, sellers_by_price)
		
	# PLOT THE BUY/SELL ORDER CURVE
	if False:
		plt.figure()
		x = np.linspace(1., 200., 1000)
		fx = np.linspace(1., 200., 1000)
		gx = np.linspace(1., 200., 1000)
		def f(p):
			total = 0
			for price in reversed(sorted(buyers_by_price)):
				if price < p:
					break
				total += sum([amount for amount,_ in buyers_by_price[price]])
			return total
		def g(p):
			total = 0
			for price in sorted(sellers_by_price):
				if price > p:
					break
				total += sum([abs(amount) for amount,_ in sellers_by_price[price]])
			return total

		for i in range(0, 1000):
			fx[i] = f(x[i])
			gx[i] = g(x[i])
		plt.plot(x, fx, label="buy orders")
		plt.plot(x, gx, label="sell orders")
		# black line at pstar
		plt.plot((pstar,pstar), (0, 500), 'k-')
		plt.legend(loc="best")
		plt.show()
	
	market.setNewPrice(pstar)
	#print("market price + momentum: ", pstar, market.priceMomentum)

	for (agent_idx, amount, price) in accepted_orders:
		agents[agent_idx].assets += amount
		agents[agent_idx].money -= amount*pstar
	price_formation_time = time.time()
	
	#print('time for agents: {}, time for market equilibrium: {}'
	#	.format(bidding_time-start_time, price_formation_time-bidding_time))
	

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
		


def formOrders(buyers_by_price, sellers_by_price):

	accepted_orders = []
	
	buyer_iter = reversed(sorted(buyers_by_price))
	sell_iter = iter(sorted(sellers_by_price))
	
	buy_limit = 0.
	sell_limit = float('Inf')
	
	buy_price = next(buyer_iter, buy_limit)
	sell_price = next(sell_iter, sell_limit)
	pstar = None
	
	if buy_price == buy_limit or sell_price == sell_limit:
		if buy_price == buy_limit:
			# no one willing to buy
			pstar = min(sellers_by_price)
		else:
			# no one willing to sell
			pstar = max(buyers_by_price)
		return pstar, accepted_orders
		
	unmatched_buyers = buyers_by_price[buy_price]
	unmatched_sellers = sellers_by_price[sell_price]
	
	sum_amount = lambda price_list : sum([abs(amount) for (amount,_) in price_list])
	num_unmatched_buyers = sum_amount(buyers_by_price[buy_price])
	num_unmatched_sellers = sum_amount(sellers_by_price[sell_price])
	
	while buy_price >= sell_price:
		pstar = (buy_price + sell_price) / 2.
		
		if num_unmatched_buyers > num_unmatched_sellers:
			# more buyers than sellers, so satisfy all sell orders
			num_unmatched_buyers -= num_unmatched_sellers
			accepted_orders.extend([(agent, amount, sell_price) for (amount, agent) in unmatched_sellers])
			sell_price = next(sell_iter, sell_limit)
			if sell_price in sellers_by_price:
				unmatched_sellers = sellers_by_price[sell_price]
				num_unmatched_sellers = sum_amount(unmatched_sellers)
		else:
			# more sellers than buyers
			num_unmatched_sellers -= num_unmatched_buyers
			accepted_orders.extend([(agent, amount, buy_price) for (amount, agent) in unmatched_buyers])
			buy_price = next(buyer_iter, buy_limit)
			if buy_price in buyers_by_price:
				unmatched_buyers = buyers_by_price[buy_price]
				num_unmatched_buyers = sum_amount(unmatched_buyers)
	if pstar is not None:
		# some buyers or sellers could remain, choose randomly
		if buy_price >= pstar:
			total = sum_amount(buyers_by_price[buy_price])
			if total > 0:
				num_to_choose = total - num_unmatched_buyers
				sample = sample_amounts(buyers_by_price[buy_price], total, num_to_choose)
				accepted_orders.extend([(agent, amount, buy_price) for (amount, agent) in sample])
		if sell_price <= pstar:
			total = sum_amount(sellers_by_price[sell_price])
			if total > 0:
				num_to_choose = total - num_unmatched_sellers
				sample = sample_amounts(sellers_by_price[sell_price], total, num_to_choose)
				accepted_orders.extend([(agent, amount, sell_price) for (amount, agent) in sample])
	else:
		pstar = (buy_price + sell_price) / 2.
		
		
	return pstar, accepted_orders
	
def sample_amounts(amount_tuples, n, k):
	# this could potentially be very slow for large n (large amount of tied assets)
	sample = np.random.choice(n, k, replace=False)
	edges = np.cumsum([0] + [abs(amount) for (amount, _) in amount_tuples])
	allocations = np.histogram(sample, bins=edges)[0]
	return [(amount*np.sign(orig_tuple[0]), orig_tuple[1]) for (orig_tuple, amount) in zip(amount_tuples, allocations)]
	
