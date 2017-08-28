#!/usr/bin/env python3

# a1l_t4b135_R_oR5
# 61316c5f7434623133355f525f6f5235

import sys, os
import deadpool_dfa
import phoenixAES

def processinput(iblock, blocksize):
    return (bytes.fromhex('%0*x' % (2*blocksize, iblock)), ["--stdin"])

def processoutput(output, blocksize):
    i = int(b''.join([x for x in output.split()]), 16)
    return i


# Initial attack attempt:
engine=deadpool_dfa.Acquisition(targetbin='./wb_patched', targetdata='./wb_data', goldendata='./mem.dump',
       dfa=phoenixAES, processinput=processinput, processoutput=processoutput,
       maxleaf=0x100, minleaf=0x1, minleafnail=0x1,
    )
tracefiles_sets=engine.run()
for tracefile in tracefiles_sets[0]:
    if phoenixAES.crack(tracefile, verbose=1):
        break
