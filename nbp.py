import pyfits as pf
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

def nixBadPix(filename = "", numstd = 1, smoothhotpix = True, radiusscale = 2):
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

	outfile = filename[:filename.rfind(".")]
	AND = np.logical_and


	fits = pf.open(filename,ignore_missing_end=True)
	data = fits[0].data

	mn = np.mean(data)
	std = np.std(data)

	threshold = mn + numstd*std

	datapadded = shift(data,"center")
	M = (datapadded > threshold)

	sup = shift(data,"up") 
	sdown = shift(data,"down") 
	sleft = shift(data,"left") 
	sright = shift(data,"right") 

	localmean = (sup+sdown+sleft+sright)/4.

	M1 = (sup > threshold)
	M2 = (sdown > threshold)
	M3 = (sleft > threshold)
	M4 = (sright > threshold)

	Ms = [M1,M2,M3,M4]
	Mhots = [np.logical_xor(M,m) for m in Ms]

	Mobj = cp.deepcopy(M)
	Mhot = np.array(np.ones(datapadded.shape),dtype = np.bool_)
	for m,mhot in zip(Ms,Mhots):
		Mhot = np.logical_and(Mhot, mhot )
		Mobj = np.logical_and(Mobj, m)

	hotxs,hotys = Mhot.nonzero()

	for x,y in zip(hotxs,hotys):
		data[x-1][y-1] = localmean[x][y] if smoothhotpix else mn

	fits.writeto(outfile+"_nohot.fits", clobber = True)

	xs,ys = Mobj.nonzero()
	centerx,centery = np.median(xs),np.median(ys)
	print 'centerx,centery ',centerx,centery
	distances = np.sqrt((xs-centerx)**2 + (ys - centery)**2)


	#maxovermean comes directly from:
	#	r_mean = integral(r*f(r))/integral(f(r))
	#	where f(r)=2*pi*r

	maxovermean = 1.5
	robj = int(np.mean(distances)*maxovermean*radiusscale)
	print 'max radius of obj in pixels: ',robj

	fits[0].data = datapadded[centerx-robj:centerx+robj,centery-robj:centery+robj]

	fits.writeto(outfile+"_cropped.fits", clobber = True)

numstd = 3
smoothhotpix = True
radiusscale = 2

filename = "./keckdata_orig/n0038.fits"
nixBadPix(filename, numstd = numstd, smoothhotpix = smoothhotpix, radiusscale = radiusscale)
filename = "./keckdata_orig/n0039.fits"
nixBadPix(filename, numstd = numstd, smoothhotpix = smoothhotpix, radiusscale = radiusscale)
filename = "./keckdata_orig/n0040.fits"
nixBadPix(filename, numstd = numstd, smoothhotpix = smoothhotpix, radiusscale = radiusscale)
