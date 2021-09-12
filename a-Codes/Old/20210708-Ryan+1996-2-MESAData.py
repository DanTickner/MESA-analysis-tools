import csv
import matplotlib.pyplot as plt

#----- Define variables and matplotlib setup -----
FeH = []
ALi = []
logTeff = []
header_strings = [ "[Fe/H]", "log_Teff", "[Li]" ]
header_cols = []
plt.rcParams.update({ "font.size": 14 })
plt.rc( "text", usetex=True )

add_title = True


#----- Read data -----
with open( "Data_MESA_MSTO.csv", "r" ) as csv_file:
	contents = list(csv.reader( csv_file ))
	headers = contents[0]
	
	for header in header_strings:
		header_cols.append( headers.index( header ) )

	for row in contents[1:]:
		FeH.append(float( row[header_cols[0]] ))
		logTeff.append(float( row[header_cols[1]] ))
		ALi.append(float( row[header_cols[2]] ))


#----- Plot [Fe/H] vs Teff -----
fig1 = plt.figure( figsize=(6,4))
ax1 = fig1.add_subplot( 111 )
ax1.scatter( logTeff, FeH, s=1 )
ax1.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax1.set_ylabel( r"$[\rm{Fe}/\rm{H}]$" )
if add_title:
	ax1.set_title( "MESA data" )
#ax1.set_xlim( 3.82, 3.74 )
#ax1.set_ylim( -3.6, -1.1 )
fig1.tight_layout()
plt.savefig( "Ryan+1996-2a-MESA-[FeH]" )


#----- Plot A(Li) vs Teff -----
fig2 = plt.figure( figsize=(6,4))
ax2 = fig2.add_subplot( 111 )
ax2.scatter( logTeff, ALi, s=1 )
ax2.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax2.set_ylabel( r"$A(\rm{Li})$" )
if add_title:
	ax2.set_title( "MESA data" )
#ax2.set_xlim( 3.82, 3.74 )
#ax2.set_ylim( 1.82, 2.42 )
fig2.tight_layout()
plt.savefig( "Ryan+1996-2b-MESA-[Li]" )
