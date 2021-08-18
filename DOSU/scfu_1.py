import os
import sys

import re
from pymatgen.core import structure
from pymatgen.ext.matproj import MPRester
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import numpy as np
import subprocess
import pandas as pd
import math

from Base.Symmetry import symmetrize, equiv_atoms
from Base.Pseudos import Pseudos
from Base.PBS_maker import pbs_submit
import Base.DOS_QE_set as qe_input
from Base.Elements import transition_metal_elements

from ase.io import read, write
from Utils.whether_DFTU import *
from Utils.Parser import hp_parser, pw_parser
from Utils.Hubbard import initialize_hubbard, insert_hubbard_block, reorder

#==============================================================================#
#  Density of States SCF calculation using DFT+U                               #
#==============================================================================#

def get_structure_from_mp(MP_ID) -> str:
    """
    Obtain a crystal from the MP database via the API.

    Args: formula (str): A formula

    Returns: (Structure) the lowest energy structure on the Convex hull form MP
    database and its material_id
    """
    m = MPRester("N7AIm1s2v43BQ6FT")
    pymat0 = m.get_structure_by_material_id(MP_ID, final=False, conventional_unit_cell=False)
    pymat = SpacegroupAnalyzer(pymat0, symprec=0.01, angle_tolerance=5.0)
    pymat_s = pymat.get_symmetrized_structure()
    formula = pymat_s.formula
    formula = "".join(formula.split(" "))


    return pymat_s, formula

def mk_final_scfu_folder(chem_form,MP_ID,dftu_type = "All") -> str:
    """
    Making folder fo SCFU calculations, the validation of vc-relax is also
    performed.

    Args: Chemical formula for creating folder.
    Returns:
    """
    if dftu_type == "All":
        hp_folder_name = "scfu_dos"
    elif dftu_type == "TM_only":
        hp_folder_name = "dos_scf_TM"
    else:
        raise ValueError("Invalid DFTU type")
    os.chdir('../')
    if os.path.isdir(chem_form + '_' + MP_ID):

        whether_DFTU(chem_form, dftu_type = dftu_type)#--Check do we need DFTU

        os.chdir(chem_form + '_' + MP_ID)

        os.chdir('hp')

        res_dict = hp_parser()

        if res_dict['status'] == "DONE":
            os.chdir('../')

            if not os.path.isdir(hp_folder_name):
                os.mkdir(hp_folder_name)
                os.chdir(hp_folder_name)
                os.mkdir('tmp')
            else:
                raise FileExistsError("Duplicate folder created")
    else:
        raise FileNotFoundError("Folder did not create.")

    return res_dict

def get_scfu_structures():
    """
    Obtain relaxed structure from vc-relax calculations
    (Validation of vc-relax is performed in mk_folder func.)

    Args:
    Returns: (ASE_Structure)
    """
    ase_S = read("../first_scfu/dftu.in", format='espresso-in')
#    nbnd = pw_parser(fname = "../first_scfu/dftu.out")['nbnd']
    return ase_S


def ase_input_generator(ase_S, res, non_sym_elements, hubbard_list, dftu_type = "All"):
    """
    Using ASE write functions for generate input
    Args: (reordered ASE Structure) ase_S
          (Int) number of bands in the calculation
          (Str) dftu_type ("All" or "TM_only")
          (Dict) Dictionary contains the hubbard DFTU list

    Returns: Input files for Quantum Espresso final SCFU calculations
    """

    SCF_input = qe_input.scfu()

    pymat_S = AseAtomsAdaptor.get_structure(ase_S)
    #-- still needs to be reordered depends on the dftu_type

    if dftu_type == "All":
     #   SCF_input['SYSTEM']['nbnd'] = nbnd
        SCF_input['SYSTEM'].update(insert_hubbard_block(hubbard_list))
        pseudos = Pseudos(pymat_S)
        converted_ase_S = AseAtomsAdaptor.get_atoms(pymat_S)

    elif dftu_type == "TM_only":
        hubbard_list_iterator = hubbard_list.copy() #--avoid size change during iteration
        for kind in hubbard_list_iterator:
            if kind not in transition_metal_elements():
                hubbard_list.pop(kind)
      #  SCF_input['SYSTEM']['nbnd'] = nbnd
        SCF_input['SYSTEM'].update(insert_hubbard_block(hubbard_list))
        converted_pymat_S = reorder(pymat_S, hubbard_list)
        pseudos = Pseudos(converted_pymat_S)
        converted_ase_S = AseAtomsAdaptor.get_atoms(converted_pymat_S)


    #--update the SYSTEM card with smearing settings
    #SCF_input['SYSTEM']['occupations'] = 'smearing'
    #SCF_input['SYSTEM']['smearing'] = 'mv'
    #SCF_input['SYSTEM']['degauss'] = 0.005


    write("dftu.in", converted_ase_S, format = "espresso-in", \
          pseudopotentials=pseudos, input_data = SCF_input, kspacing=0.04)

    if len(res) != 0:
        file = open('dftu.in', 'r')
        list_of_lines = file.readlines()

        res_num = dict()
        for i,value in enumerate(non_sym_elements):
            counter = 0
            for key in res.keys():
                if (key[:-1] == value and key[-1].isdigit()==True) or (key[:-2] == value and key[-2:].isdigit()==True):
                    counter += 1
            res_num[value] = counter
        res_new = dict()

        for key in res.keys():
            value = res[key]
            for n in range(len(value)):
                res_new[value[n]] = key

        res_list = []
        res_new = dict(sorted(res_new.items(), key=lambda item:item[0]))
        for key in res_new.keys():
            res_list.append(res_new[key])

        for i,line in enumerate(list_of_lines):

            if 'ntyp' in line:
                ntyp = int(line.split('=')[1])
                new_ntyp = ntyp + len(res) - len(non_sym_elements)
                ntyp_s = str(ntyp)
                new_ntyp_s = str(new_ntyp)
                #line.replace(ntyp_s, new_ntyp_s)   works in Python 3 but not 2.6
                line = ''.join(line.split('=')[:-1]) + '= ' +  new_ntyp_s + '\n'
                list_of_lines[i] = line

            if "ATOMIC_SPECIES" in line:
                ind1 = i
            if "K_POINTS" in line:
                ind2 = i
                counter = 0
                for n,line in enumerate(list_of_lines[ind1:ind2]):
                    for k, value in enumerate(non_sym_elements):
                        if value in res_list:
                            break
                        elif value in line.split(" "):
                            for l in range(0,res_num[value]):
                                if l == 0:
                                    line0 = ''.join(line.split(" ")[0]) + '0 ' + ' '.join(line.split(" ")[1:])
                                    list_of_lines[ind1+n+counter] = line0
                                elif l > 0:
                                    linel = ''.join(line.split(" ")[0]) + '{} '.format(l) + ' '.join(line.split(" ")[1:])
                                    list_of_lines.insert(ind1+n+1+counter,linel)
                                    counter += 1

                non_sym_chunk = [x for x in list_of_lines[(ind1+1):ind2] if (x.split(" ")[0][-1].isdigit() == True) or (x.split(" ")[0][-2:].isdigit() == True)]
                non_U_chunk = [x for x in list_of_lines[(ind1+1):ind2] if (x.split(" ")[0][-1].isdigit() == False) and (x.split(" ")[0][-2:].isdigit() == False)]
                non_sym_chunk.extend(non_U_chunk)
                list_of_lines[(ind1+1):ind2] = non_sym_chunk

            if "ATOMIC_POSITIONS" in line:
                ind3 = i
                counter = 0
                for n, line in enumerate(list_of_lines[ind3:]):
                    for k, value in enumerate(non_sym_elements):
                        if counter == len(res_list):
                            break
                        elif value in line.split(" "):
                            if value in res_list:
                                break
                            else:
                                line = str(res_list[counter]) + ' ' + ' '.join(line.split(" ")[1:])
                                list_of_lines[ind3+n] = line
                                counter += 1

                non_sym_chunk = [x for x in list_of_lines[(ind3+1):] if (x.split(" ")[0][-1].isdigit() == True) or (x.split(" ")[0][-2:].isdigit() == True)]
                non_U_chunk = [x for x in list_of_lines[(ind3+1):] if (x.split(" ")[0][-1].isdigit() == False) and (x.split(" ")[0][-2:].isdigit() == False)]
                non_sym_chunk.extend(non_U_chunk)
                list_of_lines[(ind3+1):] = non_sym_chunk


        file = open('dftu.in', 'w')
        file.writelines(list_of_lines)
        file.close()






mpid=input('enter the mpid: ')

def main():

    #Read DMREF materials list CSV
    dftu_type = "All"

    mp_structure, formu = get_structure_from_mp(mpid)

    results = mk_final_scfu_folder(formu,mpid, dftu_type = dftu_type)
    res, non_sym_elements = equiv_atoms(mp_structure)
    ase_structure = get_scfu_structures()

    ase_input_generator(ase_structure, res, non_sym_elements, results['dftu'], dftu_type)
    submit_name = str(formu)+'_scfu.pbs'

    print('submitting '+submit_name)

    pbs_submit("pw",1,submit_name)


if __name__=="__main__":

    main()
