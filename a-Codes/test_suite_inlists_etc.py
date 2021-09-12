# Copy the "test_suite" folder and remove all system files, to create a new set of folders that's small and composed only of text files, so easily searchable.

import os
import shutil

input_dir = "../Desktop"
input_folder = "test_suite"
output_folder = "test_suite_inlists_etc"

new_folder = os.path.join( input_dir, output_folder )

shutil.copytree( os.path.join(input_dir,input_folder), os.path.join(input_dir,output_folder) )

def delete_file( item, folder ):
	if not( "inlist" in item or "columns" in item or "mesh" in item or "net" in item ):
		os.remove( os.path.join( folder, item ) )

for item in os.listdir( new_folder ):

	# Delete files from test_suite main folder.
	if not os.path.isdir( os.path.join(new_folder,item) ):
		delete_file( item, new_folder )

	# Go to each individual star subfolder (e.g. 1.3M_ms_high_Z ).
	else:
		subfolder = os.path.join( new_folder, item )
		for item2 in os.listdir( subfolder ):

			# Delete files from the individual star subfolder.
			if not os.path.isdir( os.path.join(subfolder,item2) ):
				delete_file( item2, subfolder )

			# Go to each star's subsubfolder (e.g. make ).
			else:
				subsubfolder = os.path.join( subfolder, item2 )
				for item3 in os.listdir( subsubfolder ):

					# Delete files from the subsubfolder.
					if not os.path.isdir( os.path.join(subsubfolder,item3) ):
						delete_file( item3, subsubfolder )

					# Code not designed to go beyond two nesting levels, so stop here.
					else:
						print( f"Ignoring nested folder {os.path.join(subsubfolder,item3)}." )
