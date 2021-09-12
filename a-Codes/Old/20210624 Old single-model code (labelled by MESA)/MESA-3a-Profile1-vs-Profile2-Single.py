import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import Create_GIF


#----- Define variables -----
model_name = "z_SH=ES=0_R_2agb"
y_column = "omega_div_omega_crit"
x_column = "logT"# mass, zone, q, logT...


#----- Preferences -----
use_custom_filename = False
invert_xaxis = True
set_xlabel = False
set_ylabel = False
set_xlim = False
set_ylim = False
add_axhlines = True

graph_type = "normal"
frame_duration = 400

custom_filename = "Overshoot"
xlabel = ""
ylabel = ""
xlim = [ 0, 1]
ylim = [ -105, -95 ]
axhlines = [ 1 ]


#----- Don't change (constants, or to be populated by the code) -----
filename_final = custom_filename if use_custom_filename else y_column.replace("_"," ") + "-vs-" + x_column.replace("_"," ") + "-"
csv_folder = "Models/" + model_name + "/CSV"
output_folder = "Models/" + model_name
output_frames_folder = output_folder + "/" + filename_final + "Frames"
cols = []
model_number = []
star_age = []
y_data = []
x_data = []
last_pn = 0# Keep track of previous row in csv, to start new list when profile number changes
profile_number = []


#----- Make sure specified paths exist; create them if not -----
if not os.path.exists( output_frames_folder ):
	os.mkdir( output_frames_folder )


#----- Read profiles-data.csv -----
with open( csv_folder + "/profiles-data.csv", "r" ) as file_pd:
	data_pd = csv.reader( file_pd )
	headers_pd = next( data_pd )
	
	#--- Check data included ---
	for par in [ "profile_number", x_column, y_column ]:
		if not par in headers_pd:
			raise ValueError( "%s not in profiles-data.csv." %par )
		else:
			cols.append( headers_pd.index( par ) )
	
	#--- Populate lists ---
	for row in data_pd:
		
		#--- Are we still looking at the same profile? ---
		this_pn = int(float( row[ cols[0] ] ))
		
		if this_pn > last_pn:
			
			y_data.append( [] )
			x_data.append( [] )
			model_number.append( 0 )# To be updated later
			star_age.append( 0 )# To be updated later
			
			if not this_pn in profile_number:
				profile_number.append( this_pn )
		
		last_pn = this_pn
		
		#--- Add data ---
		i = profile_number.index( this_pn )
		x_data[ i ].append(float( row[ cols[1] ] ))
		y_data[ i ].append(float( row[ cols[2] ] ))


#----- Obtain star_age and model_number as a function of profile_number -----
with open( csv_folder + "/profiles.csv" ) as file_p:
	data_p = csv.reader( file_p )
	headers_p = next( data_p )
	m, p, s = [ headers_p.index( "model_number" ), headers_p.index( "profile_number" ), headers_p.index( "star_age" ) ]

	for row in data_p:
		p_i = profile_number.index(int(float( row[p] )))
		model_number[ p_i ] = int(float( row[m] ))
		star_age[ p_i ] = float( row[s] )


#----- Plot a graph for each profile_number -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })
fig = plt.figure( figsize=(8,5) )
ax = fig.add_subplot( 111 )
xlim_final = xlim if set_xlim else [ min([ min(lst) for lst in x_data ])*0.9, max([ max(lst) for lst in x_data ])*1.1 ]
ylim_final = ylim if set_ylim else [ min([ min(lst) for lst in y_data ])*0.9, max([ max(lst) for lst in y_data ])*1.1 ]
xlabel_final = xlabel if set_xlabel else r"%s" %x_column.replace("_","\_")
ylabel_final = ylabel if set_ylabel else r"%s" %y_column.replace("_","\_")

for i in range(len( star_age )):
	
	#--- Keep same figure open but reset it ---
	ax.clear()
	ax.set_xlabel( xlabel_final )
	ax.set_ylabel( ylabel_final )
	ax.set_xlim( xlim_final[0], xlim_final[1] )
	ax.set_ylim( ylim_final[0], ylim_final[1] )
	if invert_xaxis:
		plt.gca().invert_xaxis()
	if add_axhlines:
		[ ax.axhline( x, color="grey", ls="--" ) for x in axhlines ]

	#--- Plot gaph of the chosen type ---
	if graph_type == "normal":
		ax.plot( x_data[i], y_data[i] )
	elif graph_type == "semilogx":
		ax.semilogx( x_data[i], y_data[i] )
	elif graph_type == "semilogy":
		ax.semilogy( x_data[i], y_data[i] )
	elif graph_type == "loglog":
		ax.loglog( x_data[i], y_data[i] )
	else:
		raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )

	print( i, min(y_data[i]), max(y_data[i]) ) # Gives real-time feel for what ylim should be.
	
	#--- Format star age as a x 10^b, create title and save graph ---
	log_star_age = np.log10( star_age[i] )
	if log_star_age < 1:
		a, b = [ 10 ** (log_star_age - int(log_star_age) + 1 ), int(log_star_age) - 1 ]
	else:
		a, b = [ 10 ** ( log_star_age - int(log_star_age) ), int(log_star_age) ]
	ax.set_title( r"Profile $%s$, Model $%s$, Star age $%.1f\times10^{%s}$ yr" %( profile_number[i], model_number[i], a, b ) )

	fig.tight_layout()
	plt.savefig( output_frames_folder + "/" + filename_final + str(i+1) )

Create_GIF.gif( output_frames_folder, filename_final, output_folder, filename_final[:-1], len(star_age), frame_duration )
