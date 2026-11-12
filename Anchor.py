import numpy as np
import matplotlib.pyplot as plt
import math

# anchor.py takes boundary and points as input. They are two tables holding points:
#boundary: point, northing, easting
#points: name, northing, easting, elevation, description

#To align two sets of points, the steps are to: 
#    1. find the centroids
#    2. subtract each point from its centroid to find the needed rotation
#    3. translate the boundary points so the center is at  origin
#    4. rotate the boundary points according to step 2
#    5. translate the boundary points to the field points


#4x4 matrix that turns points counterclockwise by theta (radians)
def rotate(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta),  np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],    
    ])
#4x4 matrix that slides points east and north
def translate(east, north):
    return np.array([
        [1, 0, 0, east],
        [0, 1, 0, north],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

def find_angle(fieldList, boundaryList, field_centroid, boundary_centroid):
    dot_sum = 0
    cross_sum = 0
    
    # offsets from each centroid: easting = x, northing = y
    for i in range(len(fieldList)):
        #easting offset = boundary_easting - boundary_centroid_easting
        boundary_x = boundaryList[i][2] - boundary_centroid[1]
        #northing offset = boundary_northing - boundary_centroid_northing
        boundary_y = boundaryList[i][1] - boundary_centroid[0]

        #easting offset = field_easting - field_centroid_easting
        field_x = fieldList[i][2] - field_centroid[1]
        #northing offset = field_northing - field_centroid_northing
        field_y = fieldList[i][1] - field_centroid[0]

        #adds up the dot and cross totals across all pairs
        dot_sum += boundary_x * field_x + boundary_y * field_y
        cross_sum += boundary_x * field_y - boundary_y * field_x

    #turns the totals into the angle (radians) the boundary must turn to match the field
    return math.atan2(cross_sum, dot_sum)     

#pushes one point through the 4x4 matrix and finds new northing and easting
def move_point(matrix, northing, easting):
    moved = matrix @ np.array([easting, northing, 0, 1])
    return moved[1], moved[0]       # back to (northing, easting)


def find_search_points(boundary, boundaryList, matrix):
    matched = [entry[0] for entry in boundaryList]   # corner numbers that have a monument
    deed = boundary[:-1]        #removes last row of boundary because its a repeat
    searchList = []     
    for i in range(len(deed)):
        if i in matched:
            continue            #already found
        north, east = move_point(matrix, deed["northing"][i], deed["easting"][i])  # finds the search point based on the anchoring
        searchList.append((i, north, east))     #saves the corner to a list of search points
    return searchList


#this function assigns each fieldwork point to a boundary point
def assign_points(boundary, points):
    fieldList = []
    boundaryList = []
    
    input("\n\n When you press Enter, a figure will appear plotting the boundary polygon (left) and the filtered fieldwork points (right). For each highlighted fieldwork point, enter the matching boundary point name numerically. Exit each figure to continue the assignment cycle.")

    for i in range(len(points)):        #use len(points) to match field-located points to boundary corners
        plot(boundary, points, i)       #plots the boundary and fieldwork next to eachother, and i, the point thats being referenced
        match = int(input(f"Enter the boundary point that corresponds to {points[0][i]}: "))

        # field entry:      point name          Field Northing          Field Easting
        # boundary entry:   Boundary ID         Boundary Northing       Boundary Easting
        fieldEntry =        (points[0][i],      points[1][i],           points[2][i])
        boundaryEntry =     (match,             boundary["northing"][match],   boundary["easting"][match])

        fieldList.append(fieldEntry)
        boundaryList.append(boundaryEntry)
    
    return fieldList, boundaryList

#this function averages the northing and eastings of the matched points
def find_centroid(entries):
    north_total = 0     #running sum of northings
    east_total = 0      #running sum of eastings
    for entry in entries:
        north_total += entry[1] #entry[1] = northing
        east_total += entry[2]  #entry[2] = easting
    count = len(entries)
    return north_total / count, east_total / count  #averages

#plots the points side by side so users can choose which are matching
def plot(boundary, points, highlight):  #highlight is the current point # being emphasized
    deed = boundary[:-1]                #removes the last row of boundary because its a repeat
    deed_e = list(deed["easting"]) 
    deed_n = list(deed["northing"])

    names = list(points[0])
    found_e = list(points[2])
    found_n = list(points[1])

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 5))

    left.plot(deed_e + [deed_e[0]], deed_n + [deed_n[0]], color="red", marker="o")
    for i in range(len(deed_e)):
        left.annotate(str(i), (deed_e[i], deed_n[i]), textcoords="offset points", xytext=(6, 6), fontsize=12)
    left.set_title("Deed boundary (corner numbers)")

    right.plot(found_e, found_n, "bs", linestyle="none")
    right.plot(found_e[highlight], found_n[highlight], "o", color="orange", markersize=16, markeredgecolor="black", zorder=5)
    for i in range(len(names)):
        right.annotate(str(names[i]), (found_e[i], found_n[i]), textcoords="offset points", xytext=(6, 6), fontsize=12)
    right.set_title("Found monuments (point names)")

    for axis in (left, right):
        axis.set_aspect("equal")
        axis.margins(0.15)
        axis.grid(True)
    plt.show()

# this is the main function of Anchor.py. It runs the whole process starting by assigning
# the points, then finding the centroids, passing all of this to the find_angle function that 
# figures out how to rotate the boundary to match the fieldwork. Then everything is implemented in a matrix
# with a translation and rotation. finally it moves each corner to match the matrix, calculates the error and 
# gives a list of search points. 
     
def anchor_points(boundary, points):
    fieldList, boundaryList = assign_points(boundary, points) #assings points so the fieldList matches to the boundaryList

    #calculates centroids / center points
    field_centroid = find_centroid(fieldList) 
    boundary_centroid = find_centroid(boundaryList)

    #finds angle of rotation from centroid offsets
    theta = find_angle(fieldList, boundaryList, field_centroid, boundary_centroid)

    # centroids are (northing, easting) but translate() wants (east, north) --> minus sign
    matrix = (translate(field_centroid[1], field_centroid[0])
              @ rotate(theta)
              @ translate(-boundary_centroid[1], -boundary_centroid[0]))

    # checks that each matched corner lands on its monument and prints distance error 
    print(f"/n/n/n")
    for i in range(len(fieldList)):
        north, east = move_point(matrix, boundaryList[i][1], boundaryList[i][2])
        miss = math.hypot(north - fieldList[i][1], east - fieldList[i][2])
        print(f"Corner {boundaryList[i][0]} to monument {fieldList[i][0]}: {miss:.3f} ft off")

    searchList = find_search_points(boundary, boundaryList, matrix)
    print("Search points:")
    for number, north, east in searchList:
        print(f"  corner {number}: northing {north:.3f}, easting {east:.3f}")

    return searchList

