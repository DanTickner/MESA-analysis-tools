import os
import csv
import matplotlib.pyplot as plt


#----- Define variables -----
csv_folders = [ "LOGS_01", "LOGS_05", "LOGS_09", "LOGS_13" ]#[ f"LOGS_09_{x}" for x in ["B","R","D"] ] # [ "0p" + str(i) for i in range(60,96) ] # ["B", "D", "R", "RD" ]
parent_dir = "aaa_Data/20210809_B" # Where csv_folders saved. Leave as empty string to look in current directory.
folder_output = "a_Comparisons" # Code will automatically add parent_dir to this. Just name the folder.

# Plots one graph per quantity in list. Saves running the code len(column_names) times! But use separate lists for "normal", "semilogx", etc.
#column_names = [ "surf_avg_v_rot", "surf_avg_omega_div_omega_crit", "star_mass", "pp", "cno", "tri_alfa", "he_core_mass", "envelope_mass" ]
#column_names = [ "star_mass", "log_center_Rho", "log_center_T", "envelope_mass", "X", "Y", "Z", "surf_avg_omega_div_omega_crit", "rel_cumulative_energy_error", "rotation_solver_steps", "diffusion_solver_steps", "surf_avg_v_rot", "surf_avg_omega", "surf_avg_omega_crit" ]
#column_names = [ "surf_avg_v_rot", "surf_avg_omega_div_omega_crit" ]
#column_names = [ "X_surf", "Y_surf", "Z_surf", "A(Li)" ]
column_names = [ "log_center_Rho" ]


#----- Preferences -----
graph_type         = "semilogx" # "normal", "semilogx", "semilogy", "loglog"
use_custom_ylabel  = False
set_title          = False
use_custom_labels  = True
use_tight_xlim     = True # Min and max of input data with no whitespace.
use_custom_xlim    = True
use_custom_ylim    = True
append_to_filename = False
show_legend        = True
use_all_folders    = False # Read all folders in each parent_dir, saves specifying csv_folders. Ignores files and the "a_Comparisons" folder, but will fail if any parent_dir contains a folder without history.csv.
highlight_point    = True	# Highlight a specific point on the plot.
add_axhline        = True

ylabel                  = ""
title                   = r"$M/M_\odot=0.8$, $Z=0.001$"
custom_labels           = [r"$0.60\,M_\odot$", r"$0.64\,M_\odot$", r"$0.68\,M_\odot$", r"$0.72\,M_\odot$", r"$0.76\,M_\odot$" ] # [] # [ "M=0." + str(ml)[-2:] for ml in csv_folders ] # [ "Standard", "Diffusion", "Rotation", "Rotation and diffusion" ]
line_colours            = [ "k", "b", "orange", "red", "green", "grey" ]
line_styles             = [ "-", "--", ":", "-.", "-", "-" ]
#custom_xlim             = [ 1e7, 3e10 ]# good range for semilogx
custom_xlim             = [ 1e2, 3e10 ]
custom_ylim             = [ -3, 3.4 ]
append_to_filename_text = "semilogx"
axhline = 3.3
highlight_modelnumber = [ 291, 302, 313, 333 ]	# Specify which model to highlight.

if parent_dir != "":
	folder_output = os.path.join( parent_dir, folder_output )
if not os.path.exists( folder_output ):
	os.mkdir( folder_output )

#----- Definitions -----
if use_all_folders:
	csv_folders = sorted([ obj for obj in os.listdir( parent_dir ) if os.path.isdir(os.path.join( parent_dir, obj )) and obj!="a_Comparisons" ])
cols            = [ [] for m in csv_folders ] # These will become 2D lists ( model, data ).
star_age        = [ [] for m in csv_folders ]
model_number    = [ [] for m in csv_folders ]
history_data    = [ [ [] for c in column_names ] for m in csv_folders ] # This will become a 3D list ( model, column, data ).


#---- Output -----
print( "Output folder: " + folder_output )
print( "Plotting comparison graphs for the following history.data columns:\n" )


#----- Read history.csv and extract data -----
for i in range(len( csv_folders )):
	with open( os.path.join(parent_dir,csv_folders[i],"history.csv") ) as data_file:
		data = csv.reader( data_file )
		headers = next( data )
		
		#--- Check age and column are included ---
		for par in [ "star_age", "model_number" ] + column_names:
			if not par in headers:
				raise ValueError( "%s not in history.csv." %par )
			else:
				cols[i].append( headers.index( par ) )
		
		#--- Populate lists ---
		for row in data:
			star_age[i].append(     float( row[ cols[i][0] ] ) )
			model_number[i].append( float( row[ cols[i][1] ] ) )
			for j in range(len( column_names )):
				history_data[i][j].append( float( row[ cols[i][j+2] ] ) )
		
#----- Plot graphs -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

for i in range(len( column_names )):
	for x_axis, x_label, filename in zip( [star_age,model_number], ["Star age (yr)","Model number"], ["star-age", "model-number" ] ):
		fig = plt.figure( figsize=(8,5) )
		ax = fig.add_subplot( 111 )
		ax.set_xlabel( x_label )
		ax.set_ylabel( ylabel if use_custom_ylabel else column_names[i].replace("_","\_") )
		labels = custom_labels if use_custom_labels else csv_folders
		output_filename = "Compare-" + column_names[i] + "-vs-" + filename
		if append_to_filename:
			output_filename += "-" + append_to_filename_text
		
		if set_title:
			ax.set_title( title )
		if use_tight_xlim:
			ax.set_xlim( min([min(lst) for lst in star_age]), max([max(lst) for lst in star_age ]) )
		if use_custom_xlim:
			ax.set_xlim( custom_xlim[0], custom_xlim[1] )
		if use_custom_ylim:
			ax.set_ylim( custom_ylim[0], custom_ylim[1] )
		
		for j in range(len( csv_folders )):
			col = 1 - ( j+1 ) / ( len(csv_folders) + 1 )
			if graph_type == "normal":
				ax.plot( x_axis[j], history_data[j][i], color=line_colours[j], ls=line_styles[j], label=labels[j] )
			elif graph_type == "semilogx":
				#ax.semilogx( x_axis[j], history_data[j][i], color=line_colours[j], ls=line_styles[j], label=labels[j] )
				ax.semilogx( x_axis[j], history_data[j][i], color=(col,col,col), ls=line_styles[j], label=labels[j] )
			elif graph_type == "semilogy":
				ax.semilogy( x_axis[j], history_data[j][i], color=line_colours[j], ls=line_styles[j], label=labels[j] )
			elif graph_type == "loglog":
				ax.loglog( x_axis[j], history_data[j][i], color=line_colours[j], ls=line_styles[j], label=labels[j] )
			else:
				raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )
			if highlight_point:
				highlight_k = model_number[j].index( highlight_modelnumber[j] )
				ax.scatter( x_axis[j][highlight_k], history_data[j][i][highlight_k], s=20, color="b", zorder=1 )
			if add_axhline:
				ax.axhline( axhline, color="grey", ls="--", lw=1.5, zorder=-1 )
		
		#--- Put legend outside the plot, save figure and output column name ---
		if show_legend:
			box = ax.get_position()
			ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
			ax.legend( bbox_to_anchor=(1.0,1.0) )
		plt.savefig( folder_output + "/" + output_filename, bbox_inches="tight" )
		plt.close()
		print( column_names[i] + " vs " + filename )
