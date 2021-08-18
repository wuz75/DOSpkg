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
import Base.DOS_QE_set as qe_input
from ase.io import read, write
from Utils.Parser import pw_parser

#==============================================================================#
#  NSCF calculation for Density of States Calculations                         #
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

def mk_nscf_folder(chem_form, MP_ID) -> str:
    """
    Making folder for nscf calculations, the validation of scf is also
    performed.

    Args: Chemical formula for creating folder.
    Returns:
    """
    if os.path.isdir(chem_form + '_' + MP_ID):

        os.chdir(chem_form + '_' + MP_ID)
        os.chdir('scf')
        tmpsrc=os.getcwd()+"/tmp"

        res_dict = pw_parser()

        if res_dict['status'] == "DONE":
            os.chdir('../')
            os.mkdir('nscf')
            os.chdir('nscf')
            tmpdes=os.getcwd()+"/tmp"
            shutil.copytree(tmpsrc,tmpdes)
    else:
        raise FileNotFoundError("Folder is not created.")

    return res_dict

def input_generator(S):
    """
    Using ASE write functions for generate raw structures
    Args: (Pymatgen Structure)
    Returns: Input files for Quantum_espress nscf calculation 
    """
    pseudos = Pseudos(S)
    nscf = qe_input.nscf()
    ase_S = AseAtomsAdaptor.get_atoms(S)
    write("dftu.in", ase_S, format = "espresso-in", \
          pseudopotentials=pseudos, input_data = nscf, kspacing=0.04)

mpid=input('enter the mpid: ')

def main():
    mp_structure, formu = get_structure_from_mp(mpid)
    mk_nscf_folder(formu, mpid)#--create folder
    submit_name = str(formu)+'_nscf.pbs'
    print('submitting '+submit_name)
    input_generator(mp_structure)

    pbs_submit("pw",1,submit_name)

if __name__=="__main__":
    main()

