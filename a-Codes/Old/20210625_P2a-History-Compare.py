import csv
import matplotlib.pyplot as plt


#----- Define variables -----
model_letters = ["B", "D", "R", "RD" ]#[ "RD", "RD_old" ]
folder_output = "a_Comparisons" #"a_Comparisons_20210623"

# Plots one graph per quantity in list. Saves running the code len(column_names) times! But use separate lists for "normal", "semilogx", etc.
#column_names = [ "surf_avg_v_rot", "surf_avg_omega_div_omega_crit", "star_mass", "pp", "cno", "tri_alfa", "he_core_mass", "envelope_mass" ]
column_names = [ "star_mass", "log_center_Rho", "log_center_T", "envelope_mass", "X", "Y", "Z", "surf_avg_omega_div_omega_crit", "rel_cumulative_energy_error", "rotation_solver_steps", "diffusion_solver_steps", "surf_avg_v_rot", "surf_avg_omega", "surf_avg_omega_crit" ]


#----- Preferences -----
graph_type         = "normal" # "normal", "semilogx", "semilogy", "loglog"
use_custom_ylabel  = False
set_title          = True
use_custom_labels  = True
use_custom_xlim    = False
use_custom_ylim    = False
append_to_filename = True
show_legend        = False #For multiple graphs, there's little use showing the same legend in all of them. Write it in a figure caption instead or something.

ylabel                  = ""
title                   = r"$M/M_\odot=0.8$, $Z=0.001$"
custom_labels           = [ "Standard", "Diffusion", "Rotation", "Rotation and diffusion" ]
line_colours            = [ "k", "b", "orange", "red", "green", "grey" ]
line_styles             = [ "-", "--", ":", "-.", "-", "-" ]
#custom_xlim             = [ 1e7, 3e10 ]# good range for semilogx
custom_xlim             = [ 1e10, 1.5e10 ]
custom_ylim             = [ -5, 1 ]
append_to_filename_text = ""

# This unnecessarily builds up from CSVs for each column_name. Rewrite without defining a function; made history_data a 3D list.
def plot_history_vs_time( column_name ):

	#----- Definitions -----
	folders_csv     = [ m + "/CSV" for m in model_letters ]
	output_filename = "Compare-" + column_name
	cols            = [ [] for m in model_letters ]
	star_age        = [ [] for m in model_letters ]
	model_number    = [ [] for m in model_letters ]
	history_data    = [ [] for m in model_letters ]
	
	if append_to_filename:
		output_filename += append_to_filename_text
	
	
	#----- Read history.csv and extract data -----
	for i in range(len( model_letters )):
		with open( folders_csv[i] + "/history.csv" ) as data_file:
			data = csv.reader( data_file )
			headers = next( data )
			
			#--- Check age and column are included -----
			for par in [ "star_age", "model_number", column_name ]:
				if not par in headers:
					raise ValueError( "%s not in history.csv." %par )
				else:
					cols[i].append( headers.index( par ) )
			
			#--- Populate lists ---
			for row in data:
				star_age[i].append(     float( row[ cols[i][0] ] ) )
				model_number[i].append( float( row[ cols[i][1] ] ) )
				history_data[i].append( float( row[ cols[i][2] ] ) )
			
	#----- Plot graph -----
	plt.rc( "text", usetex=True )
	plt.rcParams.update({ "font.size":14 })
	
	for x_axis, x_label, filename in zip( [star_age,model_number], ["Star age (yr)","Model number"], ["star-age", "model-number" ] ):
		fig = plt.figure( figsize=(8,5) )
		ax = fig.add_subplot( 111 )
		ax.set_xlabel( x_label )
		ax.set_ylabel( ylabel if use_custom_ylabel else column_name.replace("_","\_") )
		labels = custom_labels if use_custom_labels else model_letters
		
		if set_title:
			ax.set_title( title )
		if use_custom_xlim:
			ax.set_xlim( custom_xlim[0], custom_xlim[1] )
		if use_custom_ylim:
			ax.set_ylim( custom_ylim[0], custom_ylim[1] )
		
		for i in range(len( model_letters )):
			if graph_type == "normal":
				ax.plot( x_axis[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
			elif graph_type == "semilogx":
				ax.semilogx( x_axis[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
			elif graph_type == "semilogy":
				ax.semilogy( x_axis[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
			elif graph_type == "loglog":
				ax.loglog( x_axis[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
			else:
				raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )
		
		#--- Put legend outside the plot and save figure ---
		if show_legend:
			box = ax.get_position()
			ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
			ax.legend( bbox_to_anchor=(1.0,1.0) )
		plt.savefig( folder_output + "/" + output_filename + "-vs-" + filename, bbox_inches="tight" )
		plt.close()



#----- Call the functions -----
print( "Output folder: " + folder_output )
print( "Plotting comparison graphs for the following history.data columns:\n" )

for column_name in column_names:

	plot_history_vs_time( column_name )

	print( column_name )
