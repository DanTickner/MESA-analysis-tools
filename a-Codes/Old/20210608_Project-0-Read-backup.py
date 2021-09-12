import time
import os
import csv

#----- Define variables -----
model_letters = [ "B", "D", "R", "RD" ]


#----- Preferences -----
loc = "../a-MESA"
skip_model_letters = [ False, False, False, False ] # B, D, R, RD
append_filenames_text = [ "", "", "", "stopshort" ]
calculated_col_names = [ "envelope_mass", "[Li]" ]


#----- Function to read the data files and transfer them to csv -----
start_time = time.clock()

def read_file( model_name ):
	
	#--- Definitions ---
	logs_folder = loc + "/0p8M_all/LOGS_" + model_name
	
	i_ml = model_letters.index( ml )
	if append_filenames_text[ i_ml ] != "":
		output_folder = "Models/z_" + append_filenames_text[ i_ml ] + "_" + model_name
	else:
		output_folder = "Models/" + model_name
	
	output_folder_csv = output_folder + "/CSV"
	values = []
	values_profile = []
	
	# Profiles.index
	all_model_numbers = []
	all_star_ages = []
	profiles = []
	priorities = []
	model_number = []
	star_ages = []
	
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
		sm, hecm = [ col_names.index( "star_mass" ), col_names.index( "he_core_mass" ) ]
		envelope_mass = [ values[sm][i] - values[hecm][i] for i in range(len(values[0])) ]
		values.append( envelope_mass )

		# [Li] = 12 + log( N(Li) / N(H) )
		# Perhaps need N(1H) + N(2H) + N(3H). Calculate and see if non-negligible.
		li, h = [ col_names.index( "log_surface_li7" ), col_names.index( "log_surface_h1" ) ]
		li_concentration = [ 12 + values[li][i] - values[h][i] for i in range(len(values[0])) ]# log(A/B) = log(A) - log(B)
		values.append( li_concentration )
	
	#----- Save values to csv for easy future analysis -----
	with open( output_folder_csv + "/history.csv", "w", newline="" ) as csv_file:
		writer = csv.writer( csv_file )
		writer.writerow( col_names + calculated_col_names )# Headers row
		n = len( values )# Number of columns to write

		for i in range( len( values[0] ) ):
			row = [ values[j][i] for j in range(n) ]
			writer.writerow( row )
	
	
	#----- Open "profiles.index" and record which profiles and timesteps were recorded -----
	all_model_numbers = values[ col_names.index( "model_number" ) ]
	all_star_ages = values[ col_names.index( "star_age" ) ]
	
	with open( logs_folder + "/profiles.index" ) as profiles_index_file:
		contents = [ j.strip().split() for j in profiles_index_file.readlines() ]
		
		for row in contents[1:]:
			# Skipped first line because it describes column names.
			if int( row[0] ) in all_model_numbers:
				model_number.append( float( row[0] ) )
				priorities.append( float( row[1] ) )
				profiles.append( float( row[2] ) )
				star_ages.append( all_star_ages[ all_model_numbers.index( int( row[0] ) ) ] )
			else:
				# Model ALWAYS appears in history.data, but this line is here just in case.
				print( "Warning: model %s appears in profiles.index but not history.data" %int(row[0]) )
	
	
	#----- Save profile list to csv -----
	with open( output_folder_csv + "/profiles.csv", "w", newline="" ) as csv_file:
		writer = csv.writer( csv_file )
		writer.writerow( [ "profile_number", "priority", "model_number", "star_age" ] )# Headers row
		
		for i in range( len(model_number) ):
			writer.writerow( [ profiles[i], priorities[i], model_number[i], star_ages[i] ] )
	
	
	#----- Loop through all profile files and save as one csv -----
	for profile_number in profiles:
		with open( logs_folder + "/profile" + str(int(profile_number)) + ".data" ) as history_file:
			contents = [ j.strip().split() for j in history_file.readlines() ]

			#Initial column headers come from first profile. NOTE: these are subject to change (See below)
			if profile_number == min( profiles ):
				col_names_profile = contents[5]
				[ print( txt ) for txt in [ "\nprofileN.data column names:", col_names_profile, "" ] ]
				values_profile.append( [] )# profile_number
				[ values_profile.append( [] ) for par in col_names_profile ]

			#--- Append to contents if required and create empty lists ---
			# Extra columns (e.g. species) can dis/appear in each profile, so this must be checked.
			for c in contents[5]:
				if not c in col_names_profile:
					col_names_profile.append( c )
					# We need to append an extra column that has remained empty up til this point.
					values_profile.append( [ "" for k in range(len(values_profile[0])) ] )


		#--- Append the data ---
		for row in contents[6:]:
			values_profile[0].append( profile_number )
			for c in contents[5]:
				j = col_names_profile.index( c ) # i.e. don't take it for granted that the order of columns is the same for every profile. This noticeably slows the code down, but ensures that nothing ends up in the wrong column.
				values_profile[j+1].append( float( row[j] ) )
	
	
	#----- Save values to csv -----
	with open( output_folder_csv + "/profiles-data.csv", "w", newline="" ) as csv_file:
		writer = csv.writer( csv_file )
		writer.writerow( [ "profile_number" ] + col_names_profile )# Headers row
		n = len( values_profile )# Number of columns to write, including the profile_number index
		
		for i in range( len( values_profile[0] ) ):
			row = [ values_profile[j][i] for j in range(n) ]
			writer.writerow( row )

	print( "Folder:\n" + output_folder_csv )
	print( "\nCSV files saved:")
	for filename in [ "history", "profiles", "profiles_data" ]:
		print( filename + ".csv" )


	#----- Save headers to txt file for easy reference -----
	with open( output_folder_csv + "/headers-history.txt", "w" ) as f_history:
		[ f_history.write( hdr + "\n" ) for hdr in col_names ]
	with open( output_folder_csv + "/headers-profile.txt", "w" ) as f_profile:
		[ f_profile.write( hdr + "\n" ) for hdr in col_names_profile ]
	print( "\nText files saved:" )
	[ print( "headers-" + name + ".txt" ) for name in [ "history", "profile" ] ]


#----- Call the functions -----
for i, ml in enumerate( model_letters ):
	
	if skip_model_letters[i]:
		continue
	
	read_file( ml )

end_time = time.clock()
dt = end_time - start_time
print( "\nTime: " + str(int( dt/3600 )) + " hr " + str(int( dt/60 )) + " min " + str(int( dt%60 )) + " sec." )
