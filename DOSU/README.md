
# DOSpkg

1. Performs Density of States calculations using DFT+U through Quantum Espresso
2. Generates Density of States plots from calculations

Adapted from and used in conjunction with DFTU package by Vincent Xiong
https://github.com/yyx5048/DFTU

Inspired by Density of States Calculation Code by Levi Lentz
https://blog.levilentz.com/density-of-states-calculation/

## Installation and Usage
Create and activate a conda environment containing the Pymatgen library

Move the DOSpkg folder into your DFTU folder

Change to DOSpkg directory within DFTU folder and run scripts within DOSpkg folder

Run scripts in the following order allowing each calculation to finish before continuing to next script:

1. scfu_1.py
2. nscfu_2.py
3. dosu_3.py
4. pdosu_4.py
5. makeplotu_5.py

Be sure to enter the mp-id in the format mp-#### when prompted in the command line

## Authors
Wayne Zhao, Nicole Kirchner-Hall, Vincent Xiong
