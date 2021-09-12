import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import Create_GIF


#----- Define variables -----
model_name = "R_2agb"
y_columns = [ "am_log_D_DSI", "am_log_D_SH", "am_log_D_SSI", "am_log_D_ES", "am_log_D_GSF", "am_log_D_ST" ]
x_column = "logT"# mass, zone, q, logT...


#----- Preferences -----
invert_xaxis = True
set_xlabel = False
set_ylabel = True
set_xlim = False
set_ylim = True # Overridden and always true. You must set sensible ylims manually!
set_legends = [ True ]

graph_type = "normal"
frame_duration = 400
line_colours = [ "k", "b", "orange", "red", "green", "yellow", "grey" ]
line_styles = [ "-", "--", ":", "-.", "-", "--", ":" ]


filename_addon = "-Rot-Diffusion-Coeffs-vs-logT"
xlabel = ""
ylabel = "am\_log\_D\_x"
xlim = [ 0, 1]
ylim = [ -50, 50 ] # Set these!
legends = [ "DSI", "SH", "SSI", "ES", "GSF", "ST" ]


#----- Don't change (constants, or to be populated by the code) -----
filename_final = model_name + "-" + filename_addon
csv_folder = "Models/" + model_name + "/CSV"
output_folder = "Models/" + model_name
output_frames_folder = output_folder + "/" + filename_final + "Frames"
cols = []
model_number = []
star_age = []
y_data = [ [] for y in y_columns ]
x_data = [ [] for y in y_columns ]
last_pn = 0# Keep track of previous row in csv, to start new list when profile number changes
profile_number = []


#----- Ensure enough colours defined. Make sure specified paths exist; create them if not -----
if len( line_colours ) < len( y_columns ):
	raise ValueError( "Not enough colours defined for the graph (%s colours, %s y_columns)." %( len(line_colours), len(y_columns) ) )
if len( line_styles ) < len( y_columns ):
	raise ValueError( "Not enough linestyles defined for the graph (%s colours, %s y_columns)." %( len(line_styles), len(y_columns) ) )

if not os.path.exists( output_frames_folder ):
	os.mkdir( output_frames_folder )


#----- Read profiles-data.csv -----
with open( csv_folder + "/profiles-data.csv", "r" ) as file_pd:
	data_pd = csv.reader( file_pd )
	headers_pd = next( data_pd )
	
	#--- Check data included ---
	for par in [ "profile_number", x_column ] + y_columns:
		if not par in headers_pd:
			raise ValueError( "%s not in profiles-data.csv." %par )
		else:
			cols.append( headers_pd.index( par ) )
	
	#--- Populate lists ---
	for row in data_pd:
		
		#--- Are we still looking at the same profile? ---
		this_pn = int(float( row[ cols[0] ] ))
		
		if this_pn > last_pn:
			
			for i in range(len( y_data )):
				y_data[i].append( [] )
				x_data[i].append( [] )
			model_number.append( 0 )# To be updated later
			star_age.append( 0 )# To be updated later
			
			if not this_pn in profile_number:
				profile_number.append( this_pn )
		
		last_pn = this_pn
		
		#--- Add data ---
		for i, y_col in enumerate( y_columns ):
			j = profile_number.index( this_pn )
			x_data[ i ][ j ].append(float( row[ cols[1] ] ))
			y_data[ i ][ j ].append(float( row[ cols[2+i] ] ))


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
xlim_final = xlim if set_xlim else [ min([ min(lst[0]) for lst in x_data ])*0.9, max([ max(lst[0]) for lst in x_data ])*1.1 ]#Lists all same
ylim_final = ylim # Too many layers (3) to automate at this point in time.
xlabel_final = xlabel if set_xlabel else r"%s" %x_column.replace("_","\_")
legends_final = legends if set_legends else [ y.replace("_","\_") for y in y_columns ]

for j in range(len( star_age )):
	
	#--- Keep same figure open but reset it ---
	ax.clear()
	ax.set_xlabel( xlabel_final )
	if set_ylabel:
		ax.set_ylabel( ylabel )
	ax.set_xlim( xlim_final[0], xlim_final[1] )
	ax.set_ylim( ylim_final[0], ylim_final[1] )
	if invert_xaxis:
		plt.gca().invert_xaxis()

	#--- Plot gaph of the chosen type ---
	for i in range(len( y_data )):
		if graph_type == "normal":
			ax.plot( x_data[i][j], y_data[i][j], color=line_colours[i], ls=line_styles[i], label=legends_final[i] )
		elif graph_type == "semilogx":
			ax.semilogx( x_data[i][j], y_data[i][j], color=line_colours[i], ls=line_styles[i], label=legends_final[i] )
		elif graph_type == "semilogy":
			ax.semilogy( x_data[i][j], y_data[i][j], color=line_colours[i], ls=line_styles[i], label=legends_final[i] )
		elif graph_type == "loglog":
			ax.loglog( x_data[i][j], y_data[i][j], color=line_colours[i], ls=line_styles[i], label=legends_final[i] )
		else:
			raise ValueError( "graph_type '%s' not understood. Only 'normal', 'semilogx', 'semilogy', 'loglog' are accepted." %graph_type )
	
	#--- Format star age as a x 10^b, create title and save graph ---
	log_star_age = np.log10( star_age[j] )
	if log_star_age < 1:
		a, b = [ 10 ** (log_star_age - int(log_star_age) + 1 ), int(log_star_age) - 1 ]
	else:
		a, b = [ 10 ** ( log_star_age - int(log_star_age) ), int(log_star_age) ]
	ax.set_title( r"Model $%s$, Profile $%s$, Star age = $%.1f\times10^{%s}$ yr" %( model_number[j], profile_number[j], a, b ) )

	#--- Put legend outside the plot and save figure ---
	box = ax.get_position()
	old_width = box.width
	ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
	ax.legend( bbox_to_anchor=(1.0,1.0) )
	plt.savefig( output_frames_folder + "/" + filename_final + str(j+1), bbox_inches="tight" )
	ax.set_position( [box.x0, box.y0, old_width, box.height] ) # Must undo set_position or it compounds each time!+1) )

Create_GIF.gif( output_frames_folder, filename_final, output_folder, filename_final[:-1], len(star_age), frame_duration )
