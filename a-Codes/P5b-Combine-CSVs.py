import os
import csv

#----- Define variables -----
parent_dir = "aaa_Data/20210814"
csv_folders = [ "LOGS_0p67B", "LOGS_0p67D", "LOGS_0p69B", "LOGS_0p69D" ]#[ f"20210809_{x}" for x in [ "B", "R", "D", "RD", "D_incH", "RD_incH" ] ]
csv_filename = "history.csv"
output_file = parent_dir + "/20210814.csv"


# Option to read all folders in each parent_dir, saves specifying csv_folders. Ignores files and the "a_Comparisons" folder, but will fail if any parent_dir contains a folder without history.csv.
use_all_folders = True
if use_all_folders:
	csv_folders = sorted([ obj for obj in os.listdir( parent_dir ) if os.path.isdir(os.path.join( parent_dir, obj )) and obj!="a_Comparisons" ])


all_data = []

#----- Read CSVs -----
for i, f in enumerate( csv_folders ):
	print( "Reading file: " + f )
	csv_data = list(csv.reader(open( os.path.join(parent_dir,f,csv_filename), "r" )))

	#--- Header consistency control ---
	if i == 0:
		headers_first = [ "filepath" ] + csv_data[0]
	else:
		headers_this = [ "filepath" ] + csv_data[0]
		for j in range(len( headers_first )):
			if headers_this[j] != headers_first[j]:
				raise ValueError( f"Headers in {f} inconsistent with {files[0]}. Position {j+1} is {headers_this[j]}, should be {headers_first[j]}." )
		# Extra headers can be safely appended without hurting previous data structure.
		if len( headers_this ) > len( headers_first ):
			headers_first += headers_this[ len(headers_first) : ]

	#--- Append the data ---
	[ all_data.append( [ os.path.join(f,csv_filename) ] + row ) for row in csv_data[1:] ]


#----- Save combined CSV file -----
print( "\nSaving file: " + output_file )

csv_writer = csv.writer(open( output_file, "w", newline="" ))
csv_writer.writerow( headers_first )
[ csv_writer.writerow( row ) for row in all_data ]
