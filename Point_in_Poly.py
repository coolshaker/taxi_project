#Define function
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

#Test
polygon = [(0,10),(10,10),(10,0),(0,0), (20,30),(30,30),(30,20),(20,20)]

point_x = 15
point_y = 15

print point_in_poly(5,5,polygon)
print point_in_poly(15,15,polygon)
print point_in_poly(25,25,polygon)