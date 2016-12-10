import numpy as np
import sys
import os

from setup import *
from simulation import *
from analysis import *
from optimization import *

# Number of agents
N = 1000
# Number of simulation steps
T = 1000
# Initial asset price
P0 = 100.
# Initial money count of agents
M0 = 30000.
# Initial asset count of agents
A0 = 300

def main():
	# Runs a single round of simulation, ie to show buy/sell curves, price
	# evolution, and other motivating imagery

	print("Running single simulation")
	outdir = 'single_out/'
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	buySellFilename = outdir + 'buy_sell_{:04}.png'

	[agents, market] = simulationSetup(N, P0, M0, A0, OneD=True)

	resetSimulation(agents, market, P0, M0, A0)
	for t in range(0, T):
		simulationStep(agents, market, buySellFilename.format(t), t)



if __name__ == "__main__":
	main()
