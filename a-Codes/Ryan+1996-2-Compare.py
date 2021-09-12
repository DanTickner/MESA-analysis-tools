import csv
import matplotlib.pyplot as plt
import os

#----- Define variables and matplotlib setup -----
Ryan_FeH = []
Ryan_ALi = []
Ryan_sigma_ALi = []
Ryan_logTeff = []
Ryan_sigma_logTeff = []
Ryan_header_strings = [ "#Fe/H", "log(Teff)", "elog(Teff)", "A(Li)", "eA(Li)" ]
Ryan_header_cols = []
MESA_FeH = []
MESA_ALi = []
MESA_logTeff = []
MESA_header_strings = [ "[Fe/H]_surf", "log_Teff", "A(Li)" ]
MESA_header_cols = []
plt.rcParams.update({ "font.size": 14 })
plt.rc( "text", usetex=True )

MESA_filename = "aaa_Data/20210819_1/allmodels_age.csv"
output_dir = "aaa_Data/Image_Backup/20210819_1"
add_title = False
add_legend = False
title =  "" # "Combined" "Z=1d-4"
extend_filename = ""#"-Z=1d-2" # Leave as empty string "" if unwanted.


#----- Read Ryan+1996 csv -----
Ryan_contents = list(csv.reader(open( "Templates_and_data/Data-Ryan+1996-final.csv", "r" )))
Ryan_headers = Ryan_contents[1]

[ Ryan_header_cols.append( Ryan_headers.index( header ) ) for header in Ryan_header_strings ]

for row in Ryan_contents[2:]:
	Ryan_FeH.append(float(           row[Ryan_header_cols[0]] ))
	Ryan_logTeff.append(float(       row[Ryan_header_cols[1]] ))
	Ryan_sigma_logTeff.append(float( row[Ryan_header_cols[2]] ))
	Ryan_ALi.append(float(           row[Ryan_header_cols[3]] ))
	Ryan_sigma_ALi.append(float(     row[Ryan_header_cols[4]] ))


#----- Read MESA csv -----
MESA_contents = list(csv.reader(open( MESA_filename, "r" )))
MESA_headers = MESA_contents[0]

[ MESA_header_cols.append( MESA_headers.index( header ) ) for header in MESA_header_strings ]

for row in MESA_contents[1:]:
	if True: # row[1][:6] == "LOGS_R": # To plot all data (no filter wanted), replace this line by if True:
		MESA_FeH.append(float(     row[MESA_header_cols[0]] ))
		MESA_logTeff.append(float( row[MESA_header_cols[1]] ))
		MESA_ALi.append(float(     row[MESA_header_cols[2]] ))


#----- Plot [Fe/H] vs Teff -----
fig1 = plt.figure( figsize=(6,4))
ax1 = fig1.add_subplot( 111 )
ax1.scatter( Ryan_logTeff, Ryan_FeH, s=3, color="orange", label="Ryan et al." )
ax1.scatter( MESA_logTeff, MESA_FeH, s=3, color="blue", label="MESA data" )
plt.gca().invert_xaxis()
ax1.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax1.set_ylabel( r"$[\rm{Fe}/\rm{H}]$" )
if add_title:
	ax1.set_title( title )
#ax1.set_xlim( 3.82, 3.74 )
#ax1.set_ylim( -3.6, -1.1 )
if add_legend:
	box1 = ax1.get_position()
	ax1.set_position( [box1.x0, box1.y0, box1.width*0.8, box1.height] )
	ax1.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( os.path.join( output_dir, "Ryan+1996-Compare-[FeH]" + extend_filename ), bbox_inches="tight" )


#----- Plot A(Li) vs Teff -----
fig2 = plt.figure( figsize=(6,4))
ax2 = fig2.add_subplot( 111 )
ax2.errorbar( Ryan_logTeff, Ryan_ALi, yerr=Ryan_sigma_ALi, xerr=Ryan_sigma_logTeff, ls="None", elinewidth=1, color="orange", zorder=0, label="Ryan et al." )
ax2.scatter( MESA_logTeff, MESA_ALi, s=3, color="blue", zorder=1, label="MESA data" )
plt.gca().invert_xaxis()
ax2.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax2.set_ylabel( r"$A(\rm{Li})$" )
if add_title:
	ax2.set_title( title )
#ax2.set_xlim( 3.82, 3.74 )
#ax2.set_ylim( 1, 2.6 )
if add_legend:
	box2 = ax2.get_position()
	ax2.set_position( [box2.x0, box2.y0, box2.width*0.8, box2.height] )
	ax2.legend( bbox_to_anchor=(1.0,1.0) )
plt.savefig( os.path.join( output_dir, "Ryan+1996-Compare-[Li]" + extend_filename ), bbox_inches="tight" )
