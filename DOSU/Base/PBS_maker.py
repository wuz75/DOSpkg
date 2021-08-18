import subprocess

def create_scf_pbs_file(nodes,file_name):
    """
    Generate PBS file for submission

    Args: (Int) nodes: number of nodes, using default 20 ppn.
    Return:
    """
    with open(file_name,'w') as f:
        f.write("""#PBS -l nodes=1:ppn=20
#PBS -l walltime=10:00:00
#PBS -l pmem=10gb
#PBS -j oe
#PBS -A open

cd $PBS_O_WORKDIR

echo " "
echo "Job started on `hostname` at `date`"
echo " "

PW="/gpfs/group/ixd4/default/software/qe_nek5091/rhel7_6.7/qe_U_mod/qe-6.7/bin/pw.x"

mpirun -np 20 $PW -ndiag 1 -in dftu.in > dftu.out

echo " "
echo "Job Ended at `date`"
        """.format(nodes,nodes*20))
    return


def create_dos_pbs_file(nodes,file_name):
    """
    Generate PBS file for submission

    Args: (Int) nodes: number of nodes, using default 20 ppn.
    Return:
    """
    with open(file_name,'w') as f:
        f.write("""#PBS -l nodes=1:ppn=20
#PBS -l walltime=10:00:00
#PBS -l pmem=10gb
#PBS -j oe
#PBS -A open

cd $PBS_O_WORKDIR

echo " "
echo "Job started on `hostname` at `date`"
echo " "

PW="/gpfs/group/ixd4/default/software/qe_nek5091/rhel7_6.7/qe_U_mod/qe-6.7/bin/dos.x"

mpirun -np 20 $PW -ndiag 1 -in dftu.in > dftu.out

echo " "
echo "Job Ended at `date`"
        """.format(nodes,nodes*20))

def final_pdos(nodes,file_name):
    with open(file_name,'w') as f:
        f.write("""#PBS -l nodes=1:ppn=20
#PBS -l walltime=10:00:00
#PBS -l pmem=10gb
#PBS -j oe
#PBS -A open

cd $PBS_O_WORKDIR

echo " "
echo "Job started on `hostname` at `date`"
echo " "

PW="/gpfs/group/ixd4/default/software/qe_nek5091/rhel7_6.7/qe_U_mod/qe-6.7/bin/projwfc.x"

mpirun -np 20 $PW -ndiag 1 -in dftu.in > dftu.out

echo " "
echo "Job Ended at `date`"
    """.format(nodes,nodes*20))

def pbs_submit(typ, nodes,file_name):
    """
    Submit PBS file

    Args: (Str) typ: calculation types, "pw" or "hp"
          (Int) nodes: number of nodes, using default 20 ppn.
    Return:
    """
    if typ == "pw":
        create_scf_pbs_file(nodes,file_name)
        subprocess.call(['qsub',file_name])
    elif typ == "dos":
        create_dos_pbs_file(nodes,file_name)
        subprocess.call(['qsub',file_name])
    elif typ == "pdos":
        final_pdos(nodes,file_name)
        subprocess.call(['qsub',file_name])
    else:
        raise ValueError("Invalid calculation type passed")

    return

