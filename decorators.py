import numpy as np
import collections as cl
import time

#decorator
def accepts(*decargs,**deckwargs):
	def acceptdecorator(func):
		typeName = lambda x: str(x)[str(x).find("'")+1:str(x).rfind("'")]
		def wrappedfunc(*args,**kwargs):
			match,typesreqstr,typesgivenstr = True,"",""
			for decarg,arg in zip(decargs,args):
				typesreqstr += typeName(decarg)+", "
				typesgivenstr += typeName(type(arg))+", "
				if decarg!=type(arg):
					match=False
			for key in kwargs:
				if key in deckwargs:
					typesreqstr += ("%s = %s, ")%(key,typeName(deckwargs[key]))
					typesgivenstr += ("%s = %s, ")%(key,typeName(type(kwargs[key])))
					if deckwargs[key]!=type(kwargs[key]): match=False
			typesreqstr = typesreqstr[:-2]
			typesgivenstr = typesgivenstr[:-2]
			if not match:
				message = ("\nArgument types were:\n\t%s\nRequired types were:\n\t%s\n")%(typesgivenstr,typesreqstr)
				raise Exception(message)
			return func(*args,**kwargs)
		return wrappedfunc
	return acceptdecorator

#decorator
def returns(*dargs):
	def returnsdecorator(func):
		def typeName(x):
			x = str(x)
			if x == "None": return x
			return x[x.find("'")+1:x.rfind("'")]
		def wrappedfunc(*args,**kwargs):
			outs = func(*args,**kwargs)
			swap = False
			try: len(outs)
			except Exception as e: outs,swap = [outs],True
			match,typesreqstr,typesgivenstr = True,"",""
			if len(outs) != len(dargs): match = False
			if match: match = all([type(out)==darg for out,darg in zip(outs,dargs)])
			for out in outs: typesgivenstr += typeName(type(out))+", "
			for darg in dargs: typesreqstr += typeName(darg)+", "
			typesreqstr = typesreqstr[:-2]
			typesgivenstr = typesgivenstr[:-2]
			if not match:
				message = (
				"\nReturned types were:\n\t%s\nRequired types were:\n\t%s\n")%(typesgivenstr,typesreqstr)
				raise Exception(message)
			return outs if not swap else outs[0]
		return wrappedfunc
	return returnsdecorator


#decorator
def timeinfo(func):
	def wrappedfunc(*args,**kwargs):
		print "\nfunc: ", func.__name__
		if len(args):
			print "args:"
			print "\n\t".join([str(arg) for  arg in args])
		if len(kwargs):
			print "kwargs:"
			print "\n\t".join( [ ("%s: %s")%(key,val) for key,val in zip(kwargs.keys(),kwargs.values())])
		start = time.time()
		out = func(*args, **kwargs)
		print "time: ",time.time()-start," s\n"
		return out
	return wrappedfunc


#decorator
def memoize(func):
	cache = dict()
	def wrapped(key = object()):
		if key not in cache:
			cache.update({key:func(key)})
		return cache[key]
	return wrapped

#decorator
def statistics(*statfuncs):
	def statdecorator(func):
		results = cl.deque([])
		def wrappedfunc(*args, **kwargs):
			output = func(*args,**kwargs)
			results.append(output)
			return output,[statfunc(results) for statfunc in statfuncs]
		return wrappedfunc
	return statdecorator

#decorator
def filehandling(func):
	import os
	def wrappedfunc(*args,**kwargs):
		if "filename" in kwargs.keys():
			filename = kwargs["filename"]
			if not os.path.exists(filename):
				file(filename,"w").close()
		return func(*args,**kwargs)
	return wrappedfunc

#decorator
def decryptinput(decryptfunc):
	def decryptdecorator(func):
		def wrappedfunc(inputval):
			return func(decryptfunc(inputval))
		return wrappedfunc
	return decryptdecorator

#decorator
def encryptoutput(encryptfunc):
	def encryptdecorator(func):
		def wrappedfunc(*args,**kwargs):
			funcout = func(*args,**kwargs)
			return encryptfunc(funcout)
		return wrappedfunc
	return encryptdecorator

#decorator
def outtofile(filename = "/tmp/pylog"):
	def outdecorator(func):
		def wrappedfunc(*args,**kwargs):
			output = func(*args,**kwargs)
			handle = file(filename,"a")
			handle.write(("%s\t\t%s\n")%(func.__name__,str(output)))
			handle.close()
			return output
		return wrappedfunc
	return outdecorator

