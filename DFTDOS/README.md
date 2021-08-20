
# DOSpkg

1. Performs Density of States calculations using standard DFT through Quantum Espresso
2. Generates Density of States plots from calculations

Adapted from DFTU package by Vincent Xiong
https://github.com/yyx5048/DFTU

Inspired by Density of States Calculation Code by Levi Lentz
https://blog.levilentz.com/density-of-states-calculation/


## Installation and Usage
Create and activate a conda environment containing the Pymatgen library

Move the DOSpkg folder into your working directory (any directory is okay, it does not have to be in the DFTU folder)

Run scripts in the following order allowing each calculation to finish before continuing to next script:

1. scf_1.py
2. nscf_2.py
3. dos_3.py
4. pdos_4.py
5. makeplot_5.py

Be sure to enter the mp-id in the format mp-#### when prompted in the command line

## Authors
Wayne Zhao, Nicole Kirchner-Hall, Vincent Xiong
