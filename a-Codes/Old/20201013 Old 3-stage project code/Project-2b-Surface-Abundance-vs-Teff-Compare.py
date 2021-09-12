import csv
import matplotlib.pyplot as plt

#----- Define variables -----
model_letters = [ "B", "D", "R", "RD" ]
model_stages = [ "1prems", "2agb", "3wd" ]

species_list = [ "li7", "he4" ]
title = r"$M/M_\odot=0.8$, $Z=0.001$"

custom_labels = [ "Standard", "Diffusion", "Rotation", "Rotation and diffusion" ]
line_colours = [ "k", "b", "orange", "red", "green", "grey" ]
line_styles = [ "-", "--", ":", "-.", "-", "-" ]


#----- Preferences -----
abundance_is_log = True
use_custom_xlim = False
use_custom_ylim = False
move_title_up = True

custom_xlim = [ 3.68, 3.70 ]
custom_ylim = [ -20.2, -19.5 ]
title_y = 1.06


#----- Function to plot surface abundance vs Teff -----
def plot_surface_abundance( species, stage ):
	
	#----- Definitions -----
	model_names = [ ml + "_" + stage for ml in model_letters ]
	log_Teff = [ [] for m in model_names ]
	log_abundances = [ [] for m in model_names ]
	graph_filename = "Models/aaa_Comparisons/" + stage + "/Compare-Abundance-" + species
	graph_title = title
	
	if stage == "1prems":
		graph_title += ", Pre-MS"
	elif stage == "2agb":
		graph_title += ", MS to AGB"
	elif stage == "3wd":
		graph_title += ", WD"
	
	graph_title += ", species: " + species
	#----- Read csv files -----
	for i in range(len( model_names )):
		with open( "Models/" + model_names[i] + "/CSV/history.csv", "r" ) as model_csv:
			model_data = csv.reader( model_csv )
			headers = next( model_data )
			log_Teff_col = headers.index( "log_Teff" )
			species_col = headers.index( "log_surface_" + species )
	
			for j, row in enumerate( model_data ):
				log_Teff[i].append( float( row[ log_Teff_col ] ) )
				
				if abundance_is_log:
					log_abundances[i].append( float( row[ species_col ] ) )
				else:
					log_abundances[i].append( 10**float( row[ species_col ] ) )
		
	
	#----- Plot graph -----
	plt.rcParams.update({ "font.size": 14 })
	plt.rc( "text", usetex=True )
	
	fig = plt.figure( figsize=(7,5) )
	ax = fig.add_subplot( 111 )
	
	for i in range(len( model_names )):
		ax.plot( log_Teff[i], log_abundances[i], label=custom_labels[i], color=line_colours[i], ls=line_styles[i], zorder=len(model_names)-i )
		ax.scatter( log_Teff[i][-1], log_abundances[i][-1], s=20, color=line_colours[i], zorder=len(model_names)-i )
	
	ax.set_xlabel( r"$\log(T_{\rm{eff}})$" )
	
	if abundance_is_log:
		ax.set_ylabel( "Log surface abundance" )
	else:
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
	box = ax.get_position()
	ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
	ax.legend( bbox_to_anchor=(1.0,1.0) )
	plt.savefig( graph_filename, bbox_inches="tight" )
	plt.close()


#----- Call the function -----
for sp in species_list:
	for ms in model_stages:
		plot_surface_abundance( sp, ms )