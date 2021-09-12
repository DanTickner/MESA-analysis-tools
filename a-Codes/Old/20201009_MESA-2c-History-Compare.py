import csv
import matplotlib.pyplot as plt


#----- Define variables -----
model_names = [ "B_2agb", "z_newD_R_2agb", "z_mrmb=10_R_2agb" ]
folder_output = "Models/" + model_names[2]
#column_name = "surf_avg_omega_div_omega_crit"
column_name = "surf_avg_v_rot"
#column_name = "star_mass"


#----- Preferences -----
graph_type = "semilogx" # "normal", "semilogx", "semilogy", "loglog"
use_custom_ylabel = False
set_title = True
use_custom_labels = True
use_custom_xlim = False
use_custom_ylim = False
keep_figure_open = True
append_to_filename = False

ylabel = ""
#title = r"$\Omega/\Omega_{\rm{crit}}$ Comparison, varying max\_rotational\_mdot\_boost"
title = r"$v_{\rm{rot}}$ (km/s) Comparison, varying max\_rotational\_mdot\_boost"
#title = r"Star mass Comparison, varying max\_rotational\_mdot\_boost"
custom_labels = [ "No rotation", r"$10^4$ (default)", 10 ]
line_colours = [ "k", "b", "orange", "red", "green", "yellow", "grey" ]
line_styles = [ "-", "--", ":", "-.", "-", "--", ":" ]
custom_xlim = [ 3.7, 3.68 ]
custom_ylim = [ -0.75, -0.5 ]
append_to_filename_text = ""


#----- Don't change (constants, or to be populated by the code) -----
folders_csv = [ "Models/" + m + "/CSV" for m in model_names ]
output_filename = "History-" + column_name + "-Compare"
cols = [ [] for m in model_names ]
star_age = [ [] for m in model_names ]
history_data = [ [] for m in model_names ]

if append_to_filename:
	output_filename += "-" + append_to_filename_text


#----- Read history.csv and extract values -----
for i in range(len( model_names )):
	with open( folders_csv[i] + "/history.csv" ) as data_file:
		data = csv.reader( data_file )
		headers = next( data )
		
		#--- Check age and column are included -----
		for par in [ "star_age", column_name ]:
			if not par in headers:
				raise ValueError( "%s not in history.csv." %par )
			else:
				cols[i].append( headers.index( par ) )
		
		#--- Populate lists ---
		for row in data:
			star_age[i].append( float( row[ cols[i][0] ] ) )
			history_data[i].append( float( row[ cols[i][1] ] ) )
		
#----- Plot graph -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig = plt.figure( figsize=(8,5) )
ax = fig.add_subplot( 111 )
ax.set_xlabel( "Star age (yr)" )
ax.set_ylabel( ylabel if use_custom_ylabel else column_name.replace("_"," ") )
labels = custom_labels if use_custom_labels else model_names

if set_title:
	ax.set_title( title )
if use_custom_xlim:
	ax.set_xlim( custom_xlim[0], custom_xlim[1] )
if use_custom_ylim:
	ax.set_ylim( custom_ylim[0], custom_ylim[1] )

for i in range(len( model_names )):
	if graph_type == "normal":
		ax.plot( star_age[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
	elif graph_type == "semilogx":
		ax.semilogx( star_age[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
	elif graph_type == "semilogy":
		ax.semilogy( star_age[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
	elif graph_type == "loglog":
		ax.loglog( star_age[i], history_data[i], color=line_colours[i], ls=line_styles[i], label=labels[i] )
	else:
		raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )

#--- Put legend outside the plot and save figure ---
box = ax.get_position()
old_width = box.width
ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
ax.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( folder_output + "/" + output_filename, bbox_inches="tight" )

if not keep_figure_open:
	plt.close()
