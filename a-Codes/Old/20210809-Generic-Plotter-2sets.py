# Reason archived: Generalised to plot n different sets of data.

import os
import csv
import matplotlib.pyplot as plt

#----- Define variables -----
parent_dir = "aaa_Data"
output_dir = "" # "a_Comparisons" # To save in parent_dir, leave as empty string ""
input_filename = "20210808_basic_v_diffusion.csv" #"allmodels_age.csv"
extend_filename = "" # Leave as empty string "" if unwanted.
fig_title = "" # Leave as empty string "" if unwanted.
graph_type = "semilogy" # "normal", "semilogx", "semilogy", "loglog"

x_name = "Mass" # "star_mass"
y_name = "Rho[Li]" # "A(Li)" "N[H]"


#----- Read csv -----
data = list(csv.reader(open( os.path.join(parent_dir,input_filename), "r" )))
headers = data[0]
x_col = headers.index( x_name )
y_col = headers.index( y_name )
x_vals = [ [], [] ]
y_vals = [ [], [] ]
for row in data[1:]:
	if True:# if row[1][:6] == "LOGS_B":
		if row[0] == "Basic":
			x_vals[0].append(float( row[x_col] ))
			y_vals[0].append(float( row[y_col] ))
		else:
			x_vals[1].append(float( row[x_col] ))
			y_vals[1].append(float( row[y_col] ))

#----- Plot graph -----
plt.rcParams.update({ "font.size":14 })
plt.rc( "text", usetex=True )
fig = plt.figure( figsize=(7,5) )
ax = fig.add_subplot( 111 )

if fig_title != "":
	ax.set_title( fig_title )
ax.set_xlabel( x_name.replace("_","\_") )
ax.set_ylabel( y_name.replace("_","\_")  )
#plt.gca().invert_xaxis()

if graph_type in [ "semilogx", "loglog" ]:
	ax.set_xscale( "log" )
if graph_type in [ "semilogy", "loglog" ]:
	ax.set_yscale( "log" )
ax.scatter( x_vals[0], y_vals[0], s=5, color="orange", label="No diffusion or rotation" ) # Must be after axis scales, or xlim,ylim not updated.
ax.scatter( x_vals[1], y_vals[1], s=5, color="blue", label="Diffusion and rotation" ) # Must be after axis scales, or xlim,ylim not updated.
ax.legend( loc="upper right" )

fig.tight_layout()
fig_filename = os.path.join( parent_dir, output_dir, f"{y_name}-vs-{x_name}" )
if extend_filename != "":
	fig_filename += "_" + extend_filename
plt.savefig( fig_filename )
