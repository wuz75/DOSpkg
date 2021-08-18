def nscf():
    """
    Quantum Espresso basic settings for nscf Density of States calculations
    """
    pseudo_dir=('/gpfs/group/ixd4/default/Pseudos/SSSP_PBEsol_pseudos/SSSP_PBEsol_precision_pseudos')

    control = {"calculation":"nscf",
               "pseudo_dir" : pseudo_dir,
                 "verbosity" : 'high',
                 "restart_mode" : "from_scratch",
                 "wf_collect" : True,
                 "nstep" : 200,
                 "outdir" : "./tmp",
                 "max_seconds" : 172800}

    system = {"ecutwfc" : 60,
              "ecutrho" : 480,
              "occupations" : "smearing",
              "degauss" : 0.005}

    electrons = {"diagonalization" : "david",
                 "conv_thr" :1.0e-6,
                 "mixing_beta" : 0.50,
                 "electron_maxstep" : 250,
                 "mixing_mode" : "plain"}

    ions = {'!ion_dynamics' : 'bfgs'}

    cell = {'!cell_dynamics' : 'bfgs'}

    input_dict = {"CONTROL" : control,
                  "SYSTEM" : system,
                  "ELECTRONS" : electrons,
                  "IONS" : ions,
                  "CELL" : cell,
                  }

    return input_dict

def scf():
    """
    Quantum Espresso basic settings for scf DFT+U calculations
    """
    pseudo_dir=('/gpfs/group/ixd4/default/Pseudos/SSSP_PBEsol_pseudos/SSSP_PBEsol_precision_pseudos')

    control = {"calculation":"scf",
               "pseudo_dir" : pseudo_dir,
                 "verbosity" : 'high',
                 "restart_mode" : "from_scratch",
                 "wf_collect" : True,
                 "nstep" : 200,
                 "outdir" : "./tmp",
                 "max_seconds" : 172800}

    system = {"ecutwfc" : 60,
              "ecutrho" : 480,
              "occupations" : "smearing",
              "degauss" : 0.005}

    electrons = {"diagonalization" : "david",
                 "conv_thr" :1.0e-6,
                 "mixing_beta" : 0.50,
                 "electron_maxstep" : 250,
                 "mixing_mode" : "plain"}

    ions = {'!ion_dynamics' : 'bfgs'}

    cell = {'!cell_dynamics' : 'bfgs'}

    input_dict = {"CONTROL" : control,
                  "SYSTEM" : system,
                  "ELECTRONS" : electrons,
                  "IONS" : ions,
                  "CELL" : cell,
                  }

    return input_dict

def dos(mpid,emin,emax):
    """
    QE settings for dos calculations
    """

    with open('dftu.in','w') as f:

        f.write("""&DOS
   outdir  = './tmp'
   fildos  = '"""+str(mpid)+""".dos'
   Emin="""+str(emin)+""", Emax="""+str(emax)+""", DeltaE=0.1
/
""")

    return

def pdos(emin,emax):
    """
    QE settings for pdos calculations
    """

    with open('dftu.in','w') as f:

        f.write("""&PROJWFC
   outdir      = './tmp'
   Emin        = """+str(emin)+"""
   Emax        = """+str(emax)+"""
   DeltaE      = 0.1
   ngauss      = 1
   degauss     = 0.02
/
""")
    return

