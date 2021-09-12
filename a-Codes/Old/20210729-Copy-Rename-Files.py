import shutil
import numpy as np
import os

#----- Define variables -----
dir_in  = "blanks/MESA_Blank_Folders/Template"
dir_out = "blanks/MESA_Blank_Folders/Z=1d-4_refined"
text_new  = "Z=1d-4_M="


#----- Create output folder if doesn't already exist -----
if not os.path.exists( dir_in ):
	os.mkdir( dir_out )

new_nums = [ str(i/1000).replace(".","p") for i in np.linspace( 660, 700, 41 ) ]
print( new_nums )

#----- Copy files to new directory and rename -----
for filename_old in os.listdir( dir_in ):

	# This snippet is specific to the renaming structure desired.

	'''
	if filename_old[:4] == "LOGS":
		filename_new = "LOGS_" + text_new + filename_old[-4:]
	elif filename_old[:6] == "Photos":
		filename_new = "Photos_" + text_new + filename_old[-4:]
	else:
		print( "filename not recognised: " + filename_old )
		continue
	'''

	path_old = os.path.join( dir_in, filename_old )
	path_intermediate = os.path.join( dir_out, filename_old )
	path_new = os.path.join( dir_out, filename_new )

	shutil.copytree( path_old, path_intermediate )
	os.rename( path_intermediate, path_new )

	print( filename_old, filename_new )
