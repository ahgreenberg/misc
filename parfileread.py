def readPars(parfile, pardict, nonetypes = {}, delimiter = "=", comment = "#"):
	with open(parfile,'r') as f:
		for line in f.readlines():
			if line[0] == comment: continue
			parname,val = [el.strip() for el in line.split(delimiter)]
			if parname in pardict.keys():
				valtype = nonetypes[parname] if pardict[parname] is None else type(pardict[parname])
				pardict[parname] = valtype(val)
	return pardict

if __name__ == "__main__":
	parfile = "/tmp/test.pars"
	pardict = {	"name":"adam",
			"age":25,
			"height":6.5,
			"married":False,
			"pets":None	}
	nonetypes = { "pets": str }
	pardict = readPars(parfile, pardict, nonetypes)
	x = pardict["pets"]
	print 'x ',x
	print 'x[0] ',x[0]
