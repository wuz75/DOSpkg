import os
import sys

import warnings
from pymatgen.core import structure
from pymatgen.ext.matproj import MPRester

def Pseudos(structure) -> structure:
    """
    GBRV Pseudopotentials

    Args: (pymatgen.core.structure.Structure) pymatgen structure

    Return: (dictionary) pseudopotentials
    """
    pseudo = {"Ba": "Ba.pbesol-spn-kjpaw_psl.1.0.0.UPF", "Pb":"Pb.pbesol-dn-kjpaw_psl.0.2.2.UPF",
              "O": "O.pbesol-n-kjpaw_psl.0.1.UPF", "Ag": "Ag_ONCV_PBEsol-1.0.upf",
              "Fe": "Fe.pbesol-spn-kjpaw_psl.0.2.1.UPF", "Na": "Na_ONCV_PBEsol-1.0.upf",
              "Si": "Si.pbesol-n-rrkjus_psl.1.0.0.UPF", "Al": "Al.pbesol-n-kjpaw_psl.1.0.0.UPF",
              "F": "F.oncvpsp.upf", "Nb": "Nb.pbesol-spn-kjpaw_psl.0.3.0.UPF",
              "Sn": "sn_pbesol_v1.4.uspp.F.UPF", "As" : "As.pbesol-n-rrkjus_psl.0.2.UPF",
              "Ga": "Ga.pbesol-dn-kjpaw_psl.1.0.0.UPF", "Ni":"ni_pbesol_v1.4.uspp.F.UPF",
              "S": "s_pbesol_v1.4.uspp.F.UPF", "Au" : "Au_ONCV_PBEsol-1.0.upf",
              "Ge": "ge_pbesol_v1.4.uspp.F.UPF", "N": "N.oncvpsp.upf",
              "Sr": "sr_pbesol_v1.uspp.F.UPF", 
              "Ta" : "ta_pbesol_v1.uspp.F.UPF", "Be" : "Be_ONCV_PBEsol-1.0.upf",
              "Hf" : "Hf-sp.oncvpsp.upf", "Os": "os_pbesol_v1.2.uspp.F.UPF",
              "Tc": "Tc_ONCV_PBEsol-1.0.upf" , "Bi": "bi_pbesol_v1.uspp.F.UPF",
              "Hg" : "Hg_ONCV_PBEsol-1.0.upf", 
              "Te" : "te_pbesol_v1.uspp.F.UPF", "B": "b_pbesol_v1.4.uspp.F.UPF",
              "H" : "H_ONCV_PBEsol-1.0.upf", "Pd": "Pd_ONCV_PBEsol-1.0.upf",
              "Ti" : "ti_pbesol_v1.4.uspp.F.UPF", "Br" : "br_pbesol_v1.4.uspp.F.UPF",
              "In" : "In.pbesol-dn-rrkjus_psl.0.2.2.UPF", "P" : "P.pbesol-n-rrkjus_psl.1.0.0.UPF",
              "Tl" : "tl_pbesol_v1.2.uspp.F.UPF", "Ca" : "ca_pbesol_v1.uspp.F.UPF",
              "I" : "I.pbesol-n-kjpaw_psl.0.2.UPF", "Pt" : "Pt.pbesol-spfn-rrkjus_psl.1.0.0.UPF",
              "V" : "v_pbesol_v1.4.uspp.F.UPF", "Cd" : "Cd.pbesol-dn-rrkjus_psl.0.3.1.UPF",
              "Ir" : "ir_pbesol_v1.2.uspp.F.UPF", "Rb": "Rb_ONCV_PBEsol-1.0.upf",
              "W": "w_pbesol_v1.2.uspp.F.UPF", "Cl" : "Cl.pbesol-n-rrkjus_psl.1.0.0.UPF",
              "K" : "K.pbesol-spn-kjpaw_psl.1.0.0.UPF", "Re" : "re_pbesol_v1.2.uspp.F.UPF",
              "Y" : "y_pbesol_v1.4.uspp.F.UPF", "Co" : "co_pbesol_v1.2.uspp.F.UPF",
              "La" : "La.GGA-PBESOL-paw.UPF", "Rh" : "Rh_ONCV_PBEsol-1.0.upf",
              "Zn" : "zn_pbesol_v1.uspp.F.UPF", "C" : "C.pbesol-n-kjpaw_psl.1.0.0.UPF",
              "Li" : "li_pbesol_v1.4.uspp.F.UPF", "Ru" : "Ru_ONCV_PBEsol-1.0.upf",
              "Zr" : "zr_pbesol_v1.uspp.F.UPF", "Cr" : "cr_pbesol_v1.5.uspp.F.UPF",
              "Mg" : "mg_pbesol_v1.4.uspp.F.UPF", "Sb" : "sb_pbesol_v1.4.uspp.F.UPF",
              "Cs" : "cs_pbesol_v1.uspp.F.UPF", "Mn" : "mn_pbesol_v1.5.uspp.F.UPF",
              "Sc" : "Sc.pbesol-spn-kjpaw_psl.0.2.3.UPF", "Cu" : "Cu_ONCV_PBEsol-1.0.upf",
              "Mo" : "Mo_ONCV_PBEsol-1.0.upf", "Se" : "se_pbesol_v1.uspp.F.UPF"}

    pseudo_atm = list(structure.symbol_set)

    pseudo_name = [pseudo[k] for k in pseudo_atm]

    pseudo_dict = dict(zip(pseudo_atm,pseudo_name))

    return pseudo_dict
