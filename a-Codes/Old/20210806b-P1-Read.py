# Reason archived: Partial density calculation in profiles.csv is overcomplicated. We don't need to calculate the volume of each zone. Keeping this file as a backup in case I need those lines of code in the future.

import time
import os
import csv
import numpy as np

#----- Define variables -----
input_dir = "../a-MESA/z_Logs" # Where models located. Leave as empty string to look in current directory.
output_dir = "aaa_Data/20210806a_newcolumns" # Where to save folders. Leave as empty string to save in current directory.
models = [ "LOGS_Z=1d-4_M=0p68" ] # [ f for f in os.listdir(input_dir) if f[:6]=="LOGS_Z" ] #[ "LOGS_0p" + str(i) for i in range(60,96) ]


#----- Preferences -----
# Option to read all folders in "loc", saves specifying models. Ignores files, but will fail if "loc" contains any folders that are not MESA logs. If in doubt, place logs in a nested folder and change loc to that.
use_all_folders = False
if use_all_folders:
	models = [ obj for obj in os.listdir( input_dir ) if os.path.isdir(os.path.join( input_dir, obj )) ]

do_profiles = True	# Slow and produces large files, so turn off if you don't need them.

skip_models = [ False for i in range(len(models)) ] # List of boolean values giving option to skip a model. Useful if you are troubleshooting a small list of models which doesn't change.
calculated_col_names_h = [ "A(Li)", "X", "Y", "Z", "[Fe/H]" ] # Must be in same order as calculations carried out in this code below.
calculated_col_names_p = [ "V_zone" ] # Must be in same order as calculations carried out in this code below.


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


	#--- Prepare for calculation of surface number fractions given surface mass fractions ---
	species_h  = [ [], [], [] ] # isotope, element, col_number.
	elements_h = [ [], [], [] ] # element, col_name fraction ( N[H] N[He] etc ), col_name absolute ( N_abs[H], N_abs[He] etc ).
	for n, name in enumerate( col_names ):
		if name[:8] == "surface_" and name[8:] in isotopes:
			isotope = name.replace("surface_","")
			element = "".join([ i for i in isotope if not i.isdigit() ]) # Remove numeric characters, e.g. li7 -> li.
			[ species_h[i].append( val ) for i, val in enumerate([ isotope, element, n ]) ]
			if not element in elements_h[0]:
				[ elements_h[i].append( val ) for i, val in enumerate([ element, f"N[{element.title()}]", f"N_abs{element.title()}]" ]) ]

	history_headers = col_names + elements_h[1] + calculated_col_names_h # Headers for history.csv.
	print( history_headers )


	#--- Append data values, one row at a time ---
	for row in contents[6:]:

		values = [ float(r) for r in row ]
		
		#- Add calculated columns here -
		star_mass = values[history_headers.index("star_mass")] # Needed for multiple calculations.
		# Number fractions.
		N_abs = [] # Total number of atoms of each element, divided by the atomic mass unit and the unknown mass of the "surface layer". Doesn't matter because it cancels when we normalise.
		for el in elements_h[0]:
			sum_isotope_masses = sum([ values[n] for i,n in enumerate(species_h[2]) if species_h[1][i] == el ])
			N_abs.append( sum_isotope_masses / AW_weights[AW_names.index(el)] * star_mass * 1.989e30 / 1.661e-27 ) # This is inaccurate because we are only considering the surface elements. Should replace star_mass by the mass of the "surface" region, but this value is only available in the profiles. Delete this row once profiles are working. 20210806
		values += [ N / sum( N_abs ) for N in N_abs ]
		
		# A(Li) = 12 + log10( N[Li] / N[H] ).
		values.append( 12 + np.log10( values[history_headers.index("N[Li]")] / values[history_headers.index("N[H]")] ) )

		# X, Y, Z. Given by sum_isotopes( mass fraction ) and X+Y+Z=1. Using total mass fractions; surface mass fractions are commented out.
		values.append( ( values[history_headers.index("total_mass_h1" )] + values[history_headers.index("total_mass_h2" )] ) / star_mass )
		values.append( ( values[history_headers.index("total_mass_he3")] + values[history_headers.index("total_mass_he4")] ) / star_mass )
		#values.append( values[history_headers.index("surface_h1" )] + values[history_headers.index("surface_h2" )] )
		#values.append( values[history_headers.index("surface_he3")] + values[history_headers.index("surface_he4")] )
		values.append( 1 - values[-2] - values[-1] )

		# [Fe/H] = log10( Z / X ) + 1.61, where 1.61 = -log10(Z/X)_solar.
		values.append( np.log10( values[-1] / values[-3] ) + 1.61 )
		values += N_abs

		#- This row is finished -
		all_values.append( values )


	#----- Write data to csv -----
	h_writer = csv.writer(open( output_folder + "/history.csv", "w", newline="" ))
	h_writer.writerow( history_headers ) # Headers row
	[ h_writer.writerow( row ) for row in all_values ]

	
	#----- Append all profiles to single csv file -----
	if do_profiles:
		profile_numbers = sorted([ int(f.replace("profile","").replace(".data","")) for f in os.listdir(logs_folder) if f[:7]=="profile" and f[-5:]==".data" ])
		p_writer = csv.writer(open( output_folder + "/profiles.csv", "w", newline="" ))
		
		for p in profile_numbers:
			p_contents = [ j.strip().split() for j in open( logs_folder + f"/profile{p}.data" ).readlines() ]
			
			# Read headers from first profile. Check headers of subsequent profiles for consistency. Stop if inconsistent. Else, continue with the loop (implicit).
			if p == min( profile_numbers ):
				p_headers = p_contents[5] # Read headers from first profile.
				p_writer.writerow( [ "profile_number", "model_number" ] + p_headers + calculated_col_names_p )
				#- Prepare for calculation of partial densities as a function of R, given mass fractions -
				# Only need to assemble this list once because changes in the net between profiles manifest as changes in headers.
				species_p  = [ [], [], [] ] # isotope, element, col_number.
				elements_p = [ [], [] ] # element, col_name ( Rho[H] Rho[He] etc )
				for n, name in enumerate( p_headers ):
					if name in isotopes:
						element = "".join([ i for i in name if not i.isdigit() ]) # Remove numeric characters, e.g. li7 -> li.
						[ species_p[i].append( val ) for i, val in enumerate([ name, element, n ]) ]
						if not element in elements_p[0]:
							[ elements_p[i].append( val ) for i, val in enumerate([ element, f"Rho[{element.title()}]" ]) ]
				print( "\nspecies_p:" )
				print( species_p )
				print( "\nelements_p:" )
				print( elements_p )
			elif p_contents[5] != p_headers:
				raise ValueError( "Headers inconsistent for profile %s:\n%s\n%s" %( p, p_headers, p_contents[5] ) )

			# Write to profiles.csv.
			m = p_contents[2][0] # Corresponding model_number. Useful to keep in profiles.csv.
			for row in p_contents[6:]:
				values = [ float(r) for r in row ]
				R_out = values[ p_headers.index( "radius_cm" ) ] # Outer radius of zone in cm.
				dR    = values[ p_headers.index( "dr" ) ] # Width of zone in cm.
				dM    = values[ p_headers.index( "dm" ) ] # Mass of zone in g.

				#- Add calculated columns here -

				# V_zone = 4pi/3 * ( R_out^3 - (R_out-dR)^3 ), units cm^3
				V_zone = 4*np.pi/3 * ( R_out**3 - ( R_out-dR)**3 )
				values.append( V_zone )

				# Partial density of each element, units g/cm^3
				for el in elements_p[0]:
					sum_isotope_masses = sum([ values[n] for i,n in enumerate(species_p[2]) if species_p[1][i] == el ])
					values.append( sum_isotope_masses * dM  / V_zone )

				#- This row is finished -
				p_writer.writerow( [ p, m ] + values ) # First 2 columns are profile_number and model_number.

	#----- Notify user of files saved and locations -----
	if do_profiles:
		print( f"Folder:\t{output_folder}\nhistory.csv\tprofiles.csv" )
	else:
		print( f"Folder:\t{output_folder}\nhistory.csv" )



#----- Code execution -----
start_time = time.clock()
print( f"Code executed at {time.ctime()}." )

#--- Read atomic weights and list of isotopes ---
AW_contents = list(csv.reader(open( "Templates_and_data/P1-AtomicWeights.csv", "r" )))[1:] # Skip headers on first row.
AW_names    = [ row[0] for row in AW_contents ]
AW_weights  = [ float(row[1]) for row in AW_contents ]
isotopes    = [ j.strip() for j in open( "Templates_and_data/P1-Isotopes.txt" ).readlines() ]

#--- Read each file ---
for i, m in enumerate( models ):
	
	if skip_models[i]:
		continue
	
	read_file( m )

dt = time.clock() - start_time
print( f"\nTime: {int(dt/3600)} hr {int(dt/60)} min {int(dt%60)} sec." )
