# import all required libraries
import xlrd
import csv
import pandas as pd
import glob, os
from os import sys

#print(os.path.splitext("/path/to/some/file.txt")[0])

# Read .xls files from directory
xls_files = [file for file in glob.glob("*.xlsx")]

print(xls_files)

# Substring removal in String list
file_names = [sub.replace('.xlsx', '') for sub in xls_files]
print(file_names)

#file_dict = {file_names[i]: xls_files[i] for i in range(len(xls_files))}

def xls_to_csv(xls_file, file_name):
    """Convert xls to csv with correct format"""
    # Read and store content
    # of an excel file 
    read_file = pd.read_excel(xls_file)
  
    # Write the dataframe object
    # into csv file
    read_file.to_csv(file_name +'.csv', 
                  index = None,
                  header=True)



# convert list of files to  csv

create_csv_files = [xls_to_csv(xls_file, file_name) for xls_file, file_name in zip(xls_files, file_names)]

# Read .csv files from directory
csv_files = [file for file in glob.glob("*.csv")]

def find_delimiter(filename):
     """Find the delimiter in a given csv file"""
     sniffer = csv.Sniffer()
     with open(filename) as fp:
             delimiter = sniffer.sniff(fp.read(5000)).delimiter
     return delimiter

# remove unnecessary columns from dataframes
for csv_file in csv_files:
    # skiprows=34 will skip the first 34 lines and try to read from 35 line
    # remove headings
    df = pd.read_csv(csv_file, skiprows=1)
    print(df)
    df.columns = ['Angle\tDE']
    

    
    # add new headings
    
    # print the data frame
    print(df['Angle\tDE']) 

    # Output reformatted csv
    df.to_csv('test.csv', index=False)

# Read .csv files from directory again
csv_files = [file for file in glob.glob("*.csv")]


