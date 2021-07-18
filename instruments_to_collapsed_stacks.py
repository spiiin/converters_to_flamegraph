"""
example input:
# Samples	Symbol Name
13369	my_proccess (524)
12045	 start
12045	  main
12045	   UIApplicationMain
12045	    GSEventRunModal
12045	     CFRunLoopRunSpecific
12045	      __CFRunLoopRun
11976	       __CFRunLoopDoSource1
"""

from itertools import takewhile

#TODO: cmd arguments
INPUT_FILE = "samples.txt"
OUTPUT_FILE = "perf.folded"

#read input file
with open(INPUT_FILE, "rt") as f:
	lines = f.readlines()

#escape special symbols
def escape_symbols(stackSummary):
	stackSummary = stackSummary.strip()
	# Escape symbols
	stackSummary = stackSummary.replace(";", ":")
	# Spaces seem like a bad idea also.
	stackSummary = stackSummary.replace(" ", "_")
	# Having single-quote characters in the call stacks gives flamegraph.pl heartburn.
	# Replace them with back ticks.
	stackSummary = stackSummary.replace("'", "`")
	# Double-quote characters also cause problems. Remove them.
	stackSummary = stackSummary.replace('"', "")
	# Remove <PDB_not_found> labels
	stackSummary = stackSummary.replace("<PDB_not_found>", "Unknown")
	return stackSummary

#collect data to output dict
out_dict = {} #OrderedDict()
func_stack = []

for line in lines[1:]:
	parts = line.split("\t")
	if len(parts) < 2:
		continue
	samples = parts[0]
	funcName =  escape_symbols(parts[1].strip())
	funcDepth = len(list(takewhile(lambda x: x==" ", parts[1])))
	while len(func_stack) > 0:
		prevFuncName, prevFuncDepth = func_stack[-1]
		if funcDepth > prevFuncDepth:
			#make full stack name
			fullName = ""
			for stackName, _ in func_stack:
				fullName = fullName + ";" + stackName
			out_dict[fullName] = samples
			break
		else:
			#pop previous value
			func_stack.pop()
	else:
		pass #if func_stack was empty
	#append new func to func_stack
	func_stack.append((funcName, funcDepth))

#dump output dict to file
output = []
for key, value in out_dict.items():
	out_line = key + " " + str(value) + "\n"
	output.append(out_line)
with open(OUTPUT_FILE, "wt") as f:
	f.writelines(output)