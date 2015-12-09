import sys

IMPORT = "import"
cutoffString = lambda string,char: string[:string.find(char)] if char in string else string

infile = "decorators.py" #sys.argv[1]
#outfile = sys.arv[2]

lines = open(infile,'r').readlines()
importlines = [el for el in lines if len(el.strip().split()) and el.strip().split()[0] == IMPORT]

dashes = "\n"+"- "*10+"\n"
outstr = " Python version: %s%s"%(sys.version,dashes)
for el in importlines:
	modules = el.strip()[len(IMPORT):].strip().split(",")

	for module in modules:
		module = cutoffString(module,".")
		module = cutoffString(module," ")
		outstr += " %s: version "%module
		try:
			exec("%s %s"%(IMPORT,module))
			outstr += eval("%s.__version__"%module)
		except:
			outstr += "not applicable"
		outstr += dashes

outstr = outstr[:-1]
outstr = "#"+outstr.replace("\n","\n#")
print outstr


			
