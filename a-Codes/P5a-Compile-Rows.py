import os
import csv
import numpy as np

#----- Define variables -----
parent_dirs = [ "aaa_Data/20210819_1" ] # Each of these folders is expected to contain all members of csv_folders as subdirectories.
csv_folders = [ "Z=1d-4" ]
output_filename =  parent_dirs[0]+"/allmodels_age.csv" # "Ryan+1996/Data_MESA_model_number_z=1d-4.csv" # Include parent directories (if desired) and .csv extension. Make sure any parent directories exist!

headers = []
first_filepath = "" # To keep track of reference file when comparing headers.
desired_rows = [] # To store the data.
stars_ignored = 0 # Counter for stars which don't reach the desired age.

#----- Preferences -----

# Option to read all folders in each parent_dir, saves specifying csv_folders. Ignores files and the "a_Comparisons" folder, but will fail if any parent_dir contains a folder without history.csv.
use_all_folders = True

condition = "age"	# "final", "MSTO", "age", "model_number"
age = 13e9		# Only used if condition == "age"; in years.
ignore_past_MSTO = True	# Only used if condition == "age".
model_number = 1	# Only used if condition == "model_number".


#----- Open all folders from each parent directory and read the final line ------
print( "Reading csv:" )
for parent in parent_dirs:

	if use_all_folders:
		csv_folders = sorted([ obj for obj in os.listdir( parent ) if os.path.isdir(os.path.join( parent, obj )) and obj!="a_Comparisons" ])

	for subfolder in csv_folders:
		filepath = parent + "/" + subfolder
		print( filepath )

		data = list(csv.reader(open( filepath + "/history.csv", "r" )))

		# Create list of headers if this is the first passthrough. Stop the code if the headers aren't consistent.
		if headers == []:
			headers = data[0]
			Teff_col = headers.index( "log_Teff" )
			age_col = headers.index( "star_age" )
			model_number_col = headers.index( "model_number" )
			X_col = headers.index( "X_surf" )
		if data[0] != headers:
			raise ValueError( f"Headers of {filepath} don't match {first_filepath}.\n{data[0]}\n{headers}" )

		# Extract desired row of csv.
		star_log_Teff = [ float(row[Teff_col]) for row in data[1:] ]
		star_age = [ float(row[age_col]) for row in data[1:] ]
		star_model_number = [ float(row[model_number_col]) for row in data[1:] ]
		star_X = [ float(row[X_col]) for row in data[1:] ]

		n_maxTeff = star_log_Teff.index(max( star_log_Teff )) + 1 # Offset by 1 due to headers.
		n_maxX = star_X.index(max( star_X )) + 1 # Offset by 1 due to headers.


		if   condition == "final":
			n = -1

		elif condition == "MSTO":
			n = n_maxTeff
			if max(star_log_Teff) == star_log_Teff[-1]:
				print( f"Ignoring model: Teff never decreases so MSTO likely not reached.\tlogTeff:{star_log_Teff[-1]}." )
				continue

		elif condition == "age":
			# Skip this model if it doesn't evolve long enough.
			if star_age[-1] < age:
				print( f"Ignoring model: Max age too low.\tage:{np.log10(star_age[-1])}\tneed:{np.log10(age)}." )
				stars_ignored += 1
				continue
			n = 1 # Offset by 1 due to headers.
			while star_age[n-1] < age:
				n += 1
			if ignore_past_MSTO:
				if n > min( n_maxTeff, n_maxX ):
					print( f"Ignoring model: Star reaches max age after MSTO.\tage:{np.log10(star_age[n])}\tMSTO:{np.log10(star_age[n_maxTeff])}." )
					stars_ignored += 1
					continue

		elif condition == "model_number":
			if star_model_number[-1] < model_number:
				print( f"Ignoring model: Model number too low.\tnumber:{star_model_number[-1]}%s\tneed:{model_number}." )
				stars_ignored += 1
				continue
			n = 1 # Offset by 1 due to headers.
			while star_model_number[n-1] < model_number:
				n += 1

		desired_rows.append( [ parent, subfolder ] + data[n] )


#----- Save the final rows to a csv for further analysis -----
print( f"Stars ignored due to not meeting conditions: {stars_ignored}." )

writer = csv.writer(open( output_filename, "w", newline="" ))
writer.writerow( [ "Parent_folder", "Subfolder" ] + headers )
[ writer.writerow( row ) for row in desired_rows ]

print( "\nSaved csv: " + output_filename )
