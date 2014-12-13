#ryan ulsberger
#final project

# Creates of Updates a shapefile from the Marine Debris Tracker Application from the University of Georgia
# see (http://www.marinedebris.engr.uga.edu/). Create a user account, and download the most recent csv with all of the
# data. Use that csv as an input for this program. If the marine debris shapefile has not been created, the script will
# create a new shapefile from the csv; if the file has been created, it will update the shapefile with any of the
# entries which have not been added to the shapefile yet.

# Also the program can also create an index of the marine debris which is characterized from the Enivronmental
# Sensetivity Index, and the categorization is based on <this documentation>.

import arcpy
import os
import csv
import datetime
from os import path
from arcpy import env
from datetime import *


env.workspace = "C:/MS_GST/TGIS_501/TGIS_501_final/"
env.overwriteOutput = True
newworkspace = "C:/MS_GST/TGIS_501/TGIS_501_final/Marine_Debris.gdb"
shoreline = "C:/MS_GST/TGIS_501/TGIS_501_final/National.gdb/ESI_Shoreline/nationalshoreline"
marinedebris = "C:/MS_GST/TGIS_501/TGIS_501_final/Marine_Debris.gdb/marinedebris"
esi_marinedebris = "C:/MS_GST/TGIS_501/TGIS_501_final/Marine_Debris.gdb/Sensetivity_marinedebris"

tmp_layer = arcpy.mapping.Layer("C:/MS_GST/TGIS_501/TGIS_501_final/traps_md.lyr")
arcpy.management.MakeFeatureLayer(marinedebris,"traps_md.lyr")
arcpy.management.SelectLayerByAttribute(traps_md, "NEW_SELECTION", """ "Item_Cat" = 'Fishing lures and lines' """)
arcpy.management.SelectLayerByAttribute(traps_md, "ADD_TO_SELECTION", """ "Item_Cat" = 'Plastic rope / Small Net Pieces' """)
arcpy.management.SelectLayerByAttribute(traps_md, "ADD_TO_SELECTION", """ "Item_Cat" = 'Rope or Net Pieces (non-nylon)' """)
arcpy.management.SelectLayerByAttribute(traps_md, "ADD_TO_SELECTION", """ "Item_Cat" = 'Crab/Lobster/Fish trap parts' """)
arcpy.management.SelectLayerByAttribute(traps_md, "ADD_TO_SELECTION", """ "Item_Cat" = 'Fishing nets' """)
arcpy.management.SelectLayerByAttribute(traps_md, "ADD_TO_SELECTION", """ "Item_Cat" = 'Crab Trap in Need of Removal' """)
arcpy.management.SelectLayerByAttribute(traps_md, "ADD_TO_SELECTION", """ "Item_Cat" = 'Plastic rope / Small Net Pieces' """)
arcpy.conversion.FeatureClassToFeatureClass(traps_md, "C:/MS_GST/TGIS_501/TGIS_501_final/Marine_Debris.gdb","traps_md")
arcpy.analysis.SpatialJoin(marinedebris_net, shoreline, esi_marinedebris)
