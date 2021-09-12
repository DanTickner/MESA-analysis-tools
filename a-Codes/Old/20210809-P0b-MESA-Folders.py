# Reason archived: MESA creates folders automatically so don't need to create sets of empty folders before running the code.

# Creates all the LOGS and Photos folders required for a set of MESA models, based on a naming convention you can specify. These folders all have the relevant permissions. Works by copying a template folder that has had permissions manually enabled.

import shutil
import numpy as np
import os


#----- Define variables -----
template_folder  = "Templates_and_data/Folder_with_permissions_template"
dir_out = "Blank_folders_for_MESA/test123"
text_new  = "Z=1d-4_M="
new_masses = [ str(i/1000).replace(".","p") for i in np.linspace( 660, 700, 41 ) ]
print( new_masses )


#----- Create output folder if doesn't already exist -----
if not os.path.exists( dir_out ):
	os.mkdir( dir_out )


#----- Copy files to new directory and rename -----
for m in new_masses:

	filename_new_LOGS = "LOGS_" + text_new + m
	filename_new_Photos = "Photos_" + text_new + m

	[ shutil.copytree( template_folder, os.path.join( dir_out, f ) ) for f in [ filename_new_LOGS, filename_new_Photos ] ]

	print( filename_new_LOGS, filename_new_Photos )
