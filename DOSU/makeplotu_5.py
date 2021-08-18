import os
import shutil
import sys
import glob
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
from Utils.pdos_only import makeimg
from Utils.pdos_only_by_element import color_by_ele

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

def organize_pwscf(chem_form, MP_ID) -> str:
    """
    Making folder for DOS graphs
    copies the pwscf files into a new folder to create the image
    """
    os.chdir('../')
    if os.path.isdir(chem_form + '_' + MP_ID):

        os.chdir(chem_form + '_' + MP_ID)

        os.chdir('pdos')
        pwscf_all=glob.glob(os.getcwd()+"/pwscf.pdos_*")
        os.chdir('../')
        os.mkdir('img_maker')
        os.chdir('img_maker')
        tmpdes=os.getcwd()
        for tmpsrc in pwscf_all:
            shutil.copy(tmpsrc,tmpdes)
        os.chdir('../nscf')
        shutil.copy('dftu.out','../img_maker/dftu.out')
    else:
        raise FileNotFoundError("Folder is not created.")


mpid=input('enter the mpid: ')


def main():
    mp_structure, formu = get_structure_from_mp(mpid)

    organize_pwscf(formu, mpid)#--moves all pwscf files
    os.chdir('../img_maker')
    shutil.copy('../../DOSU/Utils/color.key','.')
    shutil.copy('../../DOSU/Utils/color_by_element.key','.')
    makeimg(formu)
    color_by_ele(formu)

if __name__=="__main__":
    main()
