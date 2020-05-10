try: 
    # Imported Libraries
    import arcpy
    from arcpy import env
    from arcpy.sa import *

    #Workspace - May need to change to run on other computer.
    
    env.workspace = "C:/Users/jimmy/Desktop/Final Project/FinalProject.gdb"
    env.overwriteOutput = True

    #User Input Varibles
    
    unitlow = arcpy.GetParameterAsText(0)
    unithigh = arcpy.GetParameterAsText(1)
    buffdist = arcpy.GetParameterAsText(2)
    zoningreq = arcpy.GetParameterAsText(3)
    unitField = arcpy.GetParameterAsText(4)
    MapPLUTO = arcpy.GetParameterAsText(5)
    housingunits = arcpy.GetParameterAsText(6)
    

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
    arcpy.Select_analysis("newconstruction", "C:/Users/jimmy/Desktop/Final Project/FinalProject.gdb/NewConstruction_UnitRange",whereClause1 + " AND " + whereClause2)


    #Buffer Operations

    arcpy.Buffer_analysis("NewConstruction_UnitRange", "NewConstruction_Select_Buffer", buffdist, "Full")

    #Select By Location

    arcpy.MakeFeatureLayer_management(MapPLUTO, "MapPLUTO_lyr")
    arcpy.SelectLayerByLocation_management("MapPLUTO_lyr", "INTERSECT", "NewConstruction_Select_Buffer", "", "NEW_SELECTION")
    arcpy.CopyFeatures_management("MapPLUTO_lyr", "Location_Parcels")

    #Copy Selected Features/Final Ouput

    arcpy.Select_analysis("Location_Parcels", "Possible_Parcels", whereClause3)


except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except:
    print "Process did not complete."
