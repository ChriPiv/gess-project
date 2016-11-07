from agent import Agent
import numpy as np

class Market:
	"""
	Global variables of a market.
	Attributes:
		assetPrice (float):  	current asset price
		history (float array): 	history of prices
		priceMomentum (float): 	price momentum calculated from previous time step
	    volatility (float):     volatility of the asset price in the last 20 turns
    """



	def __init__(self, initialPrice):
		self.assetPrice = float(initialPrice)
		self.history = [self.assetPrice]
		self.priceMomentum = 0.
		self.volatility = 0.01 # TODO what should this be?

	def setNewPrice(self, price):
		"""
		Update the price, price momentum and volatiltiy of the market.
		"""
		self.assetPrice = price
		self.history.append(price)

		if len(self.history) > 2:
			lastvalues = self.history[-20:]
			logvalues = np.zeros(len(lastvalues) - 1)
			for i in range(0, len(logvalues)):
				logvalues[i] = np.log(lastvalues[i+1]/lastvalues[i])
			self.volatility = np.std(logvalues)
		self.volatility = max(0.001, self.volatility)
