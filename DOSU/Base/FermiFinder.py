import os
import re
def FindMinMax():
	os.chdir('../')
#	os.chdir(chem_form + '_' + MP_ID)
	os.chdir('scfu_dos/')
	os.system('grep "Fermi" dftu.out > temp.txt')
	with open('temp.txt') as file:
		onlyline = file.readlines()
		energy=round(float(re.findall(r'\d+.....', str(onlyline))[0]),0)
		emin=energy-20
		emax=energy+20
	os.system('rm temp.txt')
	return emin,emax
		

