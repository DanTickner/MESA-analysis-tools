import csv
import numpy as np

#----- Define variables -----
model_name = "Overshoot-False"

#----- Preferences -----


#----- Don't change -----
folder_csv = "Models/" + model_name + "/CSV"


#----- Open csv file -----
with open( folder_csv + "/history.csv", "r" ) as data_file:
	data = csv.reader( data_file )
	headers = next( data )