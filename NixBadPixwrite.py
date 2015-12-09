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
		
def process(filename, numstd = 3, smoothhotpix = True, radiusscale = 2, writeout = True, cropwithouthot = True):

	directions = ["up","down","left","right"]

	outfile = filename[:filename.rfind(".")]

	fits = pf.open(filename,ignore_missing_end=True)
	data = fits[0].data

	mn = np.mean(data)
	std = np.std(data)
	threshold = mn + numstd*std

	datapadded = shift(data,"center")
	M = (datapadded > threshold)

	dshifts = [shift(data,direction) for direction in directions]
	localmean = np.array(np.sum(dshifts,axis=0)/4.)

	Ms = [(dshift > threshold) for dshift in dshifts]
	Mhots = [XOR(M,m) for m in Ms]

	Mobj = cp.deepcopy(M)
	Mhot = np.array(np.ones(datapadded.shape),dtype = np.bool_)
	for m,mhot in zip(Ms,Mhots):
		Mhot = AND(Mhot, mhot )
		Mobj = AND(Mobj, m)

	hotxs,hotys = Mhot.nonzero()
	for x,y in zip(hotxs,hotys):
		if cropwithouthot: datapadded[x][y] = localmean[x][y] if smoothhotpix else mn
		fits[0].data[x-1][y-1] = localmean[x][y] if smoothhotpix else mn

	if writeout: fits.writeto(outfile+"_nohot.fits", clobber = True)

	xs,ys = Mobj.nonzero()
	centerx,centery = np.median(xs),np.median(ys)
	distances = np.sqrt((xs-centerx)**2 + (ys - centery)**2)

	#maxovermean comes directly from:
	#	r_mean = integral(r*f(r))/integral(f(r))
	#	where f(r)=2*pi*r

	maxovermean = 1.5
	robj = int(np.mean(distances)*maxovermean*radiusscale)

	fits[0].data = datapadded[centerx-robj:centerx+robj,centery-robj:centery+robj]

	if writeout: fits.writeto(outfile+"_cropped.fits", clobber = True)
	return centerx,centery,robj

filename = "./keckdata_orig/n0038.fits"
fits = pf.open(filename, ignore_missing_end=True)[0].data
print 'process(fits) ',process(filename)

filename = "./keckdata_orig/n0039.fits"
fits = pf.open(filename, ignore_missing_end=True)[0].data
print 'process(fits) ',process(filename)
filename = "./keckdata_orig/n0040.fits"

fits = pf.open(filename, ignore_missing_end=True)[0].data
print 'process(fits) ',process(filename)
