# Special case of Generic-Plotter-n.py. Includes an application-specific code snippet to read allmodels_age.csv and extract the correct point to highlight.
# Combine all history.csv into one single file (using P5b-Combine-CSVs.py). Then use the "optional filter" to choose the file you want.

import os
import csv
import matplotlib.pyplot as plt

#----- Define variables -----
parent_dir = "aaa_Data/20210814"
input_filename = "20210814.csv" #"allmodels_age.csv"
output_dir = "" # "a_Comparisons" # To save in parent_dir, leave as empty string ""
extend_filename = "0p69" # Leave as empty string "" if unwanted.
fig_title = extend_filename.replace("p",".") # Leave as empty string "" if unwanted. # Reference added 20210813 for convenience. Remove when done.
graph_type = "normal" # "normal", "semilogx", "semilogy", "loglog"

place_legend_outside_plot = True
add_axhline = False
axhline_value = -2.24727217356404 # 2.4846e-9 #1-0.28-1e-4 #1-0.28-1e-4 # 2.4846e-9
highlight_points = True # Choose ONE point in each trace to stand out in a different colour.
points_to_highlight = [] # Code fills this out automatically.

x_name = "model_number" # "star_mass"
y_name = "X_surf" # "A(Li)" "N[H]"

linestyles = [ "-", "--", ":", "-." ] # matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html?highlight=linestyles#matplotlib.lines.Line2D.lineStyles
colors = [ "k", "r", "g", "m", "c", "y" ] # matplotlib.org/stable/gallery/color/named_colors.html

#----- Extract model_number at 13 Gyr -----
data_13Gyr = list(csv.reader(open( os.path.join(parent_dir,"allmodels_age.csv"), "r" )))
headers_13Gyr = data_13Gyr[0]
star = [ row[1] for row in data_13Gyr[1:] ]
model_number = [ row[2] for row in data_13Gyr[1:] ]

#----- Read csv -----
data = list(csv.reader(open( os.path.join(parent_dir,input_filename), "r" )))
headers = data[0]
x_col = headers.index( x_name )
y_col = headers.index( y_name )
x_vals = []
y_vals = []
dataset_names = []

for row in data[1:]:

	#Optional filter. Change condition to suit your needs. Comment-out to include the entire CSV.
	#if "excl" in row[0] or "Rot_+_Diff" in row[0]:
	#if row[2] != fig_title[2:]:
	if row[0][5:9] != extend_filename:
		continue
	
	star_name = row[0].replace("/history.csv","")

	if not star_name in dataset_names:
		dataset_names.append( star_name )
		x_vals.append( [] )
		y_vals.append( [] )
		points_to_highlight.append(float( model_number[ star.index(star_name) ] ))

	i = dataset_names.index( star_name )
	x_vals[i].append(float( row[x_col] ))
	y_vals[i].append(float( row[y_col] ))

#----- Plot graph -----
plt.rcParams.update({ "font.size":14 })
plt.rc( "text", usetex=True )
fig = plt.figure( figsize=(7,5) )
ax = fig.add_subplot( 111 )

if fig_title != "":
	ax.set_title( fig_title )
ax.set_xlabel( x_name.replace("_","\_") )
ax.set_ylabel( y_name.replace("_","\_")  )

#plt.gca().invert_xaxis() # Use this if x_axis is Teff, for example.

if graph_type in [ "semilogx", "loglog" ]:
	ax.set_xscale( "log" )
if graph_type in [ "semilogy", "loglog" ]:
	ax.set_yscale( "log" )

# Must be after axis scales, or xlim,ylim not updated.
for i in range(len( dataset_names )):
	# Failsafe in case not enough markers or colours defined.
	if i-1 > len( linestyles ) or i-1 > len( colors ):
		print( "Ran out of unique markers and/or colours. Using last specified value again." )
		j = min( len(linestyles)-1, len(colors)-1 )
	else:
		j = i
	ax.plot( x_vals[i], y_vals[i], lw=1, color=colors[j], ls=linestyles[j], label=dataset_names[i][-1] )

	if highlight_points:
		highlight_j = x_vals[i].index( points_to_highlight[i] )
		plt.scatter( x_vals[i][highlight_j], y_vals[i][highlight_j], s=20, color="b" )

if add_axhline:
	ax.axhline( axhline_value, color="grey", ls="--" )

#ax.set_ylim( 0.8e-4, 1.2e-4 )

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
