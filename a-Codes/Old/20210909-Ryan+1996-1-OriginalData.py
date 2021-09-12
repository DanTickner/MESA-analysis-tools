import numpy as np
import matplotlib.pyplot as plt
import csv


#----- Define variables and matplotlib setup -----
FeH = []
Teff = []
sigma_Teff = []
ALi = []
sigma_ALi = []
logTeff = []
sigma_logTeff = []
plt.rcParams.update({ "font.size": 14 })
plt.rc( "text", usetex=True )

add_title = True


#----- Read data -----
contents = [ j.strip().split() for j in open( "Templates_and_data/Data-Ryan+1996-original.txt", "r" ).readlines() ]
headers = contents[1]
for row in contents[2:]:
	Teff_i = float( row[1] )
	sigma_Teff_i = float( row[2] )
	
	FeH.append(float( row[0] ))
	Teff.append( Teff_i)
	sigma_Teff.append( sigma_Teff_i )
	ALi.append(float( row[3] ))
	sigma_ALi.append(float( row[4] ))
	logTeff.append( np.log10( Teff_i ) )
	sigma_logTeff.append( sigma_Teff_i / ( Teff_i * np.log(10) ) )


#----- Save data with calculated logs and errors -----
ow = csv.writer(open( "Templates_and_data/Data-Ryan+1996-final.csv", "w", newline="" ))
ow.writerow( " ".join(contents[0]) ) # First line with name of paper from which data is taken.
ow.writerow( contents[1] + [ "log(Teff)", "elog(Teff)" ] )
for i in range(len( Teff )):
	ow.writerow( [ FeH[i], Teff[i], sigma_Teff[i], ALi[i], sigma_ALi[i], logTeff[i], sigma_logTeff[i] ] )


#----- Plot [Fe/H] vs Teff -----
fig1 = plt.figure( figsize=(6,4))
ax1 = fig1.add_subplot( 111 )
ax1.scatter( logTeff, FeH, s=1 )
ax1.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax1.set_ylabel( r"$[\rm{Fe}/\rm{H}]$" )
if add_title:
	ax1.set_title( "Ryan et al." )
ax1.set_xlim( 3.82, 3.74 )
ax1.set_ylim( -3.6, -1.1 )
fig1.tight_layout()
plt.savefig( "Templates_and_data/Ryan+1996-1a-Ryan-[FeH]" )


#----- Plot A(Li) vs Teff -----
fig2 = plt.figure( figsize=(6,4))
ax2 = fig2.add_subplot( 111 )
ax2.errorbar( logTeff, ALi, yerr=sigma_ALi, xerr=sigma_logTeff, ls="None", elinewidth=1 )
ax2.set_xlabel( r"$\log(T_{\rm{eff}})$" )
ax2.set_ylabel( r"$A(\rm{Li})$" )
if add_title:
	ax2.set_title( "Ryan et al." )
ax2.set_xlim( 3.82, 3.74 )
ax2.set_ylim( 1.82, 2.42 )
fig2.tight_layout()
plt.savefig( "Templates_and_data/Ryan+1996-1b-Ryan-[Li]" )
