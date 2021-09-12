# Generalisation of Generic-Plotter.py, but plots the same trend for n different CSVs.

import os
import csv
import matplotlib.pyplot as plt

#----- Define variables -----
parent_dir = "aaa_Data/20210819_1" # Common part of path of all input_folders. Use "" if there is no common part.
input_folders = [ "LOGS_07", "LOGS_08" ]
graph_labels = [ "M=0.66", "M=0.67" ] # Label for the star described by each CSV.
csv_filename = "history.csv" # Forcing this ensures the same data is being compared for each star.
output_dir = input_folders[0]#"" # "a_Comparisons" # To save in parent_dir, leave as empty string ""
extend_filename = "" # Leave as empty string "" if unwanted.
fig_title = "" # Leave as empty string "" if unwanted.
graph_type = "normal" # "normal", "semilogx", "semilogy", "loglog"
line_type = "plot" # "scatter", "plot"
invert_xaxis = False # Use this if x_axis is Teff, for example.

place_legend_outside_plot = True
add_axhline = False
axhline_value = -2.24727217356404 # 2.4846e-9 #1-0.28-1e-4 #1-0.28-1e-4 # 2.4846e-9
highlight_points   = True # Choose ONE point in each trace to stand out in a different colour.
highlight_points_2 = True # Choose ONE extra point in each trace in another different colout.
points_to_highlight   = [ 306, 311 ] # [ 316, 317 ] [ 311, 311 ]
points_to_highlight_2 = [ 328, 327 ] # [ 336, 333 ] [ 335, 331 ]

x_name = "model_number" # star_age
y_name = "X_surf"

markers = [ "o", "s", "*", "h", "X", "D" ] # matplotlib.org/stable/api/markers_api.html
colors = [ "k", "b", "r", "g", "m", "c", "y" ] # matplotlib.org/stable/gallery/color/named_colors.html


#----- Read csv -----
data = [ list(csv.reader(open( os.path.join(parent_dir,f,csv_filename), "r" ))) for f in input_folders ]
headers = [ d[0] for d in data ]
x_cols = [ h.index( x_name ) for h in headers ]
y_cols = [ h.index( y_name ) for h in headers ]
x_vals = [ [] for f in input_folders ]
y_vals = [ [] for f in input_folders ]

for i, d in enumerate( data ):
	for row in d[1:]:

		#Optional filter. Change condition to suit your needs. Comment-out to include the entire CSV. Use one-line for easier commenting-out.
		#if row[2] != fig_title[2:]: continue
		if float(row[0]) < 250 or float(row[0]) > 350: continue # Near main sequence.

		x_vals[i].append(float( row[x_cols[i]] ))
		y_vals[i].append(float( row[y_cols[i]] ))

#----- Plot graph -----
plt.rcParams.update({ "font.size":14 })
plt.rc( "text", usetex=True )
fig = plt.figure( figsize=(7,5) )
ax = fig.add_subplot( 111 )

ax.set_xlabel( x_name.replace("_","\_") )
ax.set_ylabel( y_name.replace("_","\_")  )

if fig_title != "":
	ax.set_title( fig_title )
if invert_xaxis:
	plt.gca().invert_xaxis() 
if graph_type in [ "semilogx", "loglog" ]:
	ax.set_xscale( "log" )
if graph_type in [ "semilogy", "loglog" ]:
	ax.set_yscale( "log" )

# Must be after axis scales, or xlim,ylim not updated.
for i in range(len( input_folders )):
	# Failsafe in case not enough markers or colours defined.
	if i-1 > len( markers ) or i-1 > len( colors ):
		print( "Ran out of unique markers and/or colours. Using last specified value again." )
		j = min( len(markers)-1, len(colors)-1 )
	else:
		j = i

	if line_type == "scatter":
		ax.scatter( x_vals[i], y_vals[i], s=15, color=colors[j], marker="o", label=graph_labels[i], zorder=1 )
	elif line_type == "plot":
		ax.plot( x_vals[i], y_vals[i], lw=1, color=colors[j], ls="-", label=graph_labels[i], zorder=2 )
	
	if highlight_points:
		highlight_j = x_vals[i].index( points_to_highlight[i] )
		plt.scatter( x_vals[i][highlight_j], y_vals[i][highlight_j], s=20, color="r", zorder=3 )
	if highlight_points_2:
		highlight_j2 = x_vals[i].index( points_to_highlight_2[i] )
		plt.scatter( x_vals[i][highlight_j2], y_vals[i][highlight_j2], s=20, color="yellow", zorder=4 )

if add_axhline:
	ax.axhline( axhline_value, color="grey", ls="--" )

fig_filename = os.path.join( parent_dir, output_dir, f"{y_name}-vs-{x_name}".replace("/","") )
if extend_filename != "":
	fig_filename += "_" + extend_filename

if place_legend_outside_plot:
	box = ax.get_position()
	ax.set_position([ box.x0, box.y0, box.width*0.8, box.height ])
	ax.legend( bbox_to_anchor=(1.0,1.0) )
	plt.savefig( fig_filename, bbox_inches="tight" )
else:
	ax.legend( loc="upper right" )
	fig.tight_layout()
	plt.savefig( fig_filename )
