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
#  DOS calculation                                                             #
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

def mk_dos_folder(chem_form, MP_ID) -> str:
    """
    Making folder for dos calculations, the validation of nscf is also
    performed.
    tmp folder is copied from nscf to pdos

    Args: Chemical formula for creating folder.
    Returns:
    """
   # if os.path.isdir(chem_form):
    if os.path.isdir(chem_form + '_' + MP_ID):

       # os.chdir(chem_form)
        os.chdir(chem_form + '_' + MP_ID)
        os.chdir('nscf')
        tmpsrc=os.getcwd()+"/tmp"

        res_dict = pw_parser()

        if res_dict['status'] == "DONE":
            os.chdir('../')
            os.mkdir('dos')
            os.chdir('dos')
            tmpdes=os.getcwd()+"/tmp"
            shutil.copytree(tmpsrc,tmpdes)
    else:
        raise FileNotFoundError("Folder is not created.")

    return res_dict

mpid=input('enter the mpid: ')

def main():
    mp_structure, formu = get_structure_from_mp(mpid)
    mk_dos_folder(formu, mpid)#--create folder
    submit_name = str(formu)+'_dos.pbs'
    emin,emax=ff.FindMinMax() #finds the fermi energy +/- 20 to get energy range for DOS calculation
    os.chdir('../dos')
    qe_input.dos(formu,emin,emax) #create the dftu.in file for dos calculation
    print('submitting '+submit_name)
    pbs_submit("dos",1,submit_name)

if __name__=="__main__":
    main()
