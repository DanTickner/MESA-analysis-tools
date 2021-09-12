import csv
import matplotlib.pyplot as plt

#----- Define variables -----
model_names = [ "B_2agb", "z_mrmb=10_R_2agb", "z_2020-10-11-a-relax_R_2agb" ]
folder_output = "Models/" + model_names[2]


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

title = r"Rotation comparison"
custom_legends = [ "No rotation", "Previous", r"Relax $\Omega$" ]
line_colours = [ "k", "b", "orange", "red", "green", "yellow", "grey" ]
line_styles = [ "-", "--", ":", "-.", "-", "--", ":" ]
custom_xlim = [ 3.7, 3.68 ]
custom_ylim = [ -0.75, -0.5 ]
append_to_filename_text = "Dfactors-All-But-One"


#----- Don't change (constants, or to be populated by the code) -----
hrd_filename = "HRD-Comparison"
folders_csv = [ "Models/" + m + "/CSV" for m in model_names ]
folders_main = []
log_Teff = [ [] for m in model_names ]
log_L = [ [] for m in model_names ]
star_age = [ [] for m in model_names ]
cols = [ [] for m in model_names ]
labels = custom_legends if use_custom_legends else model_names


#----- Read csv and extract values -----
for i in range( len( model_names ) ):
	with open( folders_csv[i] + "/history.csv" ) as data_file:
		data = csv.reader( data_file )
		headers = next( data )
		
		#--- Check T and L are included -----
		for par in [ "log_Teff", "log_L", "star_age" ]:
			if not par in headers:
				raise ValueError( "%s not in history.csv." %par )
			else:
				cols[i].append( headers.index( par ) )
				
		#--- Populate T and L lists ---
		for row in data:
			log_Teff[i].append( float( row[ cols[i][0] ] ) )
			log_L[i].append( float( row[ cols[i][1] ] ) )
			star_age[i].append( float( row[ cols[i][2] ] ) )


#----- Temperature vs time and luminosity vs time -----
for param, ylabel, lst in zip( ["Temperature","Luminosity"], [r"$\log(T_{\rm{eff}})$",r"$\log(L/L_\odot)$"], [log_Teff,log_L] ):
	fig = plt.figure( figsize=(8,5) )
	ax = fig.add_subplot( 111 )
	ax.set_xlabel( r"$\log(t\rm{ (yr)})$" )
	ax.set_ylabel( ylabel )
	graph_v_time_filename = "HRD-Comparison-" + param + "-vs-Time"
	
	if append_to_filename:
		graph_v_time_filename += "-" + append_to_filename_text
	
	for i in range(len( model_names )):
		ax.semilogx( star_age[i], lst[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_names)-i )
	
	#--- Put legend outside the plot and save figure ---
	box = ax.get_position()
	old_width = box.width
	ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
	ax.legend( bbox_to_anchor=(1.0,1.0) )
	plt.savefig( folder_output + "/" + graph_v_time_filename, bbox_inches="tight" )
	plt.close()


#----- Plot HRD -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig = plt.figure( figsize=(8,5) )
ax = fig.add_subplot( 111 )
ax.invert_xaxis()
ax.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax.set_ylabel( r"$\log(L/L_\odot)$" )

if set_title:
	ax.set_title( title )
if use_custom_xlim:
	ax.set_xlim( custom_xlim[0], custom_xlim[1] )
if use_custom_ylim:
	ax.set_ylim( custom_ylim[0], custom_ylim[1] )
if append_to_filename:
	hrd_filename += "-" + append_to_filename_text

for i in range(len( model_names )):
	ax.plot( log_Teff[i], log_L[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_names)-i )

if show_endpoint:
	for i in range(len( model_names )):
		ax.scatter( log_Teff[i][-1], log_L[i][-1], s=20, color=line_colours[i], zorder=len(model_names)-i )

#--- Put legend outside the plot and save figure ---
box = ax.get_position()
old_width = box.width
ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
ax.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( folder_output + "/" + hrd_filename, bbox_inches="tight" )

if not keep_figure_open:
	plt.close()
