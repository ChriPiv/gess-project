from agent import Agent

class Market:
	"""
	Global variables of a market.
	Attributes:
		assetPrice (int):       current asset price
		priceMomentum (int):    price momentum calculated from previous time step
	"""



	def __init__(self, initialPrice):
		self.assetPrice = initialPrice
		self.priceMomentium = 0
   
