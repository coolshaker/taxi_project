#!/usr/bin/python
from datetime import date, datetime
import sys
###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### check whether a point is in a polygon
def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###retrieve geo boundary of each county
### data kept in geo_loc_list_merge
def getcounty():
    file = open('geolocationmerge.txt', 'r')
    
    geo_loc_list_merge = []
    for line in file:
        geo_line = []
        geo_list = []
    #     print line[8:-2] # geo boundary
        tmp1 = line[8:-2]
        tmp2 = tmp1.replace('[','').replace(']','')
        tmp3 = tmp2.strip().split(',')
        
        length = len(tmp3) 
        i = 0
        val = []
        for i in range(length):
            tmp4 = float(tmp3[i].strip())
            if (i%2==0):
                val = []
                val.append(tmp4)
            else:
                val.append(tmp4)
                geo_list.append(val)
        geo_line.append(line[2:5]) # county id
        geo_line.append(geo_list)
        
        geo_loc_list_merge.append(geo_line) 
    file.close()
    return geo_loc_list_merge
###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###retrieve geo boundary of each census tract
### data kept in geo_loc_census_tract
def getcensustract():
    file = open('geolocationcensustract.txt', 'r')
    
    geo_loc_census_tract = {}
    for line in file:
        geo_line = []
        geo_list = []
        tmp1 = line[23:-2] #geo boundary
        tmp2 = tmp1.replace('[','').replace(']','')
        tmp3 = tmp2.strip().split(',')
    
        length = len(tmp3) 
        val = []
        for i in range(length):
            tmp4 = float(tmp3[i].strip())
            if (i%2==0):
                val = []
                val.append(tmp4)
            else:
                val.append(tmp4)
                geo_list.append(val)
        geo_line.append(line[9:20]) # geoid
        geo_line.append(geo_list)
        
        county_id = line[2:5] #county id
        if county_id not in geo_loc_census_tract:
            geo_loc_census_tract[county_id] = []
        geo_loc_census_tract[county_id].append(geo_line)
        
    file.close() 
    return geo_loc_census_tract   
# for key in geo_loc_census_tract:
#     print key
#     print len(geo_loc_census_tract[key])
#     for l in geo_loc_census_tract[key]:
#         print l         

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### get county id
def get_county_id(x,y):
    county_id = 0
    for county in geo_loc_list_merge:
        if (point_in_poly(x, y,county[1])):
            county_id = county[0]
            break
    return county_id

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### get geoid
def get_geoid(x,y,tract_in_county):
    geoid = 0
    for tract in tract_in_county:
        if (point_in_poly(x, y,tract[1])):
            geoid = tract[0]
            break
    return geoid
# county_id =  get_county_id(-73.983803, 40.743511)
# tract_in_county = geo_loc_census_tract[county_id]
# print county_id
# print get_geoid(-73.983803, 40.743511,tract_in_county)

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### mapper
geo_loc_list_merge = []
if __name__ == '__main__':
    lon_id = 10 #pickup_lon 
    lat_id = 11 #pickup_lat
    pickup_datetime = 5
    
    geo_loc_list_merge = getcounty()
    geo_loc_census_tract = getcensustract()
    
    # input comes from STDIN (stream data that goes to the program)
    i = 0
    for line in sys.stdin:
        if (i == 0):
            if (line[:9] == 'medallion'): #medallion
                i = i + 1
                continue
            else:
                break
        i = i + 1
    
        value = line.strip().split(',')
        try:
            lon = float(value[lon_id])
            lat = float(value[lat_id])
            
            if (lon == 0 or lat ==0):
                continue
          
            county_id = 0
            geoid = 0
            # get county id
            county_id =  get_county_id(lon, lat)
            if (county_id != 0):
                tract_in_county = geo_loc_census_tract[county_id]
                geoid = get_geoid(lon, lat,tract_in_county)
            if (geoid != 0):
                currentday = datetime.strptime(value[pickup_datetime], '%Y-%m-%d %H:%M:%S')
                year_month = str(currentday.year) + ('%02d' % currentday.month)
                print "%s\t%s" %( geoid, year_month)
        except:
            pass

    