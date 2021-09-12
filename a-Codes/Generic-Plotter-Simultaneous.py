# As Generic-Plotter.py, but allows you to plot an arbitrary number of columns on the same graph, with the same y-scale.
import os
import csv
import matplotlib.pyplot as plt

#----- Define variables -----
parent_dir = "aaa_Data/20210814/LOGS_0p67B"
output_dir = "" # To save in parent_dir, leave as empty string ""
input_filename = "history.csv" #"allmodels_age.csv"
extend_filename = "test"#"MSTOmarked" # Leave as empty string "" if unwanted.
fig_title = ""# "M=0.69, diffusion" # Leave as empty string "" if unwanted.
graph_type = "semilogy" # "normal", "semilogx", "semilogy", "loglog"
line_type = "plot" # "scatter", "plot"
highlight_point = False			# Highlight a specific point on the HRD.
highlight_modelnumber = 320		# Specify which model to highlight.

x_name = "model_number" # "star_mass" "model_number"
y_names= [ "X_surf", "Y_surf", "Z_surf" ]#[ f"dln(N_abs[{x}])/dlnt" for x in [ "Neut", "H", "He", "Li", "C", "N", "O", "F", "Ne" ] ] #[ "X_surf", "Y_surf", "Z_surf" ]


#----- Read csv -----
data = list(csv.reader(open( os.path.join(parent_dir,input_filename), "r" )))
headers = data[0]
x_col = headers.index( x_name )
y_cols = [ headers.index( y_name ) for y_name in y_names ]
m_col = headers.index( "model_number" )
x_vals = []
y_vals = [ [] for y in y_cols ]
model_number = []
for row in data[1:]:
	if True: # if row[1][:6] == "LOGS_B":
		x_vals.append(float( row[x_col] ))
		[ y_vals[i].append(float( row[y_col] )) for i,y_col in enumerate(y_cols) ]
		model_number.append(float( row[m_col] ))

#----- Plot graph -----
plt.rcParams.update({ "font.size":14 })
plt.rc( "text", usetex=True )
fig = plt.figure( figsize=(7,5) )
ax = fig.add_subplot( 111 )

if fig_title != "":
	ax.set_title( fig_title )
ax.set_xlabel( x_name.replace("_","\_") )

#plt.gca().invert_xaxis() # Use this if x_axis is Teff, for example.

if graph_type in [ "semilogx", "loglog" ]:
	ax.set_xscale( "log" )
if graph_type in [ "semilogy", "loglog" ]:
	ax.set_yscale( "log" )
if line_type == "scatter":
	[ ax.scatter( x_vals, y_vals[i], s=3, label=y_names[i].replace("_","\_") ) for i in range(len(y_vals)) ]
elif line_type == "plot":
	[ ax.plot( x_vals, y_vals[i], label=y_names[i].replace("_","\_") ) for i in range(len(y_vals)) ]
if highlight_point:
	highlight_i = model_number.index( highlight_modelnumber )
	ax.scatter( x_vals[highlight_i], y_vals[highlight_i], s=20, color="b" )
ax.legend(loc="upper right")
	

fig.tight_layout()
fig_filename = os.path.join( parent_dir, output_dir, f"{y_names[0]}-vs-{x_name}".replace("/","") )
if extend_filename != "":
	fig_filename += "_" + extend_filename
plt.savefig( fig_filename )
print( fig_filename)
