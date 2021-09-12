import os
import csv
import matplotlib.pyplot as plt

#----- Define variables -----
parent_dir = "aaa_Data/20210809b/LOGS_01"
output_dir = "aaa_Data/Image_Backup/20210910_report" # To save in parent_dir, leave as empty string ""
input_filename = "history.csv" #"allmodels_age_modified.csv"
extend_filename = "20210910b01" # Leave as empty string "" if unwanted.
fig_title = "" # Leave as empty string "" if unwanted.
graph_type = "loglog" # "normal", "semilogx", "semilogy", "loglog"
line_type = "scatter" # "scatter", "plot"
use_custom_markersize = True
custom_markersize = 12
highlight_point = False			# Highlight a specific point on the plot.
highlight_modelnumber = 320		# Specify which model to highlight.
invert_xaxis = False	# Use this if x_axis is Teff, for example.
add_axhline = False
axhline = 2.7

x_name = "new_omega_div_omega_crit" # "star_mass" "model_number"
y_name = "surf_avg_v_rot" # "A(Li)" "N[H]"


#----- Read csv -----
data = list(csv.reader(open( os.path.join(parent_dir,input_filename), "r" )))
headers = data[0]
x_col = headers.index( x_name )
y_col = headers.index( y_name )
m_col = headers.index( "model_number" )
x_vals = []
y_vals = []
model_number = []
for row in data[1:]:
	# Optional filtering condition. Replace with "if True:" if unwanted.
	if row[1] != "LOGS_20":
	#if True:
		x_vals.append(float( row[x_col] ))
		y_vals.append(float( row[y_col] ))
		model_number.append(float( row[m_col] ))

#----- Plot graph -----
plt.rcParams.update({ "font.size":14 })
plt.rc( "text", usetex=True )
fig = plt.figure( figsize=(6,6/1.414) )
ax = fig.add_subplot( 111 )

if fig_title != "":
	ax.set_title( fig_title )
ax.set_xlabel( x_name.replace("_","\_") )
ax.set_ylabel( y_name.replace("_","\_")  )

if invert_xaxis:
	plt.gca().invert_xaxis()

if graph_type in [ "semilogx", "loglog" ]:
	ax.set_xscale( "log" )
if graph_type in [ "semilogy", "loglog" ]:
	ax.set_yscale( "log" )
if line_type == "scatter":
	if use_custom_markersize:
		markersize = custom_markersize
	else:
		markersize = 3
	ax.scatter( x_vals, y_vals, s=markersize, zorder=0 ) # Must be after axis scales, or xlim,ylim not updated.
elif line_type == "plot":
	ax.plot( x_vals, y_vals ) # Must be after axis scales, or xlim,ylim not updated.
if highlight_point:
	highlight_i = model_number.index( highlight_modelnumber )
	ax.scatter( x_vals[highlight_i], y_vals[highlight_i], s=20, color="b", zorder=1 )
if add_axhline:
	ax.axhline( axhline, color="grey", ls="--", lw=1.5, zorder=-1 )

#ax.set_xlim( 0, 0.53 )
#ax.set_ylim( 0, 430 )
	

fig.tight_layout()
if output_dir == "":
	fig_filename = os.path.join( input_dir, f"{y_name}-vs-{x_name}" )
else:
	fig_filename = os.path.join( output_dir, f"{y_name}-vs-{x_name}" )
if extend_filename != "":
	fig_filename += "_" + extend_filename
plt.savefig( fig_filename )
