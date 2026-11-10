README:

This system takes a deed boundary and the monuments you found, and computes where the missing corners should be

Python Version 3.7.0
pip install pandas numpy matplotlib
To run: python Main.py

List of files:
Anchor.py
BoundaryBuilder.py
Filter.py
Main.py
[Folder] Data
  -  [Folder] Job123
                - boundary_points.csv
                - fieldwork.csv
README.md

You will have the option to make a new job or to continue working on a previous one. The best way to test run the system is by running Job123, an example job with simulated field work that matches real surveying form: (point number, northing, easting, elevation, description)

Before running the program, visit the job folder (.../Data/Job123) to see the starting files. There are two: fieldwork.csv, and boundary_points.csv. Fieldwork is a simulated file that shows 8 rows indicating different located points. EIR means Existing Iron Rod, or that a property corner physical monument was located. FENCE are irrelevant points that need to be filtered out. Meanwhile, boundary_points is a table with points that show the corners of a boundary polygon outline. This file was made with our boundary_builder function.

When prompted to Type 1, 2, or 3: [Type '2' and Enter]
When prompted to Choose job: Choose the number that corresponds to Job123 [Type '1' and Enter-if you haven't added any jobs]

The user is given instructions:
"When you press Enter, a figure will appear plotting the boundary polygon (left) and the filtered fieldwork points (right). For each highlighted fieldwork point, enter the matching boundary point name numerically. Exit each figure to continue the assignment cycle."

This part of the system assigns each located monument to a corner of the deed boundary so that it can rotate and translate the outlines properly. The point marked with an orange circle indicates the current point being assigned. The correct user input should be:

(Figure is shown, user exits figure)
Enter the boundary point that corresponds to 1: [Type '1' and Enter]
(Figure is shown, user exits figure)
Enter the boundary point that corresponds to 2: [Type '2' and Enter]
(Figure is shown, user exits figure)
Enter the boundary point that corresponds to 3: [Type '3' and Enter]

Output:
Corner 1 to monument 1: 0.050 ft off
Corner 2 to monument 2: 0.067 ft off
Corner 3 to monument 3: 0.041 ft off

Search points: corner 0: northing 199999.905, easting 2300000.020
Fieldwork with search points saved to .../Data/Job123/fieldwork_with_search.csv
Press Enter to continue

The system run is now over. Navigate to your job folder (.../Data/Job123) to see the new filtered fieldwork file and the file updated with search points.