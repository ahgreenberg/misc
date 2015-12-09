import decorators as dc

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#first example demonstrating the timing info and memoization decorators
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@dc.memoize
def sqrt(key):
	eps = 1E-10
	low,mid,high = 0,key/2.,key
	while abs(mid*mid-key)>eps:
		if mid*mid<key:
			low = mid
		else:
			high = mid
		mid = (low+high)/2.
	return mid

@dc.timeinfo
def randomSqrts(iterations = int(7E5)):
	import random as rd
	rd.seed(1)
	total = 0
	for i in range(iterations):
		key = rd.randrange(20)
		total += sqrt(key)
	return total

def example1():
	print "@dc.timeinfo makes it easy to time a function."
	randomSqrts()
	print "Wow! See how fast that was? Now try rerunning"
	print "this code with the @dc.memoize line removed"
		
print "-"*20,"\nexample 1\n","-"*20
example1()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# second example, demonstrating the encrypt/decrypt decorators
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def dencrypt(val, key = 82760182):
	import math
	binlength = lambda x: int(math.ceil(math.log(x,2)))
	assert(type(val)==type(key)==type(1))
	keybase = key
	while binlength(key)<binlength(val):
		key += keybase<<binlength(key)
	return key^val
	
@dc.encryptoutput(dencrypt)
def add(a,b):
	return a+b

@dc.decryptinput(dencrypt)
def square(a):
	return a*a

def example2():
	print "I want to calculate (103+37)^2, but I don't want anyone"
	print "to see what the interim step (103+37) is equal to"
	print "so I'll use my encrypted functions!\n"
	print "\tsquare(add(103,37)) = ",square(add(103,37))
	print "Note:\n\t(103+37)^2 = ",(103+37)**2,"\n"
	print "but\n\tadd(103,37) = ",add(103,37)
	print "and\n\t103+37 = ", 103+37
	print "\nThis is beacuse the add function encrpyted its output"
	print "so only a function with the decryption decorator"
	print "(like square) can use the result."

print "\n\n","-"*20,"\nexample 2\n","-"*20
example2()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#third example, showing how outtofile decorator can be used to easily log function outputs
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@dc.outtofile("/tmp/pylog")
def example3():
	print "big ass important calculation!"
	print "don't worry -- it's been saved"
	print "to the log file at /tmp/pylog"
	x = 6*7
	return x

print "\n\n","-"*20,"\nexample 3\n","-"*20
example3()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#fourth example, showing implementation of a basic type system for function parameters
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@dc.accepts(int,int,str)
@dc.returns(int)
def example4(a,b,c):
	print "try changing the call signature to example4(1,1,1)"
	print "or try changing the return statement to 'return a+b,c'"
	print "a =",str(a),",b =",str(b),",c =",c
	return a+b

print "\n\n","-"*20,"\nexample 4\n","-"*20
print example4(1,1,"a")
