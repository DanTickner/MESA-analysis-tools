import csv
import matplotlib.pyplot as plt

#----- Define variables -----
model_letters = [ "B", "D", "R", "RD" ]
model_stages = [ "1prems", "2agb", "3wd" ]


#----- Preferences -----
interval = 200 # Time between gif frames (in ms)
n_frames = 20 # Number of gif frames
frame_duration = 400 # milliseconds

show_endpoint = True
set_title = True
add_to_title = True # not yet implemented
use_custom_labels = True
use_custom_xlim = False
use_custom_ylim = False
append_filenames_for_model_letters = [ False, False, False, False ]
append_filename_HRD = False


title = r"$M/M_\odot=0.8$, $Z=0.001$"
add_to_title_text = r", D\_SH\_factor=0"
custom_labels = [ "Standard", "Diffusion", "Rotation", "Rotation and diffusion" ]
line_colours = [ "k", "b", "orange", "red", "green", "grey" ]
line_styles = [ "-", "--", ":", "-.", "-", "-" ]
custom_xlim = [ 3.7, 3.68 ]
custom_ylim = [ -0.75, -0.5 ]
append_filenames_text = [ "", "", "-D_SH=0" , "-D_SH=0" ]
append_filename_HRD_text = "-D_SH=0"


#----- Function to plot and compare HRDs for each evolutionary stage -----
def plot_HRDs( stage ):
	
	print( "\nPlotting HRD: " + stage )
	#----- Don't change (constants, or to be populated by the code) -----
	filename_HRD = "HRD-Comparison"
	model_names = [ ml + "_" + stage for ml in model_letters ]
	folder_output = "Models/aaa_Comparisons/" + stage
	
	folders_csv = []
	for  i_m, m in enumerate( model_names ):
		the_folder = m
		if append_filenames_for_model_letters[i_m]:
			the_folder +=  append_filenames_text[i_m]
		folders_csv.append( "Models/" + the_folder + "/CSV" )
	
	if append_filename_HRD:
		filename_HRD += append_filename_HRD_text
		
	log_Teff = [ [] for m in model_names ]
	log_L = [ [] for m in model_names ]
	star_age = [ [] for m in model_names ]
	cols = [ [] for m in model_names ]
	labels = custom_labels if use_custom_labels else model_names
	
	
	#----- Read csv and extract values -----
	for i in range( len( model_names ) ):
		print( "Reading CSV: " + folders_csv[i] + "/history.csv" )
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
		if append_filename_HRD:
			graph_v_time_filename += append_filename_HRD_text
		
		if set_title:
			if stage == "1prems":
				stage_text = ", Pre-MS"
			elif stage == "2agb":
				stage_text = ", MS to AGB"
			elif stage == "3wd":
				stage_text = ", WD"
			
			the_title = param + " vs Teff, " + title + stage_text
			if add_to_title:
				the_title += add_to_title_text
				
			ax.set_title( the_title )
				
		for i in range(len( model_names )):
			ax.semilogx( star_age[i], lst[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_names)-i )
		
		#--- Put legend outside the plot and save figure ---
		box = ax.get_position()
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
		the_title = title + stage_text
		if add_to_title:
			the_title += add_to_title_text
		ax.set_title( the_title )
	if use_custom_xlim:
		ax.set_xlim( custom_xlim[0], custom_xlim[1] )
	if use_custom_ylim:
		ax.set_ylim( custom_ylim[0], custom_ylim[1] )
	
	for i in range(len( model_names )):
		ax.plot( log_Teff[i], log_L[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_names)-i )
	
	if show_endpoint:
		for i in range(len( model_names )):
			ax.scatter( log_Teff[i][-1], log_L[i][-1], s=20, color=line_colours[i], zorder=len(model_names)-i )
	
	#--- Put legend outside the plot and save figure ---
	box = ax.get_position()
	ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
	ax.legend( bbox_to_anchor=(1.0,1.0) )
	plt.savefig( folder_output + "/" + filename_HRD, bbox_inches="tight" )
	plt.close()


#----- Call the functions -----
for ms in model_stages:
	plot_HRDs( ms )