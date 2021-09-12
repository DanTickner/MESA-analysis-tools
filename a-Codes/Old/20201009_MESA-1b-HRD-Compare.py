import csv
import matplotlib.pyplot as plt

#----- Define variables -----
m1_name = "0p8M_Rotation_2_end_agb"
m2_name = "0p8M_Rotation_Slow_2_end_agb"
folder_output = "Models/" + m1_name


#----- Preferences -----
interval = 200 # Time between gif frames (in ms)
n_frames = 20 # Number of gif frames
frame_duration = 400 # milliseconds

show_endpoint = True
set_title = True
use_custom_legends = True
keep_figure_open = True
use_custom_xlim = False
use_custom_ylim = False
append_to_filename = False

title = r"$M/M_\odot=0.8$, $Z=0.001$"
custom_legends = [ r"$\Omega/\Omega_{\rm{crit}}=0.2$", r"$\Omega/\Omega_{\rm{crit}}=0.05$" ]
custom_xlim = [ 3.7, 3.68 ]
custom_ylim = [ -0.75, -0.5 ]
append_to_filename_text = "-zoomed"


#----- Don't change (constants, or to be populated by the code) -----
hrd_filename = "HRD-" + m1_name + "-and-" + m2_name
folders_csv = [ "Models/" + m + "/CSV" for m in [ m1_name, m2_name ] ]
folders_main = []
log_Teff = [ [], [] ]
log_L = [ [], [] ]
cols = [ [], [] ]


#----- Read csv and extract values -----
for i in range( 2 ):
	with open( folders_csv[i] + "/history.csv" ) as data_file:
		data = csv.reader( data_file )
		headers = next( data )
		
		#--- Check T and L are included -----
		for par in [ "log_Teff", "log_L" ]:
			if not par in headers:
				raise ValueError( "%s not in history.csv." %par )
			else:
				cols[i].append( headers.index( par ) )
				
		#--- Populate T and L lists ---
		for row in data:
			log_Teff[i].append( float( row[ cols[i][0] ] ) )
			log_L[i].append( float( row[ cols[i][1] ] ) )


#----- Plot HRD -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig = plt.figure( figsize=(8,5) )
ax = fig.add_subplot( 111 )
ax.invert_xaxis()
ax.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax.set_ylabel( r"$\log(L/L_\odot)$" )
labels = custom_legends if use_custom_legends else [ m1_name, m2_name ] 

if set_title:
	ax.set_title( title )
if use_custom_xlim:
	ax.set_xlim( custom_xlim[0], custom_xlim[1] )
if use_custom_ylim:
	ax.set_ylim( custom_ylim[0], custom_ylim[1] )
if append_to_filename:
	hrd_filename += append_to_filename_text

ax.plot( log_Teff[0], log_L[0], color="k", ls="-", label=labels[0] )
ax.plot( log_Teff[1], log_L[1], color="b", ls="--", label=labels[1] )

if show_endpoint:
	ax.scatter( log_Teff[0][-1], log_L[0][-1], s=20, color="k" )
	ax.scatter( log_Teff[1][-1], log_L[1][-1], s=20, color="b" )

#--- Put legend outside the plot and save figure ---
box = ax.get_position()
old_width = box.width
ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
ax.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( folder_output + "/" + hrd_filename, bbox_inches="tight" )

if not keep_figure_open:
	plt.close()