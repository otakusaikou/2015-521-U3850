#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcpy


def main():
    # Define source files
    ptSource = "..\shp\Schools.shp"
    polySource = "..\shp\Stown.shp"

    # Create a template layer
    arcpy.MakeFeatureLayer_management(ptSource, "pointsLyr")

    # Dictionary of school number
    data = {}

    # Get cursor of target shapefile
    with arcpy.da.SearchCursor(
            polySource, ["OID@", "SHAPE@", "ETOWNNAME"]) as cursor:
        # Iteration
        for row in cursor:
            arcpy.SelectLayerByLocation_management(
                "pointsLyr",
                select_features=row[1])
            # Get count of schools with in polygon
            count = int(arcpy.GetCount_management("pointsLyr").getOutput(0))
            data[row[2]] = count

    dataVal = data.values()

    # Output result
    print "Have most schools (%d schools):" % max(dataVal)
    for key, value in data.items():
        if value == max(dataVal):
            print " " + key
    print "Have least schools (%d schools)" % min(dataVal)
    for key, value in data.items():
        if value == min(dataVal):
            print " " + key


if __name__ == "__main__":
    main()
