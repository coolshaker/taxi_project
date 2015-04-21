#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time

def findNeighborhood(location, index, neighborhoods):
    match = index.intersection((location[0], location[1], location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    return -1

def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
#         if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx']: continue
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[3], paths))
    neighborhoods.append(('UNKNOWN', None))

def parseInput():
    for line in sys.stdin:
        line = line.strip('\n')
        values = line.split(',')
        if len(values)>1 and values[0]!='medallion': 
            yield values

def mapper():
    lng_id = 10 #pickup_lon 
    lat_id = 11 #pickup_lat
    pickup_datetime = 5
    
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('NYC_Census_Tract.shp', index, neighborhoods)
    agg = {}
    for values in parseInput():
        try:
            pickup_location = (float(values[lng_id]), float(values[lat_id]))
            pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
            if pickup_neighborhood!=-1:
                pickup_time = time.strptime(values[5], '%Y-%m-%d %H:%M:%S')
                year_month = str(pickup_time.tm_year) + ('%02d' % pickup_time.tm_mon)
                geoid = neighborhoods[pickup_neighborhood][0]
#                 print "%s\t%s" %( geoid, year_month)
                key = "%s,%s" %( geoid, year_month)
                agg[key] = agg.get(key, 0) + 1
        except:
            pass
    for item in agg.iteritems():
        print '%s\t%s' % item
    
if __name__=='__main__':
    mapper()
