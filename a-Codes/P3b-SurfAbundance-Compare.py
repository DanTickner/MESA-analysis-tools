import os
import csv
import matplotlib.pyplot as plt

#----- Define variables -----
parent_dir    = "aaa_Data" # Where B,D,R,RD folders saved. Leave as empty string to look in current directory.
folder_output = "a_Comparisons" # Code will automatically add parent_dir to this. Just name the folder.
models = [ "20210809_B/LOGS_17", "20210809_D_incH/LOGS_17", "20210809_R/LOGS_17", "20210809_RD_incH/LOGS_17" ]
folder_output = "Image_Backup/20210910_report/HRD-M=0p76"

species_list  = [ "A(Li)", "[Fe/H]_surf", "Y_surf" ]
title         = r"$Z=10^{-4}$" # r"$M/M_\odot=0.8$, $Z=0.001$"

line_colours  = [ "k", "b", "orange", "red", "green", "grey", "yellow" ]
line_styles   = [ "-", "--", ":", "-.", "-", "--", ":" ]


#----- Preferences -----
use_custom_xlim = False
use_custom_ylim = False
append_to_filename = False
add_title = False
use_custom_ylabel = True
move_title_up = True
show_legend = False
show_endpoint = False
use_custom_labels = True

custom_xlim = [ 3.68, 3.70 ]
custom_ylim = [ -17, -9 ]
append_to_filename_text = "age"
custom_ylabel_text = [ r"Lithium abundance $A(\rm{Li})$", r"Surface metallicity $[\rm{Fe}/\rm{H}]$", r"Surface He mass fraction $Y$" ]
title_y = 1.06

x_axis = "model_number" # "Teff" or "age" or "model_number"

# Option to read all folders in "loc", saves specifying models. Ignores files, but will fail if "loc" contains any folders that are not MESA logs. If in doubt, place logs in a nested folder and change loc to that.
use_all_folders = False
if use_all_folders:
	models = [ obj for obj in os.listdir( parent_dir ) if os.path.isdir(os.path.join( parent_dir, obj )) ]
	models.remove( "a_Comparisons" )

if parent_dir != "":
	folder_output = parent_dir + "/" + folder_output
custom_labels = [ "M=0." + str(m)[-2:] for m in models ] # [ "Standard", "Diffusion", "Rotation", "Rotation and diffusion" ]
labels = custom_labels if use_custom_labels else models

#----- Function to plot surface abundance vs Teff -----
def plot_surface_abundance( species, x_axis ):
	
	#----- Definitions -----
	x_vals = [ [] for m in models ]
	abundances = [ [] for m in models ]
	graph_filename = folder_output + "/Abundance-" + species.replace( "/", "" ) + "-vs-" + x_axis
	graph_title = title + ", species: " + species

	if append_to_filename:
		graph_filename += "-" + append_to_filename_text

	#----- Read csv files -----
	for i in range(len( models )):
		if parent_dir == "":
			the_folder = models[i]
		else:
			the_folder = parent_dir + "/" + models[i]

		model_data = csv.reader(open( the_folder + "/history.csv", "r" ))
		headers = next( model_data )

		if x_axis == "Teff":
			x_col_name = "log_Teff"
			fig_xlabel = r"$\log(T_{\rm{eff}})$"
			graph_type = "normal"
		elif x_axis == "age":
			x_col_name = "star_age"
			fig_xlabel = "Star age (yr)"
			graph_type = "normal"
		elif x_axis == "model_number":
			x_col_name = "model_number"
			fig_xlabel = "Model number"
			graph_type = "normal"
		else:
			raise ValueError( "X-column %s not understood. Please choose 'Teff' or 'age'." %Teff_or_age )

		x_col = headers.index( x_col_name )
		species_col = headers.index( species )

		for j, row in enumerate( model_data ):
			x_vals[i].append( float( row[ x_col ] ) )
			abundances[i].append( float( row[ species_col ] ) )
		
	
	#----- Plot graph -----
	plt.rcParams.update({ "font.size": 14 })
	plt.rc( "text", usetex=True )
	
	fig = plt.figure( figsize=(6,6/1.414) )
	ax = fig.add_subplot( 111 )
	
	for i in range(len( models )):
		col = 1 - ( i+1 ) / ( len(models) + 1 )
		if graph_type == "normal":
			ax.plot( x_vals[i], abundances[i], label=labels[i], color=line_colours[i], ls=line_styles[i], zorder=len(models)-i )
			#ax.plot( x_vals[i], abundances[i], label=labels[i], color=(col,col,col), ls="-", zorder=len(models)-i )
		elif graph_type == "semilogx":
			ax.semilogx( x_vals[i], abundances[i], label=labels[i], color=line_colours[i], ls=line_styles[i], zorder=len(models)-i )
		else:
			raise ValueError( "Graph type %s not recognised." %graph_type )
		if show_endpoint:
			ax.scatter( x_vals[i][-1], abundances[i][-1], s=20, color=line_colours[i], zorder=len(models)-i )
	
	ax.set_xlabel( fig_xlabel )
	if use_custom_ylabel:
		ax.set_ylabel( custom_ylabel_text[ species_list.index( species ) ] )
	else:
		ax.set_ylabel( "Surface abundance" )
	
	if use_custom_xlim:
		ax.set_xlim( custom_xlim[0], custom_xlim[1] )
	if use_custom_ylim:
		ax.set_ylim( custom_ylim[0], custom_ylim[1] )
	if add_title:
		if move_title_up:
			ax.set_title( graph_title, y=title_y )
		else:
			ax.set_title( graph_title )
	
	#--- Put legend outside the plot and save ---
	if show_legend:
		box = ax.get_position()
		ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
		ax.legend( bbox_to_anchor=(1.0,1.0) )
	plt.savefig( graph_filename, bbox_inches="tight" )
	print( graph_filename )
	plt.close()


#----- Call the function -----
print( "Plots saved:" )
for x_axis in [ "Teff", "age", "model_number" ]:
	for sp in species_list :
		plot_surface_abundance( sp, x_axis )
