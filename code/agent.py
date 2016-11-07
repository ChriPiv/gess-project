class Agent:
	"""
	Ownership and behaviour variables of an agent.
	Attributes:
		money (float):                current amount of money the agent owns
		assets (int):              current amount of assets the agents owns
		riskiness (float):          riskiness parameter
		influencability (float):    influencability parameter
	"""

	def __init__(self, money, assets, riskiness, influencability):
		self.money = float(money)
		self.assets = int(assets)
		self.riskiness = float(riskiness)
		self.influencability = float(influencability)

