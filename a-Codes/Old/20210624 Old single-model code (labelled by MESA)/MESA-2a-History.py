import csv
import matplotlib.pyplot as plt


#----- Define variables -----
model_name = "RD"
folder_output = model_name
#column_names = [ "star_mass", "he_core_mass", "envelope_mass", "surf_avg_omega_div_omega_crit", "surf_avg_v_rot" ]
#column_names = [ "pp", "cno", "tri_alfa", "he_core_mass", "total_mass_h1", "total_mass_he4", "total_mass_c12", "c_core_mass", "log_center_T" ]
#column_names = [ "surf_avg_v_rot", "surf_avg_omega_div_omega_crit" ]
#column_names = [ "envelope_mass", "log_center_Rho" ]
column_names = [ "log_surface_neut", "log_surface_h1", "log_surface_h2", "log_surface_he3", "log_surface_he4", "log_surface_li7", "log_surface_be7", "log_surface_b8", "log_surface_c12", "log_surface_c13", "log_surface_n13", "log_surface_n14", "log_surface_n15", "log_surface_o16", "log_surface_o17", "log_surface_o18", "log_surface_f19", "log_surface_ne22", "rel_cumulative_energy_error", "rotation_solver_steps", "diffusion_solver_steps" ]

x_column_name = "model_number"
#x_column_name = "star_age"

#----- Preferences -----
graph_type = "normal" # "normal", "semilogx", "semilogy", "loglog"
use_custom_ylabels = False
set_title = False
use_custom_xlim = False
use_custom_ylim = False
keep_figures_open = False
append_to_filename = False

ylabels = [ "conv mx2 bot", "", "" ]
xlabel = x_column_name.replace( "_", " " )
title = r"$M/M_\odot=0.8$, $Z=0.001$, Rotating model"
#custom_xlims = [ [ 3.7, 3.68 ], [], [] ]
custom_xlims = [ [ 1e7, 3e10 ] ]
custom_ylims = [ [ -0.75, -0.5 ], [], [] ]
append_to_filename_text = ""


#----- Don't change (constants, or to be populated by the code) -----
folder_csv = model_name + "/CSV"
output_filenames = []
cols = []
x_data = []
history_data = []

for name in column_names:
	output_filename = name + "-vs-" + x_column_name
	if append_to_filename:
		output_filename += append_to_filename_text
	output_filenames.append( output_filename )
	history_data.append( [] )


#----- Read history.csv and extract values -----
with open( folder_csv + "/history.csv" ) as data_file:
	data = csv.reader( data_file )
	headers = next( data )
	
	#--- Check age and column are included -----
	for par in [ x_column_name ] + column_names:
		if not par in headers:
			raise ValueError( "%s not in history.csv." %par )
		else:
			cols.append( headers.index( par ) )
	
	#--- Populate lists ---
	for row in data:
		x_data.append( float( row[ cols[0] ] ) )
		for i in range(len(cols)-1):
			history_data[i].append( float( row[ cols[i+1] ] ) )

#----- Plot graph -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

print( "Model name: " + model_name )
print( "\nGraphs plotted vs time:" )

for i in range(len( column_names )):
	fig = plt.figure( figsize=(8,5) )
	ax = fig.add_subplot( 111 )
	ax.set_xlabel( "Star age (yr)" if x_column_name == "star_age" else x_column_name.replace("_"," ") )
	ax.set_ylabel( ylabels[i] if use_custom_ylabels else column_names[i].replace("_","\_") )

	if set_title:
		ax.set_title( title )
	if use_custom_xlim:
		ax.set_xlim( custom_xlims[i][0], custom_xlims[i][1] )
	if use_custom_ylim:
		ax.set_ylim( custom_ylims[i][0], custom_ylims[i][1] )

	if graph_type == "normal":
		ax.plot( x_data, history_data[i], color="b", ls="-" )
	elif graph_type == "semilogx":
		ax.semilogx( x_data, history_data[i], color="b", ls="-" )
	elif graph_type == "semilogy":
		ax.semilogy( x_data, history_data[i], color="b", ls="-" )
	elif graph_type == "loglog":
		ax.loglog( x_data, history_data[i], color="b", ls="-" )
	else:
		raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )

	fig.tight_layout()
	plt.savefig( folder_output + "/" + output_filenames[i] )

	print( column_names[i] )

	if not keep_figures_open:
		plt.close()
