#!/usr/bin/env python
""" Python Script to Search for Users from Calling Engagement Report Org in Control Hub
    
This script is designed to delete users from a Control Hub organization based on an INPUT CSV file with user emails.
The script is designed to be executed by users with "full admin" role in the org.
Output file called Errors.csv is generated at the end in the same directory as the input CSV file 
(Errors.csv will be empty if the script runs successfully without errors)
Tested with Python version 3.6
The script is limited to only allow 100 users per input file.
If you need to delete more than 100 users then you need to split users into multiple CSV input files or modify the script.

The CSV file should be created using the format from the CSV export from Control Hub.
- Keep the rows of users that should be deleted and REMOVE USERS who should NOT be deleted
- Do not delete the header line, or the first user to delete will be skipped
- Very little validation is done of the input file.  Deleting fields can break this script.
- (The fourth field of each row is the email of the user that will be deleted)
- IMPORTANT:  THE FILE SHOULD ONLY HAVE ENTRIES OF USERS THAT SHOULD BE DELETED

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

#############  Definitions  #############
def display_():    
    pd.set_option("display.max_rows", None)
    from IPython.core.display import display 
    display(df_group_calls.first()) #df must be defined up there

#############   User Input and Validation  #############
print('This script requires two inputs:')
print('    1. The full file path on your device for an input CSV file\n       (ex: C:\Scripts\exported_file.csv on Windows or ~/Scripts/exported_file.csv on Mac)\n')
print('    2. An access token used to authorize the API calls\n       (You can get yours from https://developer.webex.com/docs/api/getting-started)')
print('    If you changed these variables in the script itself, it will attempt to validate and use those values instead\n')
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

print('Loading CSV file.. please wait.')

df = pd.read_csv(csvFilePath)
email_ids = list(map(str, input("Enter email/s:").split()))
print("List of User Email Ids: ", email_ids, '\n')
#############   End User Input  #############

df_email_0 = df.loc[(df['Email'] == email_ids[0])]
df_email_1 = df.loc[(df['Email'] == email_ids[1])]
df_email = pd.concat([df_email_0 , df_email_1])

df_email_array = df_email['Call ID'].values
df_email_calls = df.loc[df['Call ID'].isin(df_email_array)]
df_group_calls = df_email_calls.groupby(['Call ID','Email'])

print('Call records found with the user details below', '\n')

pd.set_option("display.max_colwidth", None)
#print(df_group_calls.first())

display_()

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
