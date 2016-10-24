class Agent:
	"""
	Ownership and behaviour variables of an agent.
	Attributes:
		money (int):                current amount of money the agent owns
		assets (init):              current amount of assets the agents owns
		riskiness (float):          riskiness parameter
		influencability (float):    influencability parameter
	"""

	def __init__(self, money, assets, riskiness, influencability):
		self.money = money
		self.assets = assets
		self.riskiness = riskiness
		self.influencability = influencability

