#!bin/bash
# ================================================================================
# run.sh
#
# Bash script wrapper for python code to test Cirq's XmonSimulator performance.
#
# written by Ryan LaRose <laroser1@msu.edu>
# at Michigan State University August 2018.
# ================================================================================

# ============
# outfile name 
# ============

today=`date '+%Y_%m_%d_%H_%M_%S'`;
outfname="timing_$today.txt"

# ============
# main testing
# ============

for n in 10 12 14 16 18 20 22
do
    for depth in 10 20 30 40 50
    do
        python sim_test.py $n $depth 1 >> timing/$outfname
    done
done
