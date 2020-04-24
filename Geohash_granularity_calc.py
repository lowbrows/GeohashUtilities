#Python 3.6.6
import os
import gdal, ogr, osr
import geohash
import math
import sys
import time
from math import cos, sqrt

x = 25
y = 25
pre_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]


source = osr.SpatialReference()
source.ImportFromEPSG(4326)
target = osr.SpatialReference()
target.ImportFromEPSG(26912)
transform = osr.CoordinateTransformation(source, target)

def dist_km(bbox1):  #coords = (w,n) (w,s), (w, n) (e, n)
    R = 6371
    x1 = (lon2 - lon1) * cos( 0.5*(lat2+lat1) )
    y1 = lat2 - lat1
    d1 = R * sqrt( x*x + y*y )
    return d1

for i in pre_list:
    
    ghash = geohash.encode(x, y, precision=i)
    bboxname = "bbox_" + str(i)
    bboxname = geohash.bbox(ghash)
    print(bboxname)
    #dist = dist_km(bboxname)
    #print(dist)
