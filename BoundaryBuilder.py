import math
import matplotlib.pyplot as plt

#build_boundary it updates the x and y coordinates with new user-inputted calls and uses them to update a list of  boundary points. 

def build_boundary(jobFolder):
    points = [(0.0, 0.0)]           #this list holds the boundary points
    x, y = 0.0, 0.0                 #these values are the current position in easting, northing

    while True:
        bearing = input("\nEnter Bearing (Azimuth, degrees), or press Enter to finish: ")
        if bearing == "": break
        bearing = float(bearing)
        distance = float(input("Enter Distance (ft): "))

        #usually, x is cos and y is sin, but azimuth is clockwise starting at north,
        #so it's the opposite. the updated x's and y's give the new point every call
        x += distance * math.sin(math.radians(bearing))         
        y += distance * math.cos(math.radians(bearing))
        points.append((x, y))
    #math.hypot gives the sqrt(a^2 + b^2), or the hypotenuse of a right triangle. The last point
    #on our boundary makes a diagonal from the origin like the hypotenuse of a right triangle with 
    #length = x and height = y. The hypotenuse gives the distance from the last point to the origin.
    misclosure = math.hypot(x, y)
    print(f"\nMisclosure: {misclosure:.2f} ft")

    with open(jobFolder / "boundary_points.csv", "w") as file: #opens the boundary points file for writing
        file.write("point,northing,easting\n")                  #writes a header
        for number, (px, py) in enumerate(points):
            file.write(f"{number},{py:.3f},{px:.3f}\n")         #writes each point to boundary file

    xs, ys = zip(*points)                       #unpacks the points list into the x's and y's
    plt.plot(xs, ys, color="red", marker="o")   #plot everything
    plt.gca().set_aspect("equal")
    plt.grid(True)
    plt.show()

    return points