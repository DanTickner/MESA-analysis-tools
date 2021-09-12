import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import Create_GIF

#----- Define variables -----
model_name = "B"

interval = 200 # Time between gif frames (in ms)
n_frames = 20 # Number of gif frames
frame_duration = 400 # milliseconds


#----- Preferences -----
show_endpoint = True
set_title = False
title = r"Salaris ex-student example inlist (mass, z, termination condition modified)"


#----- Don't change (constants, or to be populated by the code) -----
folder_main = "Models/" + model_name
folder_csv = folder_main + "/CSV"
folder_frames = folder_main + "/HRD frames"
figs_folder = "Figs/" + model_name
filenames_frames = "HRD-" + model_name + "-"
log_Teff = []
log_L = []
star_age = []
cols = []
frame_list = []
images = []
model_number = []


#----- Make sure specified paths exist; create them if not -----
if not os.path.exists( folder_frames ):
	os.mkdir( folder_frames )


#----- Read csv and extract values -----
with open( folder_csv + "/history.csv" ) as data_file:
	data = csv.reader( data_file )
	headers = next( data )
	
	#--- Check T and L are included -----
	for par in [ "log_Teff", "log_L", "star_age", "model_number" ]:
		if not par in headers:
			#This will never be raised. Only there for rigour!
			raise ValueError( "%s not in history.csv." %par )
		else:
			cols.append( headers.index( par ) )
	
	#--- Populate T and L lists ---
	for row in data:
		log_Teff.append( float( row[ cols[0] ] ) )
		log_L.append( float( row[ cols[1] ] ) )
		star_age.append( float( row[ cols[2] ] ) )
		model_number.append( int(float( row[ cols[3] ] )) )


#----- Plot HRD -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig = plt.figure( figsize=(5,5) )
ax = fig.add_subplot( 111 )
ax.invert_xaxis()
ax.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax.set_ylabel( r"$\log(L/L_\odot)$" )

ax.plot( log_Teff, log_L, color="b" )

if show_endpoint:
	plt.scatter( log_Teff[-1], log_L[-1], s=20, color="b" )
if set_title:
	ax.set_title( title )

fig.tight_layout()
plt.savefig( folder_main + "/HRD-" + model_name )
plt.close()

for param, ylabel, lst in zip( ["Temperature","Luminosity"], [r"$\log(T_{\rm{eff}})$",r"$\log(L/L_\odot)$"], [log_Teff,log_L] ):
	fig = plt.figure( figsize=(5,5) )
	ax = fig.add_subplot( 111 )
	ax.set_xlabel( r"$\log(t\rm{ (yr)})$" )
	ax.set_ylabel( ylabel )
	ax.semilogx( star_age, lst )
	fig.tight_layout()
	plt.savefig( folder_main + "/HRD-with-" + param + "-vs-Time" )
	plt.close()
	

#----- Save HRD images at discrete timesteps for later conversion into GIF -----
log_age_spacing = ( max(star_age) - min(star_age) ) / n_frames
frame_spacing = len( log_Teff ) / n_frames
				  
frame_list = [ int( i * frame_spacing ) for i in range(n_frames-1) ] + [ len(log_Teff)-1 ]
frame_list[0] = 1

fig2 = plt.figure( figsize=(5,5) )
ax2 = fig2.add_subplot( 111 )
ax2.invert_xaxis()

for i, frame in enumerate( frame_list ):
	ax2.clear()
	ax2.set_xlabel( "$\log(T_{\\rm{eff}})$" )# clear() also clears limits and labels
	ax2.set_ylabel( "$\log(L/L_\\odot)$" )
	ax2.set_xlim( max(log_Teff), min(log_Teff) )
	ax2.set_ylim( min(log_L), max(log_L) )

	#--- Format star age as a x 10^b and write on top of graph ---
	log_age = np.log10( star_age[frame] )
	if log_age < 1:
		a, b = [ 10 ** (log_age - int(log_age) + 1 ), int(log_age) - 1 ]
	else:
		a, b = [ 10 ** ( log_age - int(log_age) ), int(log_age) ]
	the_text = r"Profile $%s$, Model $%s$, Star age $%.1f\times10^{%s}$ yr" %( i+1, model_number[frame], a, b )
	ax2.text( 0.5, 1.01, the_text, transform=ax2.transAxes, horizontalalignment="center" )
	fig2.tight_layout()# Layout is preserved even if this is outside the loop, but may still overlap boundaries
	
	ax2.plot( log_Teff[:frame], log_L[:frame] )
	plt.savefig( folder_frames + "/" + filenames_frames + str(i+1) )

plt.close()

#----- Loop saved images together into GIF -----
Create_GIF.gif( folder_frames, filenames_frames, folder_main, "HRD-"+model_name, n_frames, frame_duration )
