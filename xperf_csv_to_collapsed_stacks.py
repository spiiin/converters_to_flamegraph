"""
example input:
   Stack,   11726350,     404904, MyProc.exe!WinMain, MyProc.exe!invoke_main, MyProc.exe!__scrt_common_main_seh, MyProc.exe!__scrt_common_main, MyProc.exe!WinMainCRTStartup, kernel32.dll!BaseThreadInitThunk, ntdll.dll!__RtlUserThreadStart, ntdll.dll!_RtlUserThreadStart
"""

#TODO: cmd arguments
INPUT_FILE = "perf.csv"
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
for line in lines:
	parts = line.split(",")
	if len(parts) < 4:
		continue
	if parts[0].strip() == "Stack" and parts[1].strip().isdigit():
		out_line = ";".join([escape_symbols(l) for l in parts[:2:-1]])
		out_dict[out_line] = out_dict.get(out_line, 0) + 1

#dump output dict to file
output = []
for key, value in out_dict.items():
	out_line = key + " " + str(value) + "\n"
	output.append(out_line)
with open(OUTPUT_FILE, "wt") as f:
	f.writelines(output)