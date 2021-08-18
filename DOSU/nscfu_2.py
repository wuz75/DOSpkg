import os
import shutil
from pymatgen.ext.matproj import MPRester
from Base.PBS_maker import pbs_submit
from Utils.Parser import hp_parser, pw_parser

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
    os.chdir('../')
    if os.path.isdir(chem_form + '_' + MP_ID):

        os.chdir(chem_form + '_' + MP_ID)
        os.chdir('scfu_dos')
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

def nscf_input():
    """
    Copies dftu.in from scf_dos folder to create nscf dftu.in
    """
    shutil.copy('../scfu_dos/dftu.in','.')
    with open('dftu.in') as file:
        all_lines = file.readlines()
    all_lines[1]="   calculation      = 'nscf'\n"
    f = open('dftu.in','w')
    for line in all_lines:
        f.write(line)
    f.close()

mpid=input('enter the mpid: ')

def main():
    mp_structure, formu = get_structure_from_mp(mpid)
    mk_nscf_folder(formu, mpid)#--create folder
    nscf_input()
    submit_name = str(formu)+'_nscf.pbs'
    print('submitting '+submit_name)

    pbs_submit("pw",1,submit_name)

if __name__=="__main__":
    main()
