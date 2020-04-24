import os
import gdal, ogr, osr
import geohash
import math
import sys
import time

#Controls
num_of_points = 50000
precision = 24
incrementor = 0.000005   #0.000001  6-8chars / 0.00000095 10 chars Max Res
start_xcor = 40.75870100
start_ycor = -111.87618300
crs_wk = "WGS84"
shp_file_name = "50k_000005" + str(precision) +"_"
print(shp_file_name)

def geohash_encodeTest(x, y, precision):
    ghash = geohash.encode(x, y, precision=precision)
    #print "ghash precision=22 is: ", ghash
    return ghash

def coordinate_constructor(num_pts, incrementor, starting_x, starting_y, precision):
    #this function needs to construct a list of coordinates in
    cor_list=[]
    temp_x_list=[]
    temp_y_list=[]
    x = starting_x
    y = starting_y
    i = 0
    while i <= math.sqrt(num_pts):
        temp_x_list.append(x)
        x = x + incrementor
        temp_y_list.append(y)
        y = y + incrementor
        i = i + 1
    for x in temp_x_list:
        for y in temp_y_list:
            ghash = geohash_encodeTest(x, y, precision)
            xy = [x, y, ghash]
            cor_list.append(xy)
    print(len(temp_x_list))
    return cor_list


#print(sys.modules)


def shp_construct(point_list, crs, file_name):
    #setup the performance variables
    begin= time.time()

    complete_filename= file_name + crs_wk + ".shp"  #GCS in wkt
    
    # set up the shapefile driver
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # create the data source
    data_source = driver.CreateDataSource(complete_filename)
    # create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS(crs)

    print("Semi minor axis: ", srs.GetSemiMinor())
    # create the layer
    layer = data_source.CreateLayer(file_name, srs, ogr.wkbPoint)
    # Add the fields we're interested in
    field_name = ogr.FieldDefn("ghash", ogr.OFTString)
    field_name.SetWidth(24)
    layer.CreateField(field_name)
    layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))

    #loop throught each point in the point list and write to the shpfile
    for i in point_list:
        # create the feature
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("ghash", i[2])
        feature.SetField("Latitude", i[0])
        feature.SetField("Longitude", i[1])
        # create the WKT for the feature using Python string formatting
        wkt = "POINT(%f %f)" %  ((i[1]) , (i[0]))
        # Create the point from the Well Known Txt
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)
        # Create the feature in the layer (shapefile)
        layer.CreateFeature(feature)
        # Dereference the feature
        feature = None
    # Save and close the data source
    data_source = None
        

    #performance testing- keep at end of function
    end=time.time()
    time_diff= end-begin
    print("seconds to complete shp_construct: ",time_diff)
    return


cor_list = coordinate_constructor(num_of_points, incrementor, start_xcor, start_ycor, precision)

shp_construct(cor_list, crs_wk, shp_file_name)
    


print("Number of points in the shapefile: ", len(cor_list))
print("Sample points near the end of the list: ", cor_list[100430:100450])
print("Size in memory of cor_list: ", sys.getsizeof(cor_list))
