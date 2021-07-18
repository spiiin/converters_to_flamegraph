# converters_to_flamegraph
Scripts for converts profilers output to flamegraph

Flamegraphs - https://github.com/brendangregg/FlameGraph

My versions of scripts to convert profiler output to folded stacks (other are staled or don't work for me).

# Pipeline

## Windows

1. Collect data with [EtwProf](https://github.com/Donpedro13/etwprof). Others profilers thar produce etl files are good too.

`etwprof profile -t=418996 --output profile_result -m`

This file can be opened with [Windows Performance Analyze](https://www.microsoft.com/en-us/p/windows-performance-analyzer/9n0w1b2bxgnz?activetab=pivot:overviewtab).
It can show data as flamegraph, but I want to produce svg too.

2. Transform etl file in csv
`xperf -i "profile.etl" -o perf.csv -target machine -symbols`

3. Convert csv to folded_stacks format
(it convert perf.csv to perf.folded)

`xperf_csv_to_collapsed_stacks.py`

4. Run flamegraph.pl for convert folder stacks to svg file

`flamegraph.pl perf.folded > perf.svg`

It can be opened with any modern browser.

## macOS/iOS

1. Profile application with Instruments -> Time profile. Select range of data that need to be exported. 
2. (!) Choose profile output columns - number of samples, symbols. Disable all other columns
3. Select row that you want to export (root node for export all data). (!) Do not select all rows, just root.
![macosx](https://user-images.githubusercontent.com/1622049/126062333-b2cfed5b-894f-4a1b-b26a-d1e502c99cc0.png)

4. Copy data (select Edit->Deep Copy from menu) and paste it to any text editor. Save file as sample.txt
5. Run `instruments_to_collapsed_stacks.py`
6.  Run flamegraph.pl for convert folder stacks to svg file

`flamegraph.pl perf.folded > perf.svg`




