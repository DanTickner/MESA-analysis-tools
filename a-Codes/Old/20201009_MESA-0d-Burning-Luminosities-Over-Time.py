import os
import csv
import matplotlib.pyplot as plt

#----- Define variables -----
model_name = "TS-1p5M-Diffusion"


#----- Preferences -----
extend_filename = True
specify_ylim_logL = True
specify_xlim = True

filename_ext = "zoomed"
ylim_logL = [ -10, 10 ]
xlim = [ 1e7, 2e10 ]


#----- Don't change (constants, or to be populated by the code) -----
csv_folder = "Models/" + model_name + "/CSV"
output_folder = "Models/" + model_name
output_filename = "Energy-Generation-Coefficients-" + model_name + ( filename_ext if extend_filename else "" )

star_age = []
pp = []
cno = []
tri_alfa = []
cols = []
ims = []
pp_norm = []
cno_norm = []
tri_alfa_norm = []


#----- Make sure specified paths exist; create them if not -----
if not os.path.exists( output_folder ):
		os.mkdir( output_folder )


#----- Read history.csv and extract values -----
with open( csv_folder + "/history.csv" ) as data_file:
	data = csv.reader( data_file )
	headers = next( data )
	
	#--- Check T and L are included -----
	for par in [ "star_age", "pp", "cno", "tri_alfa" ]:
		if not par in headers:
			raise ValueError( "%s not in history.csv." %par )
		else:
			cols.append( headers.index( par ) )
	
	#--- Populate age and luminosity lists ---
	for row in data:
		row_pp, row_cno, row_tri_alfa = [ float( row[ cols[i] ] ) for i in range( 1, 4 ) ]
		star_age.append( float( row[ cols[0] ] ) )
		pp.append( row_pp )
		cno.append( row_cno )
		tri_alfa.append( row_tri_alfa )
		
		#--- Normalised contributions as function of time ---
		# i.e. L_pp + L_cno + L_3alpha = 1 for all time
		L_tot = 10**row_pp + 10**row_cno + 10**row_tri_alfa# Total luminosity in solar units
		pp_norm.append( 10**row_pp / L_tot )
		cno_norm.append( 10**row_cno / L_tot )
		tri_alfa_norm.append( 10**row_tri_alfa / L_tot )
		
		
#----- Plot graph -----
plt.rc( "text", usetex=True )
plt.rcParams.update({ "font.size":14 })
fig, ax = plt.subplots( 2, 1, sharex=True, figsize=(7,7) )
ax[1].set_xlabel( "Star age (yr)" )
ax[0].set_ylabel( r"$\log(L/L_\odot)$" )
ax[1].set_ylabel( r"$L/L_{\rm{tot}}$" )


#--- Luminosities in solar units ---
# label=r"$L_{\rm{PP}}/L_{\odot}$"
ax[0].semilogx( star_age, pp, color="k", ls="-", zorder=3, label="PP" )
ax[0].semilogx( star_age, cno, color="0.5", ls="--", zorder=2, label="CNO" )
ax[0].semilogx( star_age, tri_alfa, color="0.7", ls=":", zorder=1, label=r"$3\alpha$" )

#--- Normalised contributions ---
ax[1].semilogx( star_age, pp_norm, color="k", ls="-", zorder=3 )
ax[1].semilogx( star_age, cno_norm, color="0.5", ls="--", zorder=2 )
ax[1].semilogx( star_age, tri_alfa_norm, color="0.7", ls=":", zorder=1 )

#--- Format and save figure ---
ax[0].legend( loc="best" )
if specify_ylim_logL:
	ax[0].set_ylim( ylim_logL[0], ylim_logL[1] )
if specify_xlim:
	ax[0].set_xlim( xlim[0], xlim[1] )# Set after calling semilogy, otherwise causes NaN error

fig.tight_layout()
plt.savefig( output_folder + "/" + output_filename )