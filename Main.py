from pathlib import Path
from Filter import filter_job
from BoundaryBuilder import build_boundary
from Anchor import anchor_points
import pandas as pd

DATA = Path(__file__).parent / "Data"
DATA.mkdir(exist_ok=True) #creates DATA if missing

#This function prints the job folders of current jobs and returns the users job choice
def choose_job():       
    joblist = []
    for item in DATA.iterdir():                             #iterates through DATA folder 
        if item.is_dir(): joblist.append(item.name)         #if folder: append to joblist
    joblist.sort()
    if len(joblist) == 0:
        return None

    for i, jobName in enumerate(joblist, start = 1):        #cycles thru and prints job titles
        print(f"{i}: {jobName}")
    choice = int(input(f"Choose job (1-{len(joblist)}): "))
    return joblist[choice - 1]

#This function makes a new job folder and calls BoundaryBuilder
def new_job():
    address = input("Enter the address of your new job: ")
    address = address.replace("/", "-")                     #so that slashes don't change the directory
    jobFolder = DATA / address
    jobFolder.mkdir()                                       #mkdir = make directory

    print(f"Great. Your new {address} job file lives in the folder:  {jobFolder}")
    choice = input("The next step is building a job boundary. Press Enter to continue, or e to exit.")
    if choice.lower() == 'e': return
    build_boundary(jobFolder)                                #build_boundary builds a list of boundary points

#This function makes search points given the name of a job. It calls
#filter_job and anchor_points to map the fieldwork file onto the existing boundary
def make_search_points(jobName):
    #1. filters fieldwork file
    fieldPoints = filter_job(jobName)
    if fieldPoints is None: return 

    #2. builds boundary
    path = (DATA / jobName / "boundary_points.csv")                                   
    if not path.exists():                                               
        print("No file found. Build a boundary outline and return.")
        return
    boundary = pd.read_csv(path)    

    #3. anchors boundary to points
    searchList = anchor_points(boundary, fieldPoints)

    if len(searchList) == 0:
        print("Every corner has a monument, so there are no search points.")
        return

    #4. adds the search points to a copy of the fieldwork file
    searchPoints = []
    for i, north, east in searchList:
        searchPoints.append([(999 + i), round(north, 3), round(east, 3), "", "SEARCH"])

    fieldFile = DATA / jobName / "fieldwork.csv"
    outFile = DATA / jobName / "fieldwork_with_search.csv" #output file path

    fieldwork = pd.read_csv(fieldFile, header=None)
    combined = pd.concat([fieldwork, pd.DataFrame(searchPoints)]) #adds the search points at the end of the fieldwork file
    combined.to_csv(outFile, index=False, header=False)
    print(f"Fieldwork with search points saved to {outFile}")
    input("Press Enter to continue")

#Main calls the other functions and handles user interaction
def main():
    print("Hi user, welcome to SPG, a software designed to help surveyors find property corners.")

    while True:
        print("\n  1) Start a new job")
        print("  2) Make search points for an existing job")
        print("  3) Quit")
        choice = input("Type 1, 2 or 3: ")

        if choice == "1": new_job()

        elif choice == "2":
            jobName = choose_job()
            if jobName is None:
                print("\nThere are no jobs yet, so let's start a new one.")
                new_job()
            else: 
                make_search_points(jobName)

        elif choice == "3":
            print("Goodbye.")
            break
        else: print("Please type 1, 2 or 3.")

main()