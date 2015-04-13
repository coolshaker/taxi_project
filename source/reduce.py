#!/usr/bin/python

import sys

current_geoid = None
current_ym = None
current_sum = 0
geoid = None
year_month = None
    
# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    
    geoid, year_month = line.strip().split("\t", 1)
    
    count = 1
    
    if geoid == current_geoid:
        if current_ym == year_month:
            current_sum += count
        else:
            print "%s\t%s\t%d" % (current_geoid,current_ym,current_sum)
            current_sum = count
            current_ym = year_month            
    else:
        if current_geoid:
            # output goes to STDOUT (stream data that the program writes)
            print "%s\t%s\t%d"%(current_geoid,current_ym,current_sum)
  
        current_geoid = geoid
        current_sum = count
        current_ym = year_month

print "%s\t%s\t%d"%(current_geoid,current_ym,current_sum)