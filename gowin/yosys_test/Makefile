
PROJ=top

all: impl/pnr/${PROJ}.fs

impl/synth/${PROJ}.vg: ${PROJ}.v
	# Step 1: Synthesize with vendor tool
	# mkdir -p impl/synth
	# ${GOWINHOME}/IDE/bin/GowinSynthesis -i $< -o impl/synth/${PROJ}.vg
	#####################
	# Step 1: Synthesize with yosys
	mkdir -p impl/synth
	yosys -l impl/synth/top.rpt top.ys


impl/pnr/${PROJ}.fs: impl/synth/${PROJ}.vg
	# Step 2: PnR
	LD_LIBRARY_PATH=${GOWINHOME}/Programmer/bin ${GOWINHOME}/IDE/bin/gw_sh run.tcl

prog: impl/pnr/${PROJ}.fs
	openFPGALoader -m -b tangnano $<

clean:
	rm -rf impl
.PHONY: clean
