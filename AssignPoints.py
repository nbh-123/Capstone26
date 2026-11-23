import numpy as np
import matplotlib.pyplot as plt
import math

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
