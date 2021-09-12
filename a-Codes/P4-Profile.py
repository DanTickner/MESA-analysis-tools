import csv
import matplotlib.pyplot as plt
import os

#----- Define variables -----
parent_dir = "aaa_Data/20210817" # Where csv_folders saved. Leave as empty string to look in current directory.
csv_folders = [ "LOGS_Z=1d-4_M=0p68" ]

# Plots one graph per quantity in list. Saves running the code len(column_names) times! But use separate lists for "normal", "semilogx", etc.
#column_names = [ "x_mass_fraction_H", "y_mass_fraction_He", "z_mass_fraction_metals", "omega", "omega_crit", "omega_div_omega_crit" ]
column_names = [ "x_mass_fraction_H", "y_mass_fraction_He", "z_mass_fraction_metals" ]

#----- Preferences -----
graph_type	= "normal" # "normal", "semilogx", "semilogy", "loglog"
x_name		= "mass" # "zone", "mass", "logR", "radius_cm"
use_all_folders = True # Read all folders in each parent_dir, saves specifying csv_folders. Ignores files and the "a_Comparisons" folder, but will fail if any parent_dir contains a folder without history.csv.
invert_xaxis    = False # Use this if x_axis is Teff, for example.
use_custom_ylim = False
custom_ylim = [ 1e-10, 1e3 ] # [ lower, upper ]


#----- Definitions and matplotlib setup -----
if use_all_folders:
	csv_folders = sorted([ obj for obj in os.listdir( parent_dir ) if os.path.isdir(os.path.join( parent_dir, obj )) and obj!="a_Comparisons" ])

cols  	 	= [ [] for m in csv_folders ]					# 2D list ( model, data ).
profile_number  = [ [] for m in csv_folders ]					# 2D list ( model, data ); first profile number is always 1.
model_number    = [ [] for m in csv_folders ]					# 2D list ( model, data ).
x_values	= [ [] for m in csv_folders ]			 		# 3D list ( model, profile, data ).
profile_data    = [ [ [] for c in column_names ] for m in csv_folders ]	# 4D list ( model, column, profile, data ).
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })
print( "Profile graphs created:" )


#----- Cycle through models -----
for i in range(len( csv_folders )):

	#---- Read profiles.csv and extract data ----
	with open( os.path.join(parent_dir,csv_folders[i],"profiles.csv") ) as data_file:
		data = csv.reader( data_file )
		headers = next( data )

		#--- Check required columns are included ---
		for par in [ "profile_number", "model_number", x_name ] + column_names:
			if not par in headers:
				raise ValueError( "%s not in profiles.csv." %par )
			else:
				cols[i].append( headers.index( par ) )

		#--- Populate lists, adding a new list for each profile ---
		for row in data:
			# Make new lists if the most recent profile number has changed.
			if profile_number[i] == [] or row[ cols[i][0] ] != profile_number[i][-1]:
				[ lst.append( [] ) for lst in profile_data[i] ]
				profile_number[i].append( row[ cols[i][0] ] )
				model_number[i].append( row[ cols[i][1] ] )
				x_values[i].append( [] )
			x_values[i][-1].append(float( row[ cols[i][2] ] ))
			for j, c in enumerate( cols[i][3:] ):
				profile_data[i][j][-1].append(float( row[c] ))

	#--- Plot a graph for each profile, normalising axes across entire evolution ---
	# x-limits are constant for the star.
	xmin = min([ min(lst) for lst in x_values[i] ]) / 1.05
	xmax = max([ max(lst) for lst in x_values[i] ]) * 1.05

	for j in range(len( column_names )):
		# Create the figure, set y-limits and define the destination folder.
		fig = plt.figure( figsize=(8,5) )
		ax = fig.add_subplot( 111 )
		ax.set_xlabel( x_name.replace("_","\_" ) )
		ax.set_ylabel( column_names[j].replace("_","\_" ) )
		if use_custom_ylim:
			ymin, ymax = custom_ylim
		else:
			ymin = min([ min(lst) for lst in profile_data[i][j] ]) / 1.05
			ymax = max([ max(lst) for lst in profile_data[i][j] ]) * 1.05
		if ymin == ymax:
			if ymin == 0:
				ymax = 1e-3
			else:
				ymin = ymin * 0.9
				ymax = ymax / 0.9
		ax.set_xlim( xmin, xmax )
		ax.set_ylim( ymin, ymax )
		if invert_xaxis:
			plt.gca().invert_xaxis()
		folder_graph = os.path.join( parent_dir, csv_folders[i], f"{column_names[j].replace(' ','_')}-vs-{x_name.replace(' ','_')}" )

		# If folder doesn't exist, create it. If not, redundant files might be leftover after this code (esp if code is ran again and less profiles are created), so delete its contents.
		if not os.path.exists( folder_graph ):
			os.mkdir( folder_graph )
		else:
			list(map( os.unlink, ( os.path.join( folder_graph, f ) for f in os.listdir( folder_graph ) ) ))

		# Plot each profile and save separately, deleting the old profile each time.
		for k in range(len( profile_number[i] )):
			if len( ax.lines ) != 0:
				del ax.lines[0]
			if graph_type == "normal":
				ax.plot( x_values[i][k], profile_data[i][j][k], color="k" )
			elif graph_type =="semilogx":
				ax.semilogx( x_values[i][k], profile_data[i][j][k], color="k" )
			elif graph_type == "semilogy":
				ax.semilogy( x_values[i][k], profile_data[i][j][k], color="k" )
			elif graph_type == "loglog":
				ax.loglog( x_values[i][k], profile_data[i][j][k], color="k" )
			else:
				raise ValueError( f"graph_type {graph_type} no understood." )
			ax.set_title( "Star: %s,\tProfile: %s,\tModel: %s" %( csv_folders[i].replace('_','\_'), profile_number[i][k], model_number[i][k] ) ) # Would prefer to use f-string expression for readability, but it doesn't support backslashes for tabs.
			plt.savefig( folder_graph + "/" + csv_folders[i] + "-" + column_names[j].replace(" ","_" ) + "-" + str(profile_number[i][k]) )
		plt.close()
		print( folder_graph )
