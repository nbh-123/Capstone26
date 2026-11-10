import pandas as pd
from pathlib import Path
DATA = Path(__file__).parent / "Data"

#This is a library of descriptions commonly used by surveyors to describe property corner physical monuments. 
#EIP = Existing Iron Pipe, EIR = Existing Iron Rod
LIBRARY = {'EIP', 'EIR', 'DISTURBED EIP', 'DISTURBED EIR', 'PINCHED PIPE', 'DISTURBED PINCHED PIPE', 
           'Eip', 'Eir', 'Disturbed Eip', 'Disturbed Eir', 'Pinched Pipe', 'Disturbed Pinched Pipe',
           'eip', 'eir', 'disturbed eip', 'disturbed eir', 'pinched pipe', 'disturbed pinched pipe'}

#If the fieldwork file exists, filter_job checks if each row has a description corresponding to our library. 
#Then, it rebuilds the file with only those relevant rows.
def filter_job(jobName):
     fieldworkFile = DATA / jobName / "fieldwork.csv"
     
     if not fieldworkFile.exists():
        print(f"No fieldwork file found. Move it into {DATA / jobName} and name it fieldwork.csv")
        return None

     #fieldwork: [0] point ID, [1] northing, [2] easting, [3] elevation [4] description
     fieldTable = pd.read_csv(fieldworkFile, header=None)                               #this line makes a pandas table that holds the fieldwork file
     filteredTable = fieldTable[fieldTable[4].isin(LIBRARY)].reset_index(drop=True)     #fieldTable[4] is the column that holds description codes


     out = fieldworkFile.with_name("fieldwork_filtered.csv")     #.with_name makes a new path to fieldwork_filtered.csv
     filteredTable.to_csv(out, index=False, header=False)        #this line builds the new filtered file

     print("Fieldwork file successfully found and filtered.")
     return filteredTable


