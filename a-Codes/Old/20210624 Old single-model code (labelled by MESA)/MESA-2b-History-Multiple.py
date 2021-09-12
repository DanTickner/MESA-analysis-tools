import numpy as np
import csv
import matplotlib.pyplot as plt


#----- Define variables -----
model_name = "Overshoot-False"
column_names = [ "conv_mx2_top", "conv_mx2_bot" ]
filename_desc = "Convective-Regions-mx2"


#----- Preferences -----
graph_type = "semilogx" # "normal", "semilogx", "semilogy", "loglog"
use_custom_labels = True
set_ylabel = True
set_title = True
set_xlim = True
set_ylim = False
add_axhlines = False
keep_fig_open = True

labels = [ "Top", "Bottom" ]
ylabel = r"$q\equiv M(r)/M_{\rm{tot}}$"
title = "Convective region boundaries: conv\_mx2"
xlim = [ 1e6, 1e10 ]
ylim = [ 0, 1 ]
axhlines = [ np.log10(2.5e6) ]

#----- Don't change (constants, or to be populated by the code) -----
csv_folder = "Models/" + model_name + "/CSV"
output_filename = "History-" + filename_desc + "-" + model_name
cols = []
star_age = []
history_data = [ [] for col in column_names ]
colors = [ "k", "b", "grey", "yellow", "orange", "blue", "blue", "blue", "blue" ]
labels_final = labels if use_custom_labels else [ name.replace("_"," ") for name in column_names ]


#----- Escape code if not enough colours were defined -----
if len( colors ) < len( column_names ):
	raise ValueError( "Please define more colours for the plots. Have %s, need %s." %( len(colors), len(column_names) ) )


#----- Read history.csv and extract values -----
with open( csv_folder + "/history.csv" ) as data_file:
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
		# Iterate through chosen columns. Offset by 1 because cols[0] is star_age.
		for i in range(len( cols[1:] )):
			history_data[i].append( float( row[ cols[i+1] ] ) )


#----- Plot graph -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig = plt.figure( figsize=(7,5) )
ax = fig.add_subplot( 111 )
ax.set_xlabel( "Star age (yr)" )
if set_title:
	ax.set_title( title )
if set_ylabel:
	ax.set_ylabel( ylabel )
if set_xlim:
	ax.set_xlim( xlim[0], xlim[1] )
if set_ylim:
	ax.set_ylim( ylim[0], ylim[1] )

for i in range(len( column_names )):
	if graph_type == "normal":
		ax.plot( star_age, history_data[i], label=labels_final[i], color=colors[i], zorder=i )
	elif graph_type == "semilogx":
		ax.semilogx( star_age, history_data[i], label=labels_final[i], color=colors[i], zorder=i )
	elif graph_type == "semilogy":
		ax.semilogy( star_age, history_data[i], label=labels_final[i], color=colors[i], zorder=i )
	elif graph_type == "loglog":
		ax.loglog( star_age, history_data[i], label=labels_final[i], color=colors[i], zorder=i )
	else:
		raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )

if add_axhlines:
	[ ax.axhline( line, color="grey", ls=":", zorder=0 ) for line in axhlines ]

#--- Put legend outside the plot and save ---
box = ax.get_position()
ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
ax.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( "Models/" + model_name + "/" + output_filename, bbox_inches="tight" )

if not keep_fig_open:
	plt.close()