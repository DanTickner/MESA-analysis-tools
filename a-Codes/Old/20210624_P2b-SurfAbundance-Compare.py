import csv
import matplotlib.pyplot as plt

#----- Define variables -----
model_letters = [ "B", "D", "R_original", "RD_original" ] # [ "B", "D", "R", "RD" ]
folder_output = "a_Comparisons_20210623"

species_list = [ "[Li]", "[Fe/H]", "Y" ]
title = r"$M/M_\odot=0.8$, $Z=0.001$"

custom_labels = [ "Standard", "Diffusion", "Rotation", "Rotation and diffusion" ]
line_colours = [ "k", "b", "orange", "red", "green", "grey" ]
line_styles = [ "-", "--", ":", "-.", "-", "-" ]


#----- Preferences -----
use_custom_xlim = False
use_custom_ylim = False
append_to_filename = False
move_title_up = True
show_legend = True
show_endpoint = False

custom_xlim = [ 3.68, 3.70 ]
custom_ylim = [ -17, -9 ]
append_to_filename_text = "age"
title_y = 1.06

x_axis = "model_number" # "Teff" or "age" or "model_number"


#----- Function to plot surface abundance vs Teff -----
def plot_surface_abundance( species, x_axis ):
	
	#----- Definitions -----
	x_vals = [ [] for m in model_letters ]
	abundances = [ [] for m in model_letters ]
	graph_filename = folder_output + "/Abundance-" + species.replace( "/", "" ) + "-vs-" + x_axis
	graph_title = title + ", species: " + species

	if append_to_filename:
		graph_filename += "-" + append_to_filename_text

	#----- Read csv files -----
	for i in range(len( model_letters )):
		with open( model_letters[i] + "/CSV/history.csv", "r" ) as model_csv:
			model_data = csv.reader( model_csv )
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
	
	fig = plt.figure( figsize=(7,5) )
	ax = fig.add_subplot( 111 )
	
	for i in range(len( model_letters )):
		if graph_type == "normal":
			ax.plot( x_vals[i], abundances[i], label=custom_labels[i], color=line_colours[i], ls=line_styles[i], zorder=len(model_letters)-i )
		elif graph_type == "semilogx":
			ax.semilogx( x_vals[i], abundances[i], label=custom_labels[i], color=line_colours[i], ls=line_styles[i], zorder=len(model_letters)-i )
		else:
			raise ValueError( "Graph type %s not recognised." %graph_type )
		if show_endpoint:
			ax.scatter( x_vals[i][-1], abundances[i][-1], s=20, color=line_colours[i], zorder=len(model_letters)-i )
	
	ax.set_xlabel( fig_xlabel )
	ax.set_ylabel( "Surface abundance" )
	
	if use_custom_xlim:
		ax.set_xlim( custom_xlim[0], custom_xlim[1] )
	if use_custom_ylim:
		ax.set_ylim( custom_ylim[0], custom_ylim[1] )
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
