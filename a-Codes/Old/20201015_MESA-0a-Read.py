import time
import os
import shutil
import csv

#----- Define variables -----
model_name = "1M_pre_ms_to_wd"


#----- Preferences -----
append_to_model_name = "_2agb"
add_to_start_of_model_name = "TestSuite_"


#----- Don't change (constants, or to be populated by the code) -----
start_time = time.clock()
logs_folder = "../a-MESA/" + model_name + "/LOGS"
output_folder = "Models/" + add_to_start_of_model_name + model_name + append_to_model_name
output_folder_inlists = output_folder + "/inlists etc"
output_folder_csv = output_folder + "/CSV"
inlist_etc_filenames = [ "profile_columns.list", "history_columns.list", "rn" ]
values = []
values_profile = []

# Profiles.index
all_model_numbers = []
all_star_ages = []
profiles = []
priorities = []
model_number = []
star_ages = []


#----- Make sure specified paths exist; create them if not -----
for folder in [ output_folder, output_folder_inlists, output_folder_csv ]:
	if not os.path.exists( folder ):
		os.mkdir( folder )


#----- If inlist and columns files provided, copy to CSV folder -----
print( "Files copied to CSV folder:" )

for filename in os.listdir( logs_folder ):
	if filename in ( inlist_etc_filenames ) or ( "inlist" in filename ):
		shutil.copy( logs_folder + "/" + filename, output_folder_inlists )
		print( filename )


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

#----- Save values to csv for easy future analysis -----
with open( output_folder_csv + "/history.csv", "w", newline="" ) as csv_file:
	writer = csv.writer( csv_file )
	writer.writerow( col_names )# Headers row
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
				j = col_names_profile.index( c ) # i.e. don't take it for granted that the order of columns is the same for every profile.
				values_profile[j+1].append( float( row[j] ) )


#----- Save values to csv -----
with open( output_folder_csv + "/profiles-data.csv", "w", newline="" ) as csv_file:
	writer = csv.writer( csv_file )
	writer.writerow( [ "profile_number" ] + col_names_profile )# Headers row
	n = len( values_profile )# Number of columns to write, including the profile_number index
	
	for i in range( len( values_profile[0] ) ):
		row = [ values_profile[j][i] for j in range(n) ]
		writer.writerow( row )


#----- Code is finished -----
print( "CSV files saved:")
for filename in [ "history", "profiles", "profiles_data" ]:
	print( output_folder + "/" + filename + ".csv" )

end_time = time.clock()
dt = end_time - start_time
print( "\nTime: " + str(int( dt/3600 )) + " hr " + str(int( dt/60 )) + " min " + str(int( dt%60 )) + " sec." )
