"""
Coded by Adam Greenberg - adamhgreenberg@ucla.edu
Copyright 2014, Margot Research Group
"""

import pyfits as pf
import copy as cp
import numpy as np
import matplotlib.pyplot as plt
AND = np.logical_and
XOR = np.logical_or


"""
pads a 2d numpy array with zeros, and then shifts the
data within that array in the desired direction.
using shiftdirection="center" will skip the shifting
step.
"""
def shift(data,shiftdirection = "center"):
	numshifts = {"right":1,"left":1,"up":1,"down":1}
	
	shiftfuncs = {
		"right": lambda arr:np.hstack((zerocol(outarr),outarr)),
		"left": lambda arr: np.hstack((outarr,zerocol(outarr))),
		"up": lambda arr: np.vstack((outarr,zerorow(outarr))),
		"down": lambda arr: np.vstack((zerorow(outarr),outarr))
	}

	directionpairs =  \
		{"right":"left","left":"right","up":"down","down":"up"}
			
	if shiftdirection != "center":
		numshifts[shiftdirection] += 1
		numshifts[directionpairs[shiftdirection]] -= 1

	outarr = cp.deepcopy(data)
	zerocol = lambda arr: np.zeros((arr.shape[0],1))
	zerorow = lambda arr: np.zeros((1,arr.shape[1]))

	for direction in numshifts.keys():
		for numtimes in xrange(numshifts[direction]):
			outarr = shiftfuncs[direction](outarr)

	return outarr
		
"""
given a 2d numpy array, will find hot pixels and find the center
of the object in the data.
returns the coordinates of the center, the approximate radius, 
and the hot pixel mask (a boolean 2d numpy array).
"""
def process(data, numstd = 3, radiusscale = 2):

	directions = ["up","down","left","right"]
	dimx,dimy = data.shape

	threshold = np.mean(data) + numstd*np.std(data)

	datapadded = shift(data,"center")
	M = (datapadded > threshold)

	Ms = [(shift(data,direction) > threshold) for direction in directions]
	Mhots = [XOR(M,m) for m in Ms]

	Mobj = cp.deepcopy(M)
	Mhot = np.array(np.ones(datapadded.shape),dtype = np.bool_)
	for m,mhot in zip(Ms,Mhots):
		Mhot = AND(Mhot, mhot )
		Mobj = AND(Mobj, m)

	xs,ys = Mobj.nonzero()
	centerx,centery = np.median(xs),np.median(ys)
	distances = np.sqrt((xs-centerx)**2 + (ys - centery)**2)

	#maxovermean comes directly from:
	#	r_mean = integral(r*f(r))/integral(f(r))
	#	where f(r)=2*pi*r

	maxovermean = 1.5
	robj = int(np.mean(distances)*maxovermean*radiusscale)

	Mhot = Mhot[1:dimx+1,1:dimy+1]
	return centerx,centery,robj,Mhot

filename = "./keckdata_orig/n0038.fits"
fits = pf.open(filename, ignore_missing_end=True)[0].data
print 'process(fits) ',process(fits)

filename = "./keckdata_orig/n0039.fits"
fits = pf.open(filename, ignore_missing_end=True)[0].data
print 'process(fits) ',process(fits)
filename = "./keckdata_orig/n0040.fits"

fits = pf.open(filename, ignore_missing_end=True)[0].data
print 'process(fits) ',process(fits)
