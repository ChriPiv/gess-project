import numpy as np
import matplotlib.pyplot as plt
import sys
import os

"""
Take a folder out_X as paramaters and converts the files disti.npz to a plot
disti.png for i=0,...,499 (1D so histrogram with influencability) and makes
a video of the evolution called video.mp4.
"""


if len(sys.argv) < 2:
	print("Usage: 'convergenceplot.py out_X/' where the folder out_X contains the npz files")
	sys.exit(1)
folder = os.path.abspath(sys.argv[1])

plt.rcParams.update({'font.size': 22})

for i in range(0, 300):
	print("Prosessing file "+str(i)+"/300")
	data = np.load(os.path.join(folder, "dist"+str(i)+".npz")) 
	infl = data['infl']
	plt.figure(figsize=(12, 8))
	plt.title(r'Agent Strategy Distribution Histogram after '+str(i)+' timesteps')
	plt.xlabel(r'Agent Influencability')
	plt.ylabel(r'Frequency')
	plt.xlim([-3, 12])
	plt.hist(infl, bins=np.linspace(-10, 20, 100))
	plt.ylim([0, 250])
	plt.savefig(os.path.join(folder, "dist"+str(i).zfill(3)+".png"))
	plt.close()

os.system("ffmpeg -framerate 10 -i "+folder+"/dist%03d.png -s:v 1280x720 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p "+folder+"/video.mp4")
