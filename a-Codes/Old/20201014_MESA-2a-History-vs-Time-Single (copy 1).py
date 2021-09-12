import csv
import matplotlib.pyplot as plt


#----- Define variables -----
#model_name = "SC_me"
model_name = "z_new_rotation_flag=true_butrelax_R"
folder_output = "Models/" + model_name
#column_names = [ "surf_avg_omega_div_omega_crit", "surf_avg_v_rot", "star_mass" ]
column_names = [ "star_mass", "he_core_mass", "envelope_mass", "surf_avg_omega_div_omega_crit", "surf_avg_v_rot" ]
#column_names = [ "Log_L", "pp", "cno" ]

#title = r"Salaris Ex-student code" if model_name == "SC_change" else r"My code"

#----- Preferences -----
graph_type = "semilogx" # "normal", "semilogx", "semilogy", "loglog"
use_custom_ylabels = False
set_title = True
use_custom_xlim = False
use_custom_ylim = False
keep_figures_open = True
append_to_filename = False

ylabels = [ "conv mx2 bot", "", "" ]
title = r"Basic star"
custom_xlims = [ [ 3.7, 3.68 ], [], [] ]
custom_ylims = [ [ -0.75, -0.5 ], [], [] ]
append_to_filename_text = "One-At-Time"


#----- Don't change (constants, or to be populated by the code) -----
folder_csv = "Models/" + model_name + "/CSV"
output_filenames = []
cols = []
star_age = []
history_data = []

for name in column_names:
	output_filename = "History-" + name
	if append_to_filename:
		output_filename += append_to_filename_text
	output_filenames.append( output_filename )
	history_data.append( [] )


#----- Read history.csv and extract values -----
with open( folder_csv + "/history.csv" ) as data_file:
	data = csv.reader( data_file )
	headers = next( data )
	
	#--- Check age and column are included -----
	for par in [ "star_age" ] + column_names:
		if not par in headers:
			raise ValueError( "%s not in history.csv." %par )
		else:
			cols.append( headers.index( par ) )
	
	#--- Populate lists ---
	for row in data:
		star_age.append( float( row[ cols[0] ] ) )
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
	ax.set_xlabel( "Star age (yr)" )
	ax.set_ylabel( ylabels[i] if use_custom_ylabels else column_names[i].replace("_"," ") )

	if set_title:
		ax.set_title( title )
	if use_custom_xlim:
		ax.set_xlim( custom_xlims[i][0], custom_xlims[i][1] )
	if use_custom_ylim:
		ax.set_ylim( custom_ylims[i][0], custom_ylims[i][1] )

	if graph_type == "normal":
		ax.plot( star_age, history_data[i], color="b", ls="-" )
	elif graph_type == "semilogx":
		ax.semilogx( star_age, history_data[i], color="b", ls="-" )
	elif graph_type == "semilogy":
		ax.semilogy( star_age, history_data[i], color="b", ls="-" )
	elif graph_type == "loglog":
		ax.loglog( star_age, history_data[i], color="b", ls="-" )
	else:
		raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )

	fig.tight_layout()
	plt.savefig( folder_output + "/" + output_filenames[i] )

	print( column_names[i] )

	if not keep_figures_open:
		plt.close()
