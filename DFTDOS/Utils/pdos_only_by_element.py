#! /usr/bin/python

import sys
import os
import re
import glob
import numpy
from matplotlib.pyplot import *

def color_by_ele(formula):
    filelist = glob.glob("*wfc*")
    Compiled = []
    VBM = -1000
    CBM = 1000
    nscfout = open('dftu.out','r')
    for i in nscfout:
        if 'Fermi' in i:
            fermi = float(i.split()[4])
    nscfout.close()
    filekey = open('./color_by_element.key','r')
    colorkey = []
    colorkey = {'null' : 12345}
    for i in filekey:
        colorkey[i.split()[0]] = i.split()[1]
    filekey.close()
    for filename in filelist:
	#print filename
        contents = open(filename,"r")
        dummyvariable = contents.readline()
        DOS = []
        Energy = []
        LDOS = []
        for line in contents:
            DOStemp = line.split()
            DOStemp = [float(x) for x in DOStemp]
            DOStemp[0] -= fermi
            DOS.append(DOStemp)
            Energy.append(DOStemp[0])
            LDOS.append(DOStemp[1])
        centerpoint = Energy.index(min(x for x in Energy if x > 0))
        for i in range(centerpoint, len(Energy)):
            if LDOS[i] > 0 and LDOS[i+1]>0 and LDOS[i+2]>0:
                ConductionBandPoint = i
                break
        for i in range(centerpoint,0,-1):
            if LDOS[i] >0 and LDOS[i-1] >0 and LDOS[i-2] > 0:
                ValenceBandPoint = i
                break
        if Energy[ValenceBandPoint] > VBM:
            VBM = Energy[ValenceBandPoint]
        if Energy[ConductionBandPoint] < CBM:
            CBM = Energy[ConductionBandPoint]
        Bandgap = abs(Energy[ValenceBandPoint]-Energy[ConductionBandPoint])
        Compiled.append([filename,Energy[ValenceBandPoint],Energy[ConductionBandPoint],Bandgap])
        specie = filename[filename.find("(")+1:filename.find(")")]
        for i,eng in enumerate(Energy):
            Energy[i]=eng-VBM
        plot(Energy, LDOS, colorkey[specie])
        contents.close()
        plot(Energy, LDOS, colorkey[specie])
        contents.close()
    #print("Name\tVBM\tCBM\tBandGap")
    #for i in Compiled:
        #print(i[0],"\t",i[1],"\t",i[2],"\t",i[3])
    Bandgap = abs(VBM-CBM)
    print("Totals:\tVBM\tCBM\tBandgap")
    print("\t",VBM,"\t",CBM,"\t",Bandgap)
    #print(fermi)
    xlim(-10,10)
    ylim(0,5)
    xlabel('Energy (E-$\mathrm{E_{VBM}}$)', size='large')
    ylabel('PDOS (arb. units)', size='large')
    savefig(str(formula)+'_DOS_by_element.png')
    savefig(str(formula)+'_DOS_by_element.svg')
    show()

