import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import Create_GIF

#----- Define variables -----
input_dir = "aaa_Data/20210813_extra/LOGS_11"

interval = 200 # Time between gif frames (in ms)
n_frames = 20 # Number of gif frames
frame_duration = 400 # milliseconds


#----- Preferences -----
do_TRD = False				# Disable TRD plotting, e.g. if didn't include profiles in MESA codes for speed.
use_different_output_dir = False		# Save files in a different folder.
output_dir = "aaa_Data/20210727_constLi/20210730_ALi_investigation"
show_endpoint = False			# Highlight the final point in the evolution.
set_title = True 			# Give the graphs a title.
title = input_dir[-9:].replace("_"," ")#r"Test"
highlight_point = True			# Highlight a specific point on the HRD.
highlight_modelnumber = 320		# Specify which model to highlight.
append_filename_text = ""#"_MSTOmarked" #  "-"+input_dir[-9:]#""		# Option to append to filename. Useful for multiple graphs. Leave blank if not wanted.


#--- Definitions ---
if use_different_output_dir:
	filename_HRD = output_dir + "/HRD" + append_filename_text
	filename_TRD = output_dir + "/TRD" + append_filename_text
	folder_frames = output_dir + "/HRD frames"
	filenames_frames = output_dir + "HRD-frames"
else:
	filename_HRD = input_dir + "/HRD" + append_filename_text
	filename_TRD = input_dir + "/TRD" + append_filename_text
	folder_frames = input_dir + "/HRD frames"
	filenames_frames = input_dir + "HRD-frames"
log_Teff = []
log_L = []
star_age = []
model_number = []
log_Tc = []
log_Rhoc = []
cols = []
frame_list = []

	
#--- Make sure specified paths exist; create them if not ---
if not os.path.exists( folder_frames ):
	os.mkdir( folder_frames )
	
	
#----- Read csv and extract values -----
data = list(csv.reader(open( input_dir + "/history.csv", "r" )))
headers = data[0]
		
#--- Check T and L are included -----
for par in [ "log_Teff", "log_L", "star_age", "model_number", "log_center_T", "log_center_Rho" ]:
	if not par in headers:
		raise ValueError( f"{par} not in history.csv." )
	else:
		cols.append( headers.index( par ) )
		
#--- Populate T and L lists ---
for row in data[1:]:
	log_Teff.append( float( row[ cols[0] ] ) )
	log_L.append( float( row[ cols[1] ] ) )
	star_age.append( float( row[ cols[2] ] ) )
	model_number.append( int(float( row[ cols[3] ] )) )
	log_Tc.append( float( row[ cols[4] ] ) )
	log_Rhoc.append( float( row[ cols[5] ] ) )
	
	
#----- Plot HRD -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig = plt.figure( figsize=(5,5) )
ax = fig.add_subplot( 111 )
ax.invert_xaxis()
ax.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax.set_ylabel( r"$\log(L/L_\odot)$" )
ax.plot( log_Teff, log_L, color="k" )

if show_endpoint:
	plt.scatter( log_Teff[-1], log_L[-1], s=20, color="b" )
if highlight_point:
	highlight_i = model_number.index( highlight_modelnumber )
	plt.scatter( log_Teff[highlight_i], log_L[highlight_i], s=20, color="b" )
if set_title:
	ax.set_title( title )

fig.tight_layout()
plt.savefig( filename_HRD )
plt.close()
'''
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


#----- Plot T-Rho diagram -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })

fig3 = plt.figure( figsize=(5,5) )
ax3 = fig3.add_subplot( 111 )
ax3.set_xlabel( r"$\log(\rho_{\rm{c}})$" )
ax3.set_ylabel( r"$\log(T_{\rm{c}})$" )
ax3.plot( log_Rhoc, log_Tc, color="b" )

if show_endpoint:
	plt.scatter( log_Rhoc[-1], log_Tc[-1], s=20, color="b" )
if highlight_point:
	True # to be filled out.
if set_title:
	ax3.set_title( title )

fig3.tight_layout()
plt.savefig( filename_TRD )
plt.close()


for param, ylabel, lst in zip( ["Temperature","Density"], [r"$\log(T_{\rm{c}})$",r"$\log(\rho_{\rm{c}})$"], [log_Tc,log_Rhoc] ):
	fig = plt.figure( figsize=(5,5) )
	ax = fig.add_subplot( 111 )
	ax.set_xlabel( r"$\log(t\rm{ (yr)})$" )
	ax.set_ylabel( ylabel )
	ax.semilogx( star_age, lst )
	fig.tight_layout()
	plt.savefig( folder_main + "/TRD-with-" + param + "-vs-Time" )
	plt.close()
'''
