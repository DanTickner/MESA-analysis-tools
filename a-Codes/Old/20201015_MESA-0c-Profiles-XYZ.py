import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import Create_GIF

#----- Define variables -----
model_name = "z_stopshort_RD"

csv_folder = "Models/" + model_name + "/CSV"
frames_folder = "Models/" + model_name + "/XYZ Profile Frames"
frames_filenames = "XYZ-profile-" + model_name + "-"
gif_filename = "XYZ-Profile-" + model_name
gif_folder = "Models/" + model_name
interval = 200# Time between gif frames (in ms)
n_frames = 20# Number of gif frames
frame_duration = 400# milliseconds


#----- Don't change (constants, or to be populated by the code) -----
mass = []
x_mf = []
y_mf = []
z_mf = []
star_age = []
model_number = []
cols = []
last_profile_number = 0# Keep track of previous row in csv, to start new list when profile_number changes


#----- Make sure specified paths exist; create them if not -----
for pth in [ frames_folder, gif_folder ]:
	if not os.path.exists( pth ):
		os.mkdir( pth )


#----- Read csv and extract values -----
with open( csv_folder + "/profiles-data.csv" ) as data_file:
	data = csv.reader( data_file )
	headers = next( data )
	
	#--- Check mass, x,y,z included -----
	for par in [ "profile_number", "mass", "x_mass_fraction_H", "y_mass_fraction_He", "z_mass_fraction_metals" ]:
		if not par in headers:
			raise ValueError( "%s not in profiles-data.csv." %par )
		else:
			cols.append( headers.index( par ) )
	
	#--- Populate T and L lists ---
	for row in data:
		
		#--- Check if we are looking at a new profile ---
		profile_number = int(float( row[ cols[0] ] ))
		
		# Failsafe if profile_number doesn't start from zero (i.e. run is loaded and history.data overwritten)
		while len(mass) < profile_number - 1:
			[ lst.append( [] ) for lst in [ mass, x_mf, y_mf, z_mf, star_age ] ]
			
		if profile_number > last_profile_number:
			[ lst.append( [] ) for lst in [ mass, x_mf, y_mf, z_mf ] ]
		
		mass[ profile_number - 1 ].append( float( row[ cols[1] ] ) )
		x_mf[ profile_number - 1 ].append( float( row[ cols[2] ] ) )
		y_mf[ profile_number - 1 ].append( float( row[ cols[3] ] ) )
		z_mf[ profile_number - 1 ].append( float( row[ cols[4] ] ) )
		last_profile_number = profile_number



#----- Obtain star_age as a function of profile_number -----
[ star_age.append( 0 ) for i in range( len( mass ) ) ]
[ model_number.append( 0 ) for i in range( len( mass ) ) ]

with open( csv_folder + "/profiles.csv" ) as profile_file:
	data = csv.reader( profile_file )
	headers = next( data )
	pn_header = headers.index( "profile_number" )
	age_header = headers.index( "star_age" )
	mn_header = headers.index( "model_number" )
	
	for row in data:
		row_profile_number = int(float( row[pn_header] ))
		star_age[ row_profile_number - 1 ] = float( row[ age_header ] )
		model_number[ row_profile_number - 1 ] = int(float( row[ mn_header ] ))



#----- Plot graph of x,y,z as function of mass coordinate for each profile -----
fig = plt.figure( figsize=(7,5) )
ax = fig.add_subplot( 111 )
#ax.invert_xaxis() Not sure if I want to invert yet. Coordinate goes from 0 (core) to 15 (surface)

for pn in range( len(mass) ):
	if mass[ pn ] == []:
		continue
	
	#--- clear() also clears limits and labels ---
	ax.clear()
	ax.set_xlabel( r"$M_r/M_\odot$" )
	ax.set_ylabel( "Mass fraction" )
	#ax.set_xlim( 0, max(mass[-1]) )# mass[0] may be an empty list if continued from a saved model, so use mass[-1] BUT this causes issues if there's mass loss, so just assume mass[0] is fine for now. Otherwise will need to search through first elements of lists.
	ax.set_xlim( 0, max(mass[0]) )
	ax.set_ylim( -0.05, 1.05 )
	
	#--- Plot X,Y,Z profiles ---
	ax.plot( mass[pn], x_mf[pn], color="k", ls="-", zorder=3, label=r"$X$" )
	ax.plot( mass[pn], y_mf[pn], color="0.4", ls="--", zorder=2, label=r"$Y$" )
	ax.plot( mass[pn], z_mf[pn], color="0.7", ls=":", zorder=1, label=r"$Z$" )
	
	#--- Format star age as a x 10^b and write on top of graph ---
	log_age = np.log10( star_age[pn] )
	if log_age < 1:
		a, b = [ 10 ** (log_age - int(log_age) + 1 ), int(log_age) - 1 ]
	else:
		a, b = [ 10 ** ( log_age - int(log_age) ), int(log_age) ]
	if a == 10:
		a = 1
		b += 1 if b<0 else -1
	the_text = r"Profile $%s$, Model $%s$, Star age %.1f$\times10^{%s}$ yr" %( pn, model_number[pn], a, b )
	ax.text( 0.5, 1.01, the_text, transform=ax.transAxes, horizontalalignment="center" )
	
	#--- Put legend outside the plot and save ---
	box = ax.get_position()
	ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
	ax.legend( bbox_to_anchor=(1.0,1.0) )
	plt.savefig( frames_folder + "/" + frames_filenames + str(pn+1), bbox_inches="tight" )
	ax.set_position( [box.x0, box.y0, box.width, box.height] )# Reset or will continue to shrink for all frames

Create_GIF.gif( frames_folder, frames_filenames, gif_folder, gif_filename, len(mass), 400 )
