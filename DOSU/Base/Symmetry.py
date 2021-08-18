import os
import sys
import re
import logging
from pymatgen.core import structure
from pymatgen.ext.matproj import MPRester
from pymatgen.io.pwscf import PWInput
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

import numpy as np
import subprocess
import pandas as pd

from Base.Elements import dftu_elements
from Base.Pseudos import Pseudos
from ase.io import read, write

def symmetrize(pymat_s):
    sp = SpacegroupAnalyzer(pymat_s,symprec=0.0001)
    pymat_s = sp.get_symmetrized_structure()

    return pymat_s

def equiv_atoms(pymat_s):
    res = {}
    sp = SpacegroupAnalyzer(pymat_s,symprec=0.0001)
    equi_atoms_list = sp.get_symmetry_dataset()["equivalent_atoms"]
    uni_atom_list = np.unique(equi_atoms_list)
    specie_string_list = [pymat_s[sym_idx].species_string for sym_idx in uni_atom_list]

    from collections import Counter
    unique_specie_list = []
    specie_counter = Counter(specie_string_list)

    for unique_specie in specie_counter:
        specie_idx = range(specie_counter[unique_specie])
        for postfix in specie_idx:
            unique_specie_list.append(unique_specie + str(postfix))
    
    non_sym_elements = []
    for sym_idx, sym_ion in enumerate(unique_specie_list):
        if (sym_ion[0:-1] in dftu_elements() and sym_ion[-1].isdigit()==True) or (sym_ion[0:-2] in dftu_elements() and sym_ion[-2:].isdigit()==True):
            res[sym_ion] = np.where(equi_atoms_list == uni_atom_list[sym_idx])[0]
            if (sym_ion[0:-1] not in non_sym_elements) and sym_ion[-2:].isdigit()==False:
                non_sym_elements.append(sym_ion[0:-1])
                #print(non_sym_elements)
            elif (sym_ion[0:-2] not in non_sym_elements) and sym_ion[-2:].isdigit()==True:
                non_sym_elements.append(sym_ion[0:-2])
                #print(non_sym_elements)
    #print(non_sym_elements)
    #print(res)

    return res, non_sym_elements

    # cannot update pymat_s with O0, because it is not decided as an element in pymatgen's system

