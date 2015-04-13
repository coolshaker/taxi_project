import shapefile

sf = shapefile.Reader("shapefile/NYC_Census_Tract.shp")

#county_id = 1, geoid = 3
geomet = sf.shapeRecords()

for item in geomet:
    output_list = [item.record[1],item.record[3],item.shape.points]
    print output_list
