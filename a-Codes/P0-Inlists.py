# Script to read a template MESA inlist and copy it for a range of initial masses. Can also choose a single value of the metallicity z.

import numpy as np
import os
import copy
#import shutil

#----- Define varibales -----
template_filename_inlist = "Templates_and_data/template_inlist"		# Name of template inlist.
template_filename_rn = "Templates_and_data/template_rn"			# Name of template rn file.
output_folder = "inlists/20210901_RD"	# Where to save inlists.

M_min = 0.6	 #0.66		# Minimum stellar mass (inclusive).
M_max = 0.8 # 0.75 for z=1d-4, 0.83 safe to z=1d-2	# Maximum stellar mass (inclusive).
M_step = 0.01  # 0.001		# Mass increment.

A_Li = 2.7				# Desired lithium abundance
Y = 0.28				# Helium mass fraction
Z = 1e-4				# Metal mass fraction (numerical value for calculations in this code).
Z_text = "1d-4"				# Metal mass fraction (string value to write to inlist).
omega_div_omega_crit = "5d-3"		# Initial angular frequency relative to critical value for mass loss. 

# These values are fixed
m_Li = 6.941				# Atomic mass in u
m_H = 1.00794				# Atomic mass in u
R_H = 2.3e-5				# Primordial abundance ratio 2H / 1H.
R_He = 3e-4				# Primordial abundance ratio 3He / 4He.

M_range = np.arange( M_min, M_max+M_step, M_step )
# M_range = [ 0.68 for i in range( 20 ) ] # Useful for making 20 identical inlists.


#----- Make sure specified path exists; create it if not -----
if not os.path.exists( output_folder ):
	os.mkdir( output_folder )


#----- Calculate required H and He mass fractions -----
M_1H = ( 1 - Y - Z ) / ( 1 + R_H )
M_2H = R_H * M_1H
M_4He = Y / ( 1 + R_He )
M_3He = R_He * M_4He
H_He_fracs = "\n".join([ f"   initial_{isot}{' '*(4-len(isot))}= {format(val,'.10f')}" for isot,val in zip( ["h1","h2","he3","he4"], [M_1H,M_2H,M_3He,M_4He] ) ])


#----- Calculate required z_fractions -----
z0_data = [ j.strip().split() for j in open( "Templates_and_data/template_inlist_zfracs.txt" ).readlines() ]
z0_elements = [ j[0].lower() for j in z0_data[1:] ]
z0_values = [ float(j[1]) for j in z0_data[1:] ]

z_new_Li = ( 1 - Y - Z ) / Z * m_Li / m_H * 10**( A_Li - 12 )
factor = ( 1 - z_new_Li ) / ( 1 - z0_values[ z0_elements.index("li") ] )
z_new = [ j * factor for j in z0_values ]
z_new[0] = z_new_Li # Go back and input correct z(Li).
zfracs = "\n".join([ f"   z_fraction_{el}{' '*(3-len(el))}= {format(val,'.10f')}" for el,val in zip(z0_elements,z_new) ])


#----- Read template and replace metallicity, abundance, rotation placeholders -----
template_inlist = open( template_filename_inlist, "r" ).read().replace( "$METALLICITY$", Z_text ).replace( "$H_HE_FRACS$", H_He_fracs ).replace( "$ZFRACS$", zfracs ).replace( "$OMEGA_DIV_OMEGA_CRIT$", omega_div_omega_crit )


#----- Print feedback to screen -----
print( f"Output folder: {output_folder}\nMetallicity: {Z_text}" )
print( f"Mass range: {M_min} to {M_max} with step {M_step}, {len(M_range)} total." )
print( "\nInlists created:" )

#----- Create an inlist for each mass -----
do_one_list = []		# List of commands for rn file. Build within this loop.

for i, M in enumerate( M_range ):
	
	#--- Create strings, enforcing two decimal places for consistency ---
	M_string = str(round(M,2)) # You will need to change this line if working to more than 2 dp.
	if len(M_string) == 3: # You will need to change this line if working to more than 2 dp.
		M_string += "0"
	M_filename = M_string.replace( ".", "p" ) # Replace dot to avoid issues in filenames.

	#--- filename convention (Change to suit your needs) ---
	#output_filename = "inlist_Z=" + Z_text + "_M=" + M_filename
	if i+1 < 10:
		str_i = "0" + str(i+1)
	else:
		str_i = str(i+1)
	output_filename = str_i
	
	#--- Create a fresh copy and replace masses ---
	this_inlist = copy.copy( template_inlist ).replace( "$MASS$", M_string ).replace( "$MASS_STRING$", M_filename ).replace( "$FILENAME$", output_filename )
	
	#--- Save inlist and print filename to screen ---
	open( output_folder + "/inlist_" + output_filename, "w", newline="" ).write( this_inlist )
	print( output_filename )
	
	#--- Append to rn commands ---
	do_one_list.append( f"do_one z_Inlists/inlist_{output_filename} z_Mods/mod_{output_filename}.mod z_Logs/LOGS_{output_filename}" )



#----- Create rn file and set permission to execute as program -----
template_rn = open( template_filename_rn, "r" ).read()
open( output_folder + "/rn", "w", newline="" ).write( template_rn.replace( "$DO_ONE$", "\n".join(do_one_list) ) )

# Save with execute permissions (failed attempt)
#with open( os.open( output_folder + "/rn", os.O_CREAT | os.O_EXCL, 0o777 ), "w" ) as rn_file:
#	rn_file.write( template_rn.replace( "$DO_ONE$", "\n".join(do_one_list) ) )


#----- Print warning about permissions to screen -----
print( "\nWARNING: file ''rn'' will not have the relevant permissions to run as an executable file, so will cause the error message" )
print( "./rn: Command not found.\nThere are three ways to get around this." )
print( "\n1) GUI method: Right-click on ''rn'', go to ''Permissions'' tab and tick ''Allow this file to run as a program''. This works on Linux but unfortunately I can't find that option on Windows and don't own a Mac." )
print( "2) Terminal method: Type the command\nchmod +x rn\nor\nchmod +755 rn" )
print( "3) Cheat method: Just keep a working ''rn'' file in the directory, then open it and copy-paste the relevant lines." )
print( "\nI don't know how to save a file from Python with the execute permission enabled, so unfortunately that's all we can do for now." )
# https://stackoverflow.com/questions/36745577/how-do-you-create-in-python-a-file-with-permissions-other-users-can-write
# https://docs.python.org/3/library/os.html#os.open (search for "O_RDONLY" to get to list of permissions)
# https://askubuntu.com/questions/229589/how-to-make-a-file-e-g-a-sh-script-executable-so-it-can-be-run-from-a-termi
