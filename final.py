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

print "Version 1.1.2 Beta-Bugy"

inputfile = "C:/MS_GST/TGIS_501/TGIS_501_final/md_2014_1204.csv"
# go back and make so that the files are all saved in the same place
# create folder structure within a certain directory
env.workspace = "C:/MS_GST/TGIS_501/TGIS_501_final"
env.overwriteOutput = True
path = "C:/MS_GST/TGIS_501/TGIS_501_final/"
print path
fcname = 'marinedebris'
spatialref = "WGS 1984"


# Checks to see if process has been ran.

exist = os.path.exists(path + "/Marine_Debris.gdb")
print "Marine Debris Geodatabase Exists:"
print exist
#creates new feature is script has been run
if exist == False:
    #create feature class
    mardeb_gdb = arcpy.management.CreateFileGDB(path, "Marine_Debris.gdb")
    fc = arcpy.management.CreateFeatureclass(mardeb_gdb, fcname, 'POINT', '', 'DISABLED', 'DISABLED', spatialref)
    arcpy.management.AddField( fc, 'Item_Cat', 'TEXT', "15")
    arcpy.management.AddField( fc, 'Item_Name', 'TEXT', "50")
    arcpy.management.AddField( fc, 'Quantity', 'TEXT')
    arcpy.management.AddField( fc, 'Latitude', 'DOUBLE')
    arcpy.management.AddField( fc, 'Longitude', 'DOUBLE')
    arcpy.management.AddField( fc, 'Altitude', 'TEXT')
    arcpy.management.AddField( fc, 'Radius', 'TEXT')
    arcpy.management.AddField( fc, 'DtTm', 'DATE')
    #arcpy.management.AddField( fc, 'Date', 'TEXT')
    #arcpy.management.AddField( fc, 'Time', 'TEXT')
    arcpy.management.AddField( fc, 'Desc', 'TEXT', "250")
    arcpy.management.AddField( fc, 'Location', 'TEXT')
    print "Created new Shapefile with new fields"
    # iterate through csv file and split the fields to then run
    with open(inputfile, 'rb') as csvfile:
        unicode(csvfile)
        reader = csv.reader(csvfile, delimiter = ",")
        #assigns fields in csv to new feature class fields
        for row in reader:
            Item_Cat = row[0]
            Item_Name = row[1]
            Quantity = row[2]
            Longitude = row[3]
            Latitude = row[4]
            Altitude = row[5]
            Radius = row[6]
            DtTm = row[7] + " " + row[8]
            Desc = str(row[9].replace(chr(0xd7), "x")).decode('latin1').encode('utf-8')
            # print Desc
            Location = row[10]
            # makes new search cursor and new points
            cursor = arcpy.da.InsertCursor(fc, ("SHAPE@XY","Item_Cat", "Item_Name", "Quantity", "Latitude", "Longitude", "Altitude", "Radius", "DtTm", "Desc", "Location"))
            point = arcpy.Point(float(Latitude), float(Longitude))
            cursor.insertRow((point, Item_Name, Item_Cat, Quantity, Latitude, Longitude, Altitude, Radius, datetime.strptime(DtTm, "%m/%d/%Y %H:%M:%S"), Desc, Location))
            del cursor
    print "Added all Marine Debris to shapefile"
    print "processed finished"
else:
    print "Marine Debris Feature Class already exists:"
    fc = env.workspace + "/Marine_Debris.gdb/marinedebris"
    search = arcpy.da.SearchCursor(fc, ["DtTm"])
    for day in search:
        #finds most recent day in the shapefile
        newday = max(search)
        print 'Most recent date in Shapefile:'
        newday_shp = newday[0]
        print newday_shp
    # Iterates through csv to find all dates which havent been update
    with open("C:/MS_GST/TGIS_501/TGIS_501_final/md_2014_1204_2.csv", 'rb') as csvfile:
        unicode(csvfile)
        reader = csv.reader(csvfile, delimiter = ",")
        newday_csv = list()
        for row in reader:
            Item_Cat = row[0]
            Item_Name = row[1]
            Quantity = row[2]
            Longitude = row[3]
            Latitude = row[4]
            Altitude = row[5]
            Radius = row[6]
            DtTm = row[7] + " " + row[8]
            Desc = str(row[9].replace(chr(0xd7), "x")).decode('latin1').encode('utf-8')
            Location = row[10]
            # print newday
            # print newday_csv
            #writes new days into existing feature class
            if datetime.strptime(DtTm, '%m/%d/%Y %H:%M:%S') > newday_shp:
                newday_csv.append(datetime.strptime(DtTm, '%m/%d/%Y %H:%M:%S'))
                print "Added Entry for:"
                print datetime.strptime(DtTm, '%m/%d/%Y %H:%M:%S')
                # makes new search cursor and new points
                cursor = arcpy.da.InsertCursor(fc, ("SHAPE@XY","Item_Cat", "Item_Name", "Quantity", "Latitude", "Longitude", "Altitude", "Radius", "DtTm", "Desc", "Location"))
                point = arcpy.Point(float(Latitude), float(Longitude))
                cursor.insertRow((point, Item_Name, Item_Cat, Quantity, Latitude, Longitude, Altitude, Radius, datetime.strptime(DtTm, "%m/%d/%Y %H:%M:%S"), Desc, Location))
                del cursor
    del search
    print "finished process"

