import csv
import matplotlib.pyplot as plt


#----- Define variables -----
model_name = "R_2agb_moreprofiles"
folder_output = "Models/" + model_name
#column_name = "surf_avg_omega_div_omega_crit"
#column_name = "star_mass"
column_name = "pp"
x_column_name = "model_number"


#----- Preferences -----
graph_type = "normal" # "normal", "semilogx", "semilogy", "loglog"
use_custom_ylabel = False
use_custom_xlabel = False
set_title = True
use_custom_xlim = False
use_custom_ylim = False
keep_figure_open = True
append_to_filename = False

ylabel = "conv mx2 bot"
xlabel = "model number"
title = r"Test Suite: conserve\_angular\_momentum"
custom_xlim = [ 3.7, 3.68 ]
custom_ylim = [ -0.75, -0.5 ]
append_to_filename_text = "One-At-Time"


#----- Don't change (constants, or to be populated by the code) -----
folder_csv = "Models/" + model_name + "/CSV"
output_filename = "History-" + column_name + "-vs-" + x_column_name
cols = []
x_data = []
history_data = []

if append_to_filename:
	output_filename += "-" + append_to_filename_text


#----- Read history.csv and extract values -----
with open( folder_csv + "/history.csv" ) as data_file:
	data = csv.reader( data_file )
	headers = next( data )
	
	#--- Check age and column are included -----
	for par in [ x_column_name, column_name ]:
		if not par in headers:
			raise ValueError( "%s not in history.csv." %par )
		else:
			cols.append( headers.index( par ) )
	
	#--- Populate lists ---
	for row in data:
		x_data.append( float( row[ cols[0] ] ) )
		history_data.append( float( row[ cols[1] ] ) )

#----- Plot graph -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig = plt.figure( figsize=(8,5) )
ax = fig.add_subplot( 111 )
ax.set_xlabel( xlabel if use_custom_xlabel else x_column_name.replace("_"," ") )
ax.set_ylabel( ylabel if use_custom_ylabel else column_name.replace("_"," ") )

if set_title:
	ax.set_title( title )
if use_custom_xlim:
	ax.set_xlim( custom_xlim[0], custom_xlim[1] )
if use_custom_ylim:
	ax.set_ylim( custom_ylim[0], custom_ylim[1] )

if graph_type == "normal":
	ax.plot( x_data, history_data, color="b", ls="-" )
elif graph_type == "semilogx":
	ax.semilogx( x_data, history_data, color="b", ls="-" )
elif graph_type == "semilogy":
	ax.semilogy( x_data, history_data, color="b", ls="-" )
elif graph_type == "loglog":
	ax.loglog( x_data, history_data, color="b", ls="-" )
else:
	raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )

fig.tight_layout()
plt.savefig( folder_output + "/" + output_filename )

if not keep_figure_open:
	plt.close()
