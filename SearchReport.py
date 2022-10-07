#!/usr/bin/env python
""" Python Script to Search for Users from Calling Engagement Report Org in Control Hub
    
This script is designed to delete users from a Control Hub organization based on an INPUT CSV file with user emails.
The script is designed to be executed by users with "full admin" role in the org.
Output file called Errors.csv is generated at the end in the same directory as the input CSV file 
(Errors.csv will be empty if the script runs successfully without errors)
Tested with Python version 3.6
"""

__author__ = "Matt Klawiter"
__date__ = "2020/4/29"

__modification_by_author__ = "Ephraim Kakumani"
__date__ = "2022/9/19"

#############  Imports  #############
import requests
import json
import os
import csv
import urllib
import time
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)
pd.set_option("display.max_rows", None)

#############  Definitions  #############
csvFilePath = ''                                                        # Update this value to skip entering command line input

def display_():    
    from IPython.core.display import display 
    display(df_group_calls.first()) #df must be defined up there

#############   User Input and Validation  #############
print('This script requires two inputs:')
print('    1. The full file path on your device for an input CSV file\n (eg: C:\Scripts\exported_file.csv on Windows or ~/Scripts/exported_file.csv on Mac)\n')

validationSuccess = 0
# Loop to allow the user to input a file path and file name until successful.
while (validationSuccess == 0):
    if not csvFilePath :
        csvFilePath = input('Please enter the full file path of the CSV file you wish to use:  ')
    # Validate the Input CSV file exists.
    csvFilePath = os.path.expanduser(csvFilePath)
    if( not os.path.isfile(csvFilePath) ):
        print('No Input CSV file found on your device at: ' + csvFilePath)
        print('Please check the file path you entered above and try again.\n')
        csvFilePath = ''
    else:
        validationSuccess = 1
print('Input CSV file found at: ', csvFilePath, '\n')
errorFilePath = os.path.join(os.path.dirname(csvFilePath),'Errors.csv')

print('Loading CSV file. Please wait....', '\n')

startTime = time.time()
df = pd.read_csv(csvFilePath)
endTime = time.time()

print("Total number of records in CSV file :", len(df), '\n')
print("The time to load CSV file is :", round(endTime-startTime), "s", '\n')
#print("The time to load CSV file is :", round(endTime-startTime) * 10**3, "ms", '\n')
email_ids = list(map(str, input("Enter email/s: ").split()))

print('\n',"List of User Email Ids: ", email_ids, '\n')
#############   End User Input  and validation #############

#############   Search users and Display results  #############

df_email = pd.DataFrame()

for i in range(len(email_ids)):
    df_email_init = df.loc[(df['Email'] == email_ids[i])]
    df_email = pd.concat([df_email , df_email_init])

df_email_array = df_email['Call ID'].values
df_email_calls = df.loc[df['Call ID'].isin(df_email_array)]

df_group_calls = df_email_calls.groupby(['Call ID','Email'])

df_group = pd.DataFrame(df_email_calls.groupby(['Call ID','Email','Name']).size(),columns=['Count'])
#print('Total Number of Call Records', len(df_group_calls['Call ID'].unique()), '\n')

print(df_group_calls.first())
#df_group_calls.to_excel('SearchOutput.xls', index=False)
df_group.to_csv('SearchOutput.csv',index=True)
#display_()

#############   End Search users and Display results  #############

"""
Copyright 2022 <Cisco Systems inc>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
