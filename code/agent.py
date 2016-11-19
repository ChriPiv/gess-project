class Agent:
	"""
	Ownership and behaviour variables of an agent.
	Attributes:
		money (float):             current amount of money the agent owns
		assets (int):              current amount of assets the agents owns
		noisiness (float):         noisiness parameter
		influencability (float):   influencability parameter
		conservativeness (float):  conservativeness parameter
	"""

	def __init__(self, money, assets, noisiness, influencability, conservativeness):
		self.money = float(money)
		self.assets = int(assets)
		self.noisiness = float(noisiness)
		self.influencability = float(influencability)
		self.conservativeness = float(conservativeness)

