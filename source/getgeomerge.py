import shapefile

sf = shapefile.Reader("shapefile/NYC_Census_Tract_Merge.shp")

geomet = sf.shapeRecords()
for item in geomet:
    output_list = [item.record[0],item.shape.points]
    print output_list
#     print item.record # geoid