import arcpy
from arcpy import env
from arcpy.sa import *
env.workspace = "C:/Users/jimmy/Desktop/Final Project/FinalProject.gdb"
env.overwriteOutput = True

#Defined Varibles

MapPLUTO = "MapPLUTO"
housingunits = "Housing_Units"
unitField = 'All_Counted_Units'
unitlow = 10
unithigh = 100
buffdist = 100
zoningreq = "R6"

#Select Where Clauses

whereClause1 = "\"%s\" >= %s" % (unitField, unitlow)
whereClause2 = "\"%s\" <= %s" % (unitField, unithigh)

if zoningreq == "R6":
    whereClause3 = "ZoneDist1 = 'R6' OR ZoneDist1 = 'R6A'  OR ZoneDist1 = 'R6B'"
elif zoningreq == "R7":
    whereClause3 = "ZoneDist1 = 'R7-1' OR ZoneDist1 = 'R7-2' OR ZoneDist1 = 'R7-3' OR ZoneDist1 = 'R7A' OR ZoneDist1 = 'R7B'  OR ZoneDist1 = 'R7D' OR ZoneDist1 = 'R7X'"
elif zoningreq == "R8":
    whereClause3 = "ZoneDist1 = 'R8' OR ZoneDist1 = 'R8A'  OR ZoneDist1 = 'R8B' OR ZoneDist1 = 'R8X'"
elif zoningreq == "R9":
    whereClause3 = "ZoneDist1 = 'R9' OR ZoneDist1 = 'R9-1' OR ZoneDist1 = 'R8A' OR ZoneDist1 = 'R8X'"
else:
    whereClause3 = "ZoneDist1 = 'R10' OR ZoneDist1 = 'R10H'"

#Housing Select Operations

arcpy.Select_analysis(housingunits, "C:/Users/jimmy/Desktop/Final Project/FinalProject.gdb/newconstruction", "Reporting_Construction_Type = 'New Construction'")
arcpy.Select_analysis("newconstruction", "C:/Users/jimmy/Desktop/Final Project/FinalProject.gdb/newconstruction_select",whereClause1 + " AND " + whereClause2)


#Buffer Operations

arcpy.Buffer_analysis("newconstruction_select", "newconstruction_select_buffer", buffdist, "Full")

#Select By Location

arcpy.MakeFeatureLayer_management(MapPLUTO, "MapPLUTO_lyr")
arcpy.SelectLayerByLocation_management("MapPLUTO_lyr", "INTERSECT", "newconstruction_select_buffer", "", "NEW_SELECTION")
arcpy.CopyFeatures_management("MapPLUTO_lyr", "Location_Parcels")

#Copy Selected Features/Final Ouput

arcpy.Select_analysis("Location_Parcels", "possible_parcels", whereClause3)
