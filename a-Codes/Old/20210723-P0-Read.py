import time
import os
import csv
import numpy as np

#----- Define variables -----
model_letters = [ "LOGS_ztest_9test" ] #[ "LOGS_0p" + str(i) for i in range(60,96) ] #[ "LOGS_" + str(i) for i in [ "B", "D", "R", "RD" ] ]


#----- Preferences -----
loc = "../a-MESA/All_M_Z/20210721_ztest/Stored logs"

# Option to read all folders in "loc", saves specifying model_letters. Will fail if "loc" contains any folders that are not MESA logs. If in doubt, place logs in a nested folder and change loc to that.
use_all_folders = True
if use_all_folders:
	model_letters = os.listdir( loc )
	for obj in model_letters:
		if not os.path.isdir(os.path.join( loc, obj )):
			print( f"{obj} removed from list of MESA log folders." )
			model_letters.remove( obj )
print( model_letters )

skip_model_letters = [ False for i in range(len(model_letters)) ] # [ False, False, False, False, False, False, False ] # B, D, R, RD
append_filenames_text = [ "" for i in range(len(model_letters)) ] # [ "", "", "", "", "", "", "" ]
calculated_col_names = [ "X", "Y", "Z", "[Li]", "[Fe/H]" ] # [ "envelope_mass", "X", "Y", "Z", "[Li]", "[Fe/H]" ]
output_dir = "20210721_ztest/numfractions" # Where to save B,D,R,RD folders. Leave as empty string to save in current directory.


#----- Function to read the data files and transfer them to csv -----
start_time = time.clock()

def read_file( model_name ):
	
	#--- Definitions ---
	logs_folder = loc + "/" + model_name # 0p8M_all
	
	i_ml = model_letters.index( ml )
	if append_filenames_text[ i_ml ] != "":
		if output_dir == "":
			output_folder = "z_Special/z_" + append_filenames_text[ i_ml ] + "_" + model_name
		else:
			output_folder = output_dir + "/z_Special/z_" + append_filenames_text[ i_ml ] + "_" + model_name
	else:
		if output_dir == "":
			output_folder = model_name
		else:
			output_folder = output_dir + "/" + model_name
	
	output_folder_csv = output_folder + "/CSV"
	values = [] # 2D array for history.
	profile_numbers = [] # List of profiles saved.
	
	print( "\nReading file: " + model_name )
	print( "Saving to: " + output_folder )
	
	#----- Make sure specified paths exist; create them if not -----
	for folder in [ output_folder, output_folder_csv ]:
		if not os.path.exists( folder ):
			os.mkdir( folder )
	
	
	#----- Open the "history.data" file and get a list of columns -----
	with open( logs_folder + "/history.data" ) as history_file:
		contents = [ j.strip().split() for j in history_file.readlines() ]
		col_names = contents[5]
		[ print( txt ) for txt in [ "\nhistory.data column names:", col_names, "" ] ]
		
		#--- Append all values ---
		[ values.append( [] ) for col in col_names ]
		
		for row in contents[6:]:
			for i in range( len(col_names) ):
				values[i].append( float( row[i] ) )

		#--- Calculated columns ---
		# envelope_mass = star_mass - he_core_mass
		#sm, hecm = [ col_names.index( "star_mass" ), col_names.index( "he_core_mass" ) ]
		#envelope_mass = [ values[sm][i] - values[hecm][i] for i in range(len(values[0])) ]
		#values.append( envelope_mass )

		# surface abundances
		h = col_names.index( "log_surface_h1" )	#
		he4, he3 = col_names.index( "log_surface_he4" ), col_names.index( "log_surface_he3" )
		li = col_names.index( "log_surface_li7" ) # li6 also exists but negligible, and besides net "agb" doesn't contain it.
		
		# X, Y, Z
		X = [ 10**( values[h][i] ) for i in range(len(values[0])) ]
		Y = [ 10**( values[he4][i] ) + 10**( values[he3][i] ) for i in range(len(values[0])) ]
		Z = [ 1 - X[i] - Y[i] for i in range(len(values[0])) ]
		values += [ X, Y, Z ]

		# [x] = 12 + log( N(x) / N(H) ) for a given elemnt x. Also log(A/B) = log(A) - log(B).
		values.append( [ 12 + values[li][i] - values[h][i] for i in range(len(values[0])) ] )

		# [Fe/H] = log(Z/X)_star - log(Z/X)_solar = log(Z/X)_star + 1.61
		values.append( [ np.log10( Z[i] / X[i] ) + 1.61 for i in range(len(values[0])) ] )
	
	#----- Save values to csv for easy future analysis -----
	with open( output_folder_csv + "/history.csv", "w", newline="" ) as csv_file:
		writer = csv.writer( csv_file )
		writer.writerow( col_names + calculated_col_names )# Headers row
		n = len( values )# Number of columns to write

		for i in range( len( values[0] ) ):
			row = [ values[j][i] for j in range(n) ]
			writer.writerow( row )
	
	#----- Get list of profiles created -----
	with open( logs_folder + "/profiles.index" ) as pi_file:
		pi_data = [ j.strip().split() for j in pi_file.readlines() ]
		for row in pi_data[1:]:
			profile_numbers.append( row[-1] )
	
	#----- Append all profiles to single csv file. -----
	with open( output_folder_csv + "/profiles.csv", "w", newline="" ) as profiles_file:
		profiles_writer = csv.writer( profiles_file )
		
		for p in profile_numbers:
			with open( logs_folder + "/profile" + p + ".data" ) as p_file:
				p_data = [ j.strip().split() for j in p_file.readlines() ]
				
				if p == min( profile_numbers ):
					profile_headers = p_data[5] # Headers.
					profiles_writer.writerow( [ "profile_number", "model_number" ] + profile_headers )
				elif p_data[5] != profile_headers:
					raise ValueError( "Headers inconsistent for profile %s:\n%s\n%s" %( p, profile_headers, p_data[5] ) )
				
				m = p_data[2][0]
				for row in p_data[6:]:
					profiles_writer.writerow( [ p, m ] + row )
	
	#----- Notify user of files saved and loations. -----
	print( "Folder:\t" + output_folder_csv )
	print( "history.csv\tprofiles.csv" )


#----- Call the functions -----
print( "Code executed at " + time.ctime() )

for i, ml in enumerate( model_letters ):
	
	if skip_model_letters[i]:
		continue
	
	read_file( ml )

end_time = time.clock()
dt = end_time - start_time
print( "\nTime: " + str(int( dt/3600 )) + " hr " + str(int( dt/60 )) + " min " + str(int( dt%60 )) + " sec." )
