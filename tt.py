import pyfits as pf
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

AND = np.logical_and

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

filename = "./keckdata_orig/n0060.fits"

fits = pf.open(filename,ignore_missing_end=True)
data = fits[0].data
dl1 = np.hstack((data,np.zeros((data.shape[0],1))))

mn = np.mean(data)
std = np.std(data)

threshold = mn + std


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

Ms = [np.logical_and(M,M1),np.logical_and(M,M2),np.logical_and(M,M3),np.logical_and(M,M4)]


objpix = (datapadded > threshold)
for mask in Ms:
	objpix = np.logical_and(objpix, (sup > threshold))

xs,ys = objpix.nonzero()

centerx,centery = np.median(xs),np.median(ys)
distances = np.sqrt((xs-centerx)**2 + (ys - centery)**2)

print 'np.mean(distances) ',np.mean(distances)
print 'np.median(distances) ',np.median(distances)
print 'np.std(distances) ',np.std(distances)

objsize = int(np.std(distances))


fits[0].data = datapadded[centerx-objsize:centerx+objsize,centery-objsize:centery+objsize]

fits.writeto("./test.fits", clobber = True)
