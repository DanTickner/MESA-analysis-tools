# Keep this file to preserve the code for SURFACE metallicities. It might be more useful for comparison to real data.



import time
import os
import csv
import numpy as np

#----- Define variables -----
models = [ "ztest_LOGS_9test" ] #[ "LOGS_0p" + str(i) for i in range(60,96) ] #[ "LOGS_" + str(i) for i in [ "B", "D", "R", "RD" ] ]
input_dir = "../a-MESA/All_M_Z/20210721_ztest/Logs" # Where models located. Leave as empty string to look in current directory.
output_dir = "20210721_ztest/numfractions2" # Where to save folders. Leave as empty string to save in current directory.


#----- Preferences -----
# Option to read all folders in "loc", saves specifying models. Will fail if "loc" contains any folders that are not MESA logs. If in doubt, place logs in a nested folder and change loc to that.
use_all_folders = False
if use_all_folders:
	models = [ obj for obj in os.listdir( input_dir ) if os.path.isdir(os.path.join( input_dir, obj )) ]

skip_models = [ False for i in range(len(models)) ] # List of boolean values giving option to skip a model.
calculated_col_names = [ "A(Li)", "X", "Y", "Z", "[Fe/H]" ] # Must be in same order as calculations carried out in this code below.


#----- Function to read the data files and transfer them to csv -----
def read_file( model_name ):
	
	#--- Define variables and create folder (if necessary) ---
	logs_folder = os.path.join( input_dir, model_name ) # These work even if input_folder == "", output_folder == "".
	output_folder = os.path.join( output_dir, model_name ) 
	print( f"\nReading file: {model_name}\nSaving to: {output_folder}" )

	all_values = [] # List to store all data.
	
	if not os.path.exists( output_folder ):
		os.mkdir( output_folder )	
	
	
	#--- Open "history.data" and read data ---
	contents = [ j.strip().split() for j in open( logs_folder + "/history.data" ).readlines() ] # j.strip().split() removes whitespace.
	col_names = contents[5]
	print( f"\nhistory.data column names:\n{col_names}\n" )


	#--- Prepare for calculation of number fractions given mass fractions ---
	species  = [ [], [], [] ] # isotope, element, col_number
	elements = [ [], [] ] # element, col_name ( N[H] N[He] etc )
	for n, name in enumerate( col_names ):
		if name[:8] == "surface_":
			isotope = name.replace("surface_","")
			element = "".join([ i for i in isotope if not i.isdigit() ]) # Remove numeric characters, e.g. li7 -> li.
			[ species[i].append( val ) for i, val in enumerate([ isotope, element, n ]) ]
			if not element in elements[0]:
				[ elements[i].append( val ) for i, val in enumerate([ element, f"N[{element.title()}]" ]) ]

	history_headers = col_names + elements[1] + calculated_col_names # Headers for history.csv.


	#--- Append data values, one row at a time ---
	for row in contents[6:]:

		values = [ float(r) for r in row ]
		
		#- Add calculated columns here -
		# Number fractions.
		N_abs = [] # Total number of atoms of each element (divided by the atomic mass unit u and star_mass, which both cancel in our calcs).
		for el in elements[0]:
			sum_isotope_masses = sum([ values[n] for i,n in enumerate(species[2]) if species[1][i] == el ])
			N_abs.append( sum_isotope_masses / AW_weights[AW_names.index(el)] )
		values += [ N / sum( N_abs ) for N in N_abs ]
		
		# A(Li) = 12 + log10( N[Li] / N[H] ).
		values.append( 12 + np.log10( values[history_headers.index("N[Li]")] / values[history_headers.index( "N[H]" )] ) )

		# X, Y, Z. Given by sum_isotopes( mass fraction ) and X+Y+Z=1.
		star_mass = values[history_headers.index("star_mass")]
		values.append( ( values[history_headers.index("total_mass_h1" )] + values[history_headers.index("total_mass_h2" )] ) / star_mass )
		values.append( ( values[history_headers.index("total_mass_he3")] + values[history_headers.index("total_mass_he4")] ) / star_mass )
		#values.append( values[history_headers.index("surface_h1" )] + values[history_headers.index("surface_h2" )] )
		#values.append( values[history_headers.index("surface_he3")] + values[history_headers.index("surface_he4")] )
		values.append( 1 - values[-2] - values[-1] )

		# [Fe/H] = log10( Z / X ) + 1.61, where 1.61 = -log10(Z/X)_solar.
		values.append( np.log10( values[-1] / values[-3] ) + 1.61 )

		#- This row is finished -
		all_values.append( values )


	#----- Write data to csv -----
	h_writer = csv.writer(open( output_folder + "/history.csv", "w", newline="" ))
	h_writer.writerow( history_headers ) # Headers row
	[ h_writer.writerow( row ) for row in all_values ]

	
	#----- Append all profiles to single csv file -----
	profile_numbers = sorted([ int(f.replace("profile","").replace(".data","")) for f in os.listdir(logs_folder) if f[:7]=="profile" and f[-5:]==".data" ])
	p_writer = csv.writer(open( output_folder + "/profiles.csv", "w", newline="" ))
	
	for p in profile_numbers:
		p_contents = [ j.strip().split() for j in open( logs_folder + f"/profile{p}.data" ).readlines() ]
		
		# Read headers from first profile. Check headers of subsequent profiles for consistency. Stop if inconsistent.
		if p == min( profile_numbers ):
			p_headers = p_contents[5] # Read headers from first profile.
			p_writer.writerow( [ "profile_number", "model_number" ] + p_headers )
		elif p_contents[5] != p_headers:
			raise ValueError( "Headers inconsistent for profile %s:\n%s\n%s" %( p, p_headers, p_data[5] ) )

		# Write to profiles.csv.
		m = p_contents[2][0] # Corresponding model_number. Useful to keep in profiles.csv.
		[ p_writer.writerow( [ p, m ] + row ) for row in p_contents[6:] ]

	
	#----- Notify user of files saved and locations -----
	print( f"Folder:\t{output_folder}\nhistory.csv\tprofiles.csv" )



#----- Code execution -----
start_time = time.clock()
print( f"Code executed at {time.ctime()}." )

#--- Read atomic weights ---
AW_contents = list(csv.reader(open( "P0-AtomicWeights.csv", "r" )))[1:] # Skip headers on first row.
AW_names    = [ row[0] for row in AW_contents ]
AW_weights  = [ float(row[1]) for row in AW_contents ]

#--- Read each file ---
for i, m in enumerate( models ):
	
	if skip_models[i]:
		continue
	
	read_file( m )

dt = time.clock() - start_time
print( f"\nTime: {int(dt/3600)} hr {int(dt/60)} min {int(dt%60)} sec." )
