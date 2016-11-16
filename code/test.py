
from simulation import formOrders


def main():
	test_price_formation()
	# Feel free to write more tests to debug your code
	# test_something_else()
	# ...
	print('all tests passed!')

def test_price_formation():
	# no sellers
	pstar, orders = formOrders({123:[(5,0)]},{})
	assert len(orders)==0
	
	# no buyers
	pstar, orders = formOrders({}, {456:[(-3,0)]})
	assert len(orders)==0
	
	# exactly one pair
	pstar, orders = formOrders(buyers_by_price={789:[(1,0)]}, sellers_by_price={789:[(-1,1)]})
	assert pstar == 789
	assert len(orders)==2
	assert orders[0][2] == 789
	assert orders[1][2] == 789
	assert orders[0][1] + orders[1][1] == 0
	
	# exactly one pair, two different prices
	pstar, orders = formOrders(buyers_by_price={11:[(1,0)]}, sellers_by_price={10:[(-1,1)]})
	epsilon = 1e-9
	assert abs(pstar - 10.5) < epsilon
	assert len(orders)==2
	assert orders[0][1] + orders[1][1] == 0
	
	# exactly one pair, unsatisfiable
	pstar, orders = formOrders(buyers_by_price={5:[(1,0)]}, sellers_by_price={500:[(-1,1)]})
	# What should pstar be in this case? 252.5? None? 5? 500?
	assert len(orders)==0
	
	
	# several orders of variable length
	pstar, orders = formOrders(
		buyers_by_price={11:[(3,0)], 12:[(3,1)], 13:[(3,2)]}, 
		sellers_by_price={10:[(-1,3)], 9:[(-3,4)], 8:[(-3,5)], 7:[(-2,6)]})
	assert len(orders) == 7 # each agent's order is satisfiable
	uniqueAgents = sorted(set([agent for (agent,_,_) in orders]))
	assert uniqueAgents == list(range(7))
	assert abs(pstar - 10.5) < epsilon
	
	# two orders, one partially satisfied
	pstar, orders = formOrders(buyers_by_price={10:[(10,0)]}, sellers_by_price={10:[(-2,1)]})
	assert pstar == 10
	assert len(orders) == 2
	buy_order = next(order for order in orders if order[0]==0)
	sell_order = next(order for order in orders if order[0]==1)
	assert buy_order == (0, 2, 10)
	assert sell_order == (1, -2, 10)
	
	# several orders, some partially satisfied
	pstar, orders = formOrders(
		buyers_by_price={10:[(3,0),(3,1),(3,2),(3,3),(3,4)]}, # 15 buys
		sellers_by_price={10:[(-3,5),(-3,6),(-3,7)]}) # 9 sells
	assert pstar == 10
	assert sum([amount for (_,amount,_) in orders]) == 0 # all accounted for
	assert sum([abs(amount) for (_,amount,_) in orders]) == 18 # 2*9 total
	
	
	# several orders of variable length, middle one partially satisfied
	pstar, orders = formOrders(
		buyers_by_price={10:[(3,0)], 11:[(3,1)], 12:[(3,2)]},   # 9 buys
		sellers_by_price={10:[(-1,3)], 9:[(-3,4)], 8:[(-3,5)]}) # 7 sells
	assert len(orders) == 6 # each agent's order is at least partially satisfiable
	uniqueAgents = sorted(set([agent for (agent,_,_) in orders]))
	assert uniqueAgents == list(range(6))
	assert pstar == 10
	# the lowest bidder (agent 0) gets the worst offer
	agent0 = next(order for order in orders if order[0]==0)
	assert agent0 == (0, 1, 10) # only 1/3 went through
	assert sum([amount for (_,amount,_) in orders]) == 0
	assert sum([abs(amount) for (_,amount,_) in orders]) == 14 # 2*7 total

if __name__ == "__main__":
	main()
