import csv
import matplotlib.pyplot as plt

#----- Define variables -----
parent_dir = "aaa_Data" # Where B,D,R,RD folders saved. Leave as empty string to look in current directory.
model_letters = [ "20210809_B/LOGS_17", "20210809_D_incH/LOGS_17", "20210809_R/LOGS_17", "20210809_RD_incH/LOGS_17" ] #[ "0p" + str(i) for i in range(60,96) ] #[ "B", "D", "R", "RD" ]
folder_output = "Image_Backup/20210910_report/HRD-M=0p76" # Code will automatically add parent_dir to this. Just name the folder.


#----- Preferences -----
interval = 200 # Time between gif frames (in ms)
n_frames = 20 # Number of gif frames
frame_duration = 400 # milliseconds

show_endpoint = False
set_title = False
add_to_title = True # not yet implemented
use_custom_labels = True
use_custom_xlim = False
use_custom_ylim = False
append_filename_HRD = False
show_legend = False #Issue with legend on Teff and L graphs. Also for multiple graphs there's little use showing the same legend in all of them. Write it in a figure caption instead or something.

title = r"$M/M_\odot=0.8$, $Z=0.001$"
add_to_title_text = r""
custom_labels = [ "Standard", "Diffusion", "Rotation", "Rot. and diff." ]#[ "M=0." + str(ml)[-2:] for ml in model_letters ] # [ "Standard", "Diffusion", "Rotation", "Rotation and diffusion" ]
line_colours = [ "k", "b", "orange", "red", "green", "grey", "yellow" ]
line_styles = [ "-", "--", ":", "-.", "-", "--", ":" ]
custom_xlim = [ 3.7, 3.68 ]
custom_ylim = [ -0.75, -0.5 ]
append_filenames_text = [ "" for i in range(len(model_letters)) ] # [ "", "", "" , "", "", "", "" ]
append_filename_HRD_text = ""


#----- Don't change (constants, or to be populated by the code) -----
if parent_dir != "":
	folder_output = parent_dir + "/" + folder_output

filename_HRD = "HRD-Comparison"
filename_TRD = "TRD-Comparison"

folders_csv = []
for  i_m, m in enumerate( model_letters ):
	if append_filenames_text[i_m]:
		if parent_dir == "":
			the_folder =  "z_" + append_filenames_text[i_m] + "_" + m
		else:
			the_folder =  parent_dir + "/z_" + append_filenames_text[i_m] + "_" + m
	else:
		if parent_dir == "":
			the_folder = m
		else:
			the_folder = parent_dir + "/" + m
	folders_csv.append( the_folder )

if append_filename_HRD:
	filename_HRD += "-" + append_filename_HRD_text
	filename_TRD += "-" + append_filename_HRD_text
	
log_Teff     = [ [] for m in model_letters ]
log_L        = [ [] for m in model_letters ]
star_age     = [ [] for m in model_letters ]
model_number = [ [] for m in model_letters ] # This is useful but only for a quick visual aid. Clearly cannot be compared between stars.
log_Tc       = [ [] for m in model_letters ]
log_Rhoc     = [ [] for m in model_letters ]
cols         = [ [] for m in model_letters ]
labels = custom_labels if use_custom_labels else [ ml.replace("_","\_") for ml in model_letters ]


#----- Read csv and extract values -----
print( "Reading CSVs:" )
for i in range( len( model_letters ) ):
	print( folders_csv[i] + "/history.csv" )
	with open( folders_csv[i] + "/history.csv" ) as data_file:
		data = csv.reader( data_file )
		headers = next( data )
		
		#--- Check T and L are included -----
		for par in [ "log_Teff", "log_L", "star_age", "model_number", "log_center_T", "log_center_Rho" ]:
			if not par in headers:
				raise ValueError( "%s not in history.csv." %par )
			else:
				cols[i].append( headers.index( par ) )
				
		#--- Populate T and L lists ---
		for row in data:
			log_Teff[i].append(     float( row[ cols[i][0] ] ) )
			log_L[i].append(        float( row[ cols[i][1] ] ) )
			star_age[i].append(     float( row[ cols[i][2] ] ) )
			model_number[i].append( float( row[ cols[i][3] ] ) )
			log_Tc[i].append(       float( row[ cols[i][4] ] ) )
			log_Rhoc[i].append(     float( row[ cols[i][5] ] ) )



#----- Plot HRD -----
print( "\nSaving figures:" )
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })
fig = plt.figure( figsize=(8,5) )
ax = fig.add_subplot( 111 )
ax.invert_xaxis()
ax.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax.set_ylabel( r"$\log(L/L_\odot)$" )

if set_title:
	the_title = title
	if add_to_title:
		the_title += add_to_title_text
	ax.set_title( the_title )
if use_custom_xlim:
	ax.set_xlim( custom_xlim[0], custom_xlim[1] )
if use_custom_ylim:
	ax.set_ylim( custom_ylim[0], custom_ylim[1] )

for i in range(len( model_letters )):
	col = 1 - ( i+1 ) / ( len(model_letters) + 1 )
	ax.plot( log_Teff[i], log_L[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
	#ax.plot( log_Teff[i], log_L[i], color=(col,col,col), ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )

if show_endpoint:
	for i in range(len( model_letters )):
		ax.scatter( log_Teff[i][-1], log_L[i][-1], s=20, color=line_colours[i], zorder=len(model_letters)-i )

# Put legend outside the plot and save figure
box = ax.get_position()
ax.set_position( [box.x0, box.y0, box.width*0.8, box.height] )
ax.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( folder_output + "/" + filename_HRD, bbox_inches="tight" )
plt.close()
print( folder_output + "/" + filename_HRD )


#----- Teff vs time and L vs time -----
for param, ylabel, lst in zip( ["Teff","L"], [r"$\log(T_{\rm{eff}})$",r"$\log(L/L_\odot)$"], [log_Teff,log_L] ):
	fig2 = plt.figure( figsize=(6,6/1.414)  )
	ax2 = fig2.add_subplot( 111 )
	ax2.set_xlabel( r"$\log(t\rm{ (yr)})$" )
	ax2.set_ylabel( ylabel )

	if append_filename_HRD:
		graph_v_time_filename = folder_output + "/" + "HRD-Comparison-" + append_filename_HRD_text + "-" + param + "-vs-Time"
	else:
		graph_v_time_filename = folder_output + "/" + "HRD-Comparison-" + param + "-vs-Time"
	
	if set_title:	
		if add_to_title:
			ax2.set_title( title + add_to_title_text )
		else:
			ax2.set_title( title )
			
	for i in range(len( model_letters )):
		col = 1 - ( i+1 ) / ( len(model_letters) + 1 )
		ax2.semilogx( star_age[i], lst[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
		#ax2.semilogx( star_age[i], lst[i], color=(col,col,col), ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )

	#ax2.set_xlim( min([min(ls) for ls in star_age ]), max([max(ls) for ls in star_age ]) )
	ax2.set_xlim( 1e6, max([max(ls) for ls in star_age ]) )
	ax2.set_ylim( min([min(ls) for ls in lst ]), max([max(ls) for ls in lst ]) )
	
	# Put legend outside the plot and save figure
	if show_legend:
		#box2 = ax2.get_position() # L graph always has legend within plot if use this. Cause unknown.
		#ax2.set_position( [box2.x0, box2.y0, box2.width*0.8, box2.height] )
		ax2.legend( bbox_to_anchor=(1.26,1.0) )
		plt.savefig( graph_v_time_filename, bbox_inches="tight" )
	else:
		fig2.tight_layout()
		plt.savefig( graph_v_time_filename )
	print( graph_v_time_filename )
	plt.close()


#----- Teff vs model_number and L vs model_number -----
for param, ylabel, lst in zip( ["Teff","L"], [r"$\log(T_{\rm{eff}})$",r"$\log(L/L_\odot)$"], [log_Teff,log_L] ):
	fig2b = plt.figure( figsize=(8,5) )
	ax2b = fig2b.add_subplot( 111 )
	ax2b.set_xlabel( r"Model number" )
	ax2b.set_ylabel( ylabel )

	if append_filename_HRD:
		graph_v_modelnumber_filename = folder_output + "/" + "HRD-Comparison-" + append_filename_HRD_text + "-" + param + "-vs-Modelnumber"
	else:
		graph_v_modelnumber_filename = folder_output + "/" + "HRD-Comparison-" + param + "-vs-Modelnumber"
	
	if set_title:	
		if add_to_title:
			ax2b.set_title( title + add_to_title_text )
		else:
			ax2b.set_title( title )
			
	for i in range(len( model_letters )):
		col = 1 - ( i+1 ) / ( len(model_letters) + 1 )
		ax2b.plot( model_number[i], lst[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
		#ax2b.plot( model_number[i], lst[i], color=(col,col,col), ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
	
	# Put legend outside the plot and save figure
	if show_legend:
		#box2 = ax2.get_position() # L graph always has legend within plot if use this. Cause unknown.
		#ax2.set_position( [box2.x0, box2.y0, box2.width*0.8, box2.height] )
		ax2b.legend( bbox_to_anchor=(1.26,1.0) )
		plt.savefig( graph_v_modelnumber_filename, bbox_inches="tight" )
	else:
		fig2b.tight_layout()
		plt.savefig( graph_v_modelnumber_filename )
	print( graph_v_modelnumber_filename )
	plt.close()


#----- Plot TRD (T - Rho diagram) -----
fig3 = plt.figure( figsize=(8,5) )
ax3 = fig3.add_subplot( 111 )
ax3.set_xlabel( r"$\log(\rho_{\rm{c}})$" )
ax3.set_ylabel( r"$\log(T_{\rm{c}})$" )

for i in range(len( model_letters )):
	col = 1 - ( i+1 ) / ( len(model_letters) + 1 )
	ax3.plot( log_Rhoc[i], log_Tc[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
	#ax3.plot( log_Rhoc[i], log_Tc[i], color=(col,col,col), ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )

if show_endpoint:
	for i in range(len( model_letters )):
		ax3.scatter( log_Rhoc[i][-1], log_Tc[i][-1], s=20, color=line_colours[i], zorder=len(model_letters)-i )

box3 = ax3.get_position()
ax3.set_position( [box3.x0, box3.y0, box3.width*0.8, box3.height] )
ax3.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( folder_output + "/" + filename_TRD, bbox_inches="tight" )
plt.close()
print( folder_output + "/" + filename_TRD )


#----- T_c vs time and Rho_c vs time -----
for param, ylabel, lst in zip( ["Tc","Rhoc"], [r"$\log(T_{\rm{c}})$",r"$\log(\rho_{\rm{c}})$"], [log_Tc,log_Rhoc] ):
	fig4 = plt.figure( figsize=(8,5) )
	ax4 = fig4.add_subplot( 111 )
	ax4.set_xlabel( r"$\log(t\rm{ (yr)})$" )
	ax4.set_ylabel( ylabel )

	if append_filename_HRD:
		graph_v_time_filename = folder_output + "/" + "TRD-Comparison-" + append_filename_HRD_text + "-" + param + "-vs-Time"

	else:
		graph_v_time_filename = folder_output + "/" + "TRD-Comparison-" + param + "-vs-Time"
	
	if set_title:	
		if add_to_title:
			ax4.set_title( title + add_to_title_text )
		else:
			ax4.set_title( title )
			
	for i in range(len( model_letters )):
		col = 1 - ( i+1 ) / ( len(model_letters) + 1 )
		ax4.semilogx( star_age[i], lst[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
		#ax4.semilogx( star_age[i], lst[i], color=(col,col,col), ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
	
	# Put legend outside the plot and save figure
	if show_legend:
		#box2 = ax2.get_position() # L graph always has legend within plot if use this. Cause unknown.
		#ax2.set_position( [box2.x0, box2.y0, box2.width*0.8, box2.height] )
		ax4.legend( bbox_to_anchor=(1.26,1.0) )
		plt.savefig( graph_v_time_filename, bbox_inches="tight" )
	else:
		fig4.tight_layout()
		plt.savefig( graph_v_time_filename )
	print( graph_v_time_filename )
	plt.close()


#----- T_c vs model_number and Rho_c vs model_number -----
for param, ylabel, lst in zip( ["Tc","Rhoc"], [r"$\log(T_{\rm{c}})$",r"$\log(\rho_{\rm{c}})$"], [log_Tc,log_Rhoc] ):
	fig4b = plt.figure( figsize=(8,5) )
	ax4b = fig4b.add_subplot( 111 )
	ax4b.set_xlabel( r"Model number" )
	ax4b.set_ylabel( ylabel )

	if append_filename_HRD:
		graph_v_modelnumber_filename = folder_output + "/" + "TRD-Comparison-" + append_filename_HRD_text + "-" + param + "-vs-Modelnumber"

	else:
		graph_v_modelnumber_filename = folder_output + "/" + "TRD-Comparison-" + param + "-vs-Modelnumber"
	
	if set_title:	
		if add_to_title:
			ax4b.set_title( title + add_to_title_text )
		else:
			ax4b.set_title( title )
			
	for i in range(len( model_letters )):
		col = 1 - ( i+1 ) / ( len(model_letters) + 1 )
		ax4b.plot( model_number[i], lst[i], color=line_colours[i], ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
		#ax4b.plot( model_number[i], lst[i], color=(col,col,col), ls=line_styles[i], label=labels[i], zorder=len(model_letters)-i )
	
	# Put legend outside the plot and save figure
	if show_legend:
		#box2 = ax2.get_position() # L graph always has legend within plot if use this. Cause unknown.
		#ax2.set_position( [box2.x0, box2.y0, box2.width*0.8, box2.height] )
		ax4b.legend( bbox_to_anchor=(1.26,1.0) )
		plt.savefig( graph_v_modelnumber_filename, bbox_inches="tight" )
	else:
		fig4b.tight_layout()
		plt.savefig( graph_v_modelnumber_filename )
	print( graph_v_modelnumber_filename )
	plt.close()
