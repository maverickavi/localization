import sys
import numpy as np
import math

o_flag = 0

class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class circle(object):
    def __init__(self, point, radius):
        self.center = point
        self.radius = radius

def get_two_points_distance(p1, p2):
    return math.sqrt(pow((p1.x - p2.x), 2) + pow((p1.y - p2.y), 2))

def get_two_circles_intersecting_points(c1, c2):
    p1 = c1.center 
    p2 = c2.center
    r1 = c1.radius
    r2 = c2.radius

    d = get_two_points_distance(p1, p2)
    # if too far away, or self contained - can't be done
    if d > (r1 + r2) or d <= math.fabs(r1 -r2):
        return None

    a = (pow(r1, 2) - pow(r2, 2) + pow(d, 2)) / (2*d)
    h  = math.sqrt(pow(r1, 2) - pow(a, 2))
    x0 = p1.x + a*(p2.x - p1.x)/d 
    y0 = p1.y + a*(p2.y - p1.y)/d
    rx = -(p2.y - p1.y) * (h/d)
    ry = -(p2.x - p1.x) * (h / d)
    return [point(x0+rx, y0-ry), point(x0-rx, y0+ry)]

def get_all_intersecting_points(circles):
    points = []
    num = len(circles)
    for i in range(num):
        j = i + 1
        for k in range(j, num):
            res = get_two_circles_intersecting_points(circles[i], circles[k])
            if res:
                points.extend(res)
    return points

def is_contained_in_circles(point, circles):
    for i in range(len(circles)):
        d = round((get_two_points_distance(point, circles[i].center))-(circles[i].radius),0)
        if (d > 0) and (d != 0):
            return False
    return True


def circles_cointaining_point(point, circles):
    circle_index = []
    for i in range(len(circles)):
        d = round((get_two_points_distance(point, circles[i].center))-(circles[i].radius),0)
        if d <= 0:
            circle_index.append(i)
    return circle_index


def get_polygon_center(points):
    center = point(0, 0)
    num = len(points)
    for i in range(num):
        center.x += points[i].x
        center.y += points[i].y
    center.x /= num
    center.y /= num
    return center

def RSSI_distance(n, A, RSSI):
    return np.power(10,(A-RSSI)/(10*n))



pts = []
refvec = [0, 1]

def clockwiseangle_and_distance(point):
    vector = [point[0]-origin[0], point[1]-origin[1]]
    lenvector = math.hypot(vector[0], vector[1])
    if lenvector == 0:
        return -math.pi, 0
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    return angle, lenvector

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def accuracy(area):
    return round(np.sqrt(area/np.pi),1)

def drawCircle(c, rad):
    circle1 = plt.Circle((c.x,c.y),rad,color = 'r', fill = False)
    return(circle1)

def convert_point(pt):
    return point(pt[0],pt[1])

x_data = []
y_data = []
n_data = []
A_data = []
RSSI_data = []
dist_data = []

Mx1 = []
Mx2 = []
My1 = []
My2 = []


for i in range(len(sys.argv)):
    if i % 5 == 1: 
     x_data.append(float(sys.argv[i]))

    elif i % 5 == 2 :
     y_data.append(float(sys.argv[i]))

    elif i%5 == 3: n_data.append(float(sys.argv[i]))
    elif i%5 == 4: A_data.append(float(sys.argv[i]))
    elif i%5 == 0 and i> 0: RSSI_data.append(float(sys.argv[i]))
   

po = [point(x_data[i],y_data[i]) for i in range(len(x_data))]


for i in range(len(x_data)):
 dist_data.append(RSSI_distance(n_data[i], A_data[i], RSSI_data[i]))

 Mx2.append(x_data[i]+dist_data[i])
 Mx1.append(x_data[i]-dist_data[i])
 My2.append(y_data[i]+dist_data[i])
 My1.append(y_data[i]-dist_data[i])

################Min-Max######################################################
y1 = max(My1)
y2 = min(My2)
x1 = max(Mx1)
x2 = min(Mx2)

intersection_pts = [[x1,y1], [x1,y2], [x2,y1], [x2,y2]]
Minmax_center = [round((x1+x2)/2,1),round((y1+y2)/2,1)]
Minmax_accuracy = round((np.sqrt(abs((x2-x1)*(y2-y1))))/2,0)
#print "$MINMAX/BOUNDING BOX METHOD$"
#print "Location:", Minmax_center
#print "Intersection points:",intersection_pts
#print "Accurate upto ", Minmax_accuracy, " meters"

##############Multilateration#####################################


        

#print "$MULTILATERATION$"

circles = [circle(po[i],dist_data[i]) for i in range(len(x_data))]

in_points = []

if len(get_all_intersecting_points(circles)) :
    for p in get_all_intersecting_points(circles):
        if is_contained_in_circles(p, circles):
            in_points.append(p) 
if len(in_points) > 2:
        center = get_polygon_center(in_points)
        c_w_center = circles_cointaining_point(center, circles)
if len(in_points) <= 2 or len(c_w_center) <= 2: 
    o_flag = 1
else:
       
#rounding to sub-meter level accuracy

    for i in range(len(in_points)):
        pts.append([in_points[i].x, in_points[i].y])
    origin = pts[0]
    f_in_points = []
    x_area = []
    y_area = []
    sorted_in_points = sorted(pts, key=clockwiseangle_and_distance)
    for i in range(len(sorted_in_points)):
        pon = (sorted_in_points[i])
        x_area.append(round(pon[0],1))
        y_area.append(round(pon[1],1))


    for i in range(len(sorted_in_points)):
        if i > 0:
            if (x_area[i] != x_area[i-1]) or (y_area[i] != y_area[i-1]):
                f_in_points.append([x_area[i],y_area[i]])
            
        elif i == 0:
            f_in_points.append([x_area[i],y_area[i]])

#    print "Location:", [round(center.x,1), round(center.y,1)]
#    print "Intersection points:", f_in_points
    if len(f_in_points) == 2:
        Multilateration_accuracy = round(get_two_points_distance(center, convert_point(f_in_points[0])),0)
#        print "Accurate upto ",Multilateration_accuracy, "meters"
    else: 
        Multilateration_accuracy = round(accuracy(PolyArea(x_area,y_area)),0)
#        print "Accurate upto ",Multilateration_accuracy, "meters"

if o_flag == 1:
    c_x = Minmax_center[0]
    c_y = Minmax_center[1]
    c_acc = Minmax_accuracy
    #print Minmax_center[0], ',', Minmax_center[1], ',', Minmax_accuracy
else: 
    if Minmax_accuracy < Multilateration_accuracy:
        c_x = Minmax_center[0]
        c_y = Minmax_center[1]
        c_acc = Minmax_accuracy
        #print Minmax_center[0], ',', Minmax_center[1], ',', Minmax_accuracy
    else:
        c_x = round(center.x,1)
        c_y = round(center.y,1)
        c_acc = Multilateration_accuracy
        #print round(center.x,1), ',', round(center.y,1), ',', Multilateration_accuracy

dist = round(math.sqrt(pow((c_x), 2) + pow((c_y), 2))/1000,4)
angle = math.degrees(math.atan2(c_x,c_y))
if angle < 0:
    ang = round((360 + angle),4)
else:
    ang = round(angle,4)

print c_x, ',', c_y, ',', dist, ',', ang, ',', c_acc
