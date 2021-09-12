import csv
import matplotlib.pyplot as plt


#----- Define variables -----
model_name = "R"
folder_output = "Models/" + model_name
column_names = [ "surf_avg_v_rot", "surf_avg_omega_div_omega_crit" ]
output_filename = "Rotation-vs-Star-Age"

#x_column_name = "model_number"
x_column_name = "star_age"

#----- Preferences -----
graph_type = "semilogx" # "normal", "semilogx", "semilogy", "loglog"
use_custom_ylabels = False
set_title = True
use_custom_xlim = False
use_custom_ylim = False
keep_figures_open = True
append_to_filename = False

ylabels = [ "", "", "" ]
xlabel = x_column_name.replace( "_", " " )
title = r"$M/M_\odot=0.8$, $Z=0.001$, Rotating model"
#custom_xlims = [ [ 3.7, 3.68 ], [], [] ]
custom_xlims = [ [ 1e7, 3e10 ] ]
custom_ylims = [ [ -0.75, -0.5 ], [], [] ]
append_to_filename_text = ""


#----- Don't change (constants, or to be populated by the code) -----
folder_csv = "Models/" + model_name + "/CSV"
output_filenames = []
cols = []
x_data = []
history_data = []

if append_to_filename:
	output_filename += append_to_filename_text

for name in column_names:
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

fig = plt.figure( figsize=(8,5) )
ax1 = fig.add_subplot( 111 )
ax1.set_xlabel( "Star age (yr)" )
ax2 = ax1.twinx()
ax1.set_ylabel( column_names[0].replace("_","\_") )
ax2.set_ylabel( column_names[1].replace("_","\_") )

if set_title:
	ax1.set_title( title )
if use_custom_xlim:
	ax1.set_xlim( custom_xlims[0], custom_xlims[1] )
if use_custom_ylim:
	ax1.set_ylim( custom_ylims[0], custom_ylims[1] )

if graph_type == "normal":
	ax1.plot( x_data, history_data[0], color="b", ls="-" )
	ax2.plot( x_data, history_data[1], lw=0 )
elif graph_type == "semilogx":
	ax1.semilogx( x_data, history_data[0], color="b", ls="-" )
	ax2.semilogx( x_data, history_data[1], lw=0 )
elif graph_type == "semilogy":
	ax1.semilogy( x_data, history_data[0], color="b", ls="-" )
	ax2.semilogy( x_data, history_data[1], lw=0 )
elif graph_type == "loglog":
	ax1.loglog( x_data, history_data[0], color="b", ls="-" )
	ax2.loglog( x_data, history_data[1], lw=0 )
else:
	raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )

fig.tight_layout()
plt.savefig( folder_output + "/" + output_filename )

if not keep_figures_open:
	plt.close()
