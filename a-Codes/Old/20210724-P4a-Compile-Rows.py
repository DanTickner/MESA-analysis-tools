import os
import csv

#----- Define variables -----
parent_dirs = [ "20210721_ztest/numfractions" ] # [ "Omega=5d-5/z=1d-4", "Omega=5d-5/z=5d-3", "Omega=5d-5/z=1d-3" ] # Each of these folders is expected to contain all members of csv_folders as subdirectories.
csv_folders = [ "LOGS_ztest_"+i for i in [ "1AG89","2GN93","3GS98","4L03","5AGS05","6AGSS09","7L09","8A09Prz" ] ]# [ "0p" + str(i) for i in range(60,96) ] # [ "0p6", "0p65", "0p7", "0p75", "0p8", "0p85", "0p9" ]
output_filename =  parent_dirs[0]+"/20210721_ztest_model1.csv" # "Ryan+1996/Data_MESA_model_number_z=1d-4.csv" # Include parent directories (if desired) and .csv extension. Make sure any parent directories exist!

headers = []
first_filepath = "" # To keep track of reference file when comparing headers.
desired_rows = [] # To store the data.
stars_ignored = 0 # Counter for stars which don't reach the desired age.

#----- Preferences -----

# Option to read all folders in "loc", saves specifying model_letters. Will fail if any parent_dir contains anything that is not a folder with CSV/history.csv.
use_all_folders = True

condition = "model_number" # "final", "MSTO", "age", "model_number"
age = 13e9 # in years; only used if condition == "age".
model_number = 1 # Only used if condition == "model_number".


#----- Open all folders from each parent directory and read the final line ------
print( "Reading csv:" )
for parent in parent_dirs:

	if use_all_folders:
		csv_folders = os.listdir( parent )
		print( csv_folders )
		for obj in csv_folders:
			if not os.path.isdir(os.path.join( parent, obj )):
				print( f"{obj} removed." )
				csv_folders.remove( obj )

	for subfolder in csv_folders:
		filepath = parent + "/" + subfolder + "/CSV"
		print( filepath )
		with open( filepath + "/history.csv", "r" ) as in_file:
			data = list(csv.reader( in_file ))

			# Create list of headers if this is the first passthrough. Stop the code if the headers aren't consistent.
			if headers == []:
				headers = data[0]
				Teff_col = headers.index( "log_Teff" )
				age_col = headers.index( "star_age" )
				model_number_col = headers.index( "model_number" )
			if data[0] != headers:
				raise ValueError( "Headers of %s don't match %s.\n%s\n%s" %( filepath, first_filepath, data[0], headers ) )

			# Extract desired row of csv.
			if   condition == "final":
				n = -1

			elif condition == "MSTO":
				log_Teff = [ float(row[Teff_col]) for row in data[1:] ]
				n = log_Teff.index(max( log_Teff )) + 1 # Offset by 1 due to headers.

			elif condition == "age":	# Not yet tested.
				star_age = [ float(row[age_col]) for row in data[1:] ]
				# Skip this model if it doesn't evolve long enough.
				if star_age[-1] < age:
					print( "Max age too low; ignoring model.\tage:%s\tneed:%s." %( star_age[-1], age ) )
					stars_ignored += 1
					continue
				n = 1 # Offset by 1 due to headers.
				while star_age[n-1] < age:
					n += 1

			elif condition == "model_number":
				star_model_number = [ float(row[model_number_col]) for row in data[1:] ]
				if star_model_number[-1] < model_number:
					print( "Model number too low; ignoring model.\tnumber:%s\tneed:%s." %( star_model_number[-1], model_number ) )
					stars_ignored += 1
				n = 1 # Offset by 1 due to headers.
				while star_model_number[n-1] < model_number:
					n += 1

			desired_rows.append( [ parent, subfolder ] + data[n] )


#----- Save the final rows to a csv for further analysis -----
print( "Stars ignored due to not meeting conditions: %s." %stars_ignored )

with open( output_filename, "w", newline="" ) as out_file:
	ow = csv.writer( out_file )
	ow.writerow( [ "Parent_folder", "Subfolder" ] + headers )

	for row in desired_rows:
		ow.writerow( row )

print( "\nSaved csv: " + output_filename )
