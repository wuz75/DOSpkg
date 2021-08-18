import os
import shutil
import sys
import re
import logging
from pymatgen.core import structure
from pymatgen.ext.matproj import MPRester
from pymatgen.io.pwscf import PWInput
from pymatgen.io.ase import AseAtomsAdaptor

import numpy as np
import subprocess
import pandas as pd

from Base.Pseudos import Pseudos
from Base.PBS_maker import pbs_submit
import Base.FermiFinder as ff
import Base.DOS_QE_set as qe_input
from ase.io import read, write
from Utils.Parser import pw_parser

#==============================================================================#
#  PDOS calculations for generating density of states plots                    #
#==============================================================================#


def get_structure_from_mp(MP_ID) -> str:
    """
    Obtain a crystal from the MP database via the API.

    Args: formula (str): A formula

    Returns: (Structure) the lowest energy structure on the Convex hull form MP
    database and its material_id
    """
    m = MPRester("N7AIm1s2v43BQ6FT")
    pymat_s = m.get_structure_by_material_id(MP_ID, final=False, conventional_unit_cell=False)
    formula = pymat_s.formula
    formula = "".join(formula.split(" "))
    return pymat_s, formula

def mk_pdos_folder(chem_form, MP_ID) -> str:
    """
    Making folder for pdos calculations 
    tmp folder is copied from dos to pdos folder

    Args: Chemical formula for creating folder.
    Returns:
    """
    os.chdir('../')
    if os.path.isdir(chem_form + '_' + MP_ID):

        os.chdir(chem_form + '_' + MP_ID)
        os.chdir('dos')
        tmpsrc=os.getcwd()+"/tmp"

        if 1==1:
            os.chdir('../')
            os.mkdir('pdos')
            os.chdir('pdos')
            tmpdes=os.getcwd()+"/tmp"
            shutil.copytree(tmpsrc,tmpdes)
    else:
        raise FileNotFoundError("Folder is not created.")


mpid=input('enter the mpid: ')

def main():
    mp_structure, formu = get_structure_from_mp(mpid)
    mk_pdos_folder(formu, mpid)#--create folder
    submit_name = str(formu)+'_pdos.pbs'
    print('submitting '+submit_name)
    emin,emax=ff.FindMinMax() #finds +/- 20 of the fermi energy
    os.chdir('../pdos')
    qe_input.pdos(emin,emax) #creates the dftu.in file for pdos
    pbs_submit("pdos",1,submit_name) #creates and submits the pbs file to the cluster
if __name__=="__main__":
    main()
