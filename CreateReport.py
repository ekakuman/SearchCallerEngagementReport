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

#############  Definitions  #############
csvFilePath = ''                                                        # Update this value to skip entering command line input
accessToken = ''                                                        # Update this value to skip entering command line input
templateId = 116;
errorMessage = ''
reportURL = 'https://webexapis.com/v1/reports'         # Webex CH List People API URL
getMyDetailsURL = 'https://webexapis.com/v1/people/me' # Webex CH Get My Details API URL

#############   User Input and Validation  #############
print('This script requires two inputs:')
print('    1. Admin access token used to authorize the API calls\n       (You can get yours from https://developer.webex.com/docs/api/getting-started)')
print('    2. Start Date(YYYY-MM-DD), End Date((YYYY-MM-DD)) and siteList\n')

validationSuccess = 0

# Loop to allow the user to input an access token until successful.
while (validationSuccess == 0):
    if not accessToken :
        accessToken = input('Please enter your access token:  ')
        startDate = input('Please enter Start Date (YYYY-MM-DD):  ')
        endDate = input('Please enter End Date (YYYY-MM-DD):  ')
        siteList = input('Please enter siteList (e.g. <xyz>.webex.com):  ')
        payload = json.dumps({'templateId':templateId,'startDate': startDate, 'endDate': endDate, 'siteList': siteList})

    # Get People API Call to validate access token.
    validationResponse = requests.post(getMyDetailsURL,
                headers={'Authorization': 'Bearer ' + accessToken})
    if validationResponse.status_code == 401:
        # This means the access token was invalid.
        print('Access Token was invalid.  Please check your access token was entered correctly and hasn\'t expired and try again below.\n')
        accessToken = ''
    else:
        reportResponse = requests.post(reportURL,
                                              headers={'Authorization': 'Bearer ' + accessToken,
                                                       'Content-Type': 'application/json'}, 
                                              data=payload)
        # Pausing script for a 429 Error
        while reportResponse.status_code == 429:
            print('Webex returned a 429 response (too many API calls at once).  Pausing script for 30 seconds...')
            time.sleep(30)
            reportResponse = requests.post(reportURL,
                                              headers={'Authorization': 'Bearer ' + accessToken,
                                                       'Content-Type': 'application/json'}, 
                                              data=payload)
        if reportResponse.status_code != 200:
            # This means something went wrong.
            print('Error: Report Creation API call error', str(reportResponse.status_code))
            errorMessage = reportResponse.json()['message']
            with open('Errors.csv','a') as csvfile:
                csvfile.write(str(reportResponse.status_code) + ',' + errorMessage + '\n')
        else:
            print('Report Creation Status Code ' + str(reportResponse.status_code), '\n')
            print(reportResponse.json(), '\n')
            filename = 'reportid.json'
            with open(filename, 'w') as file_object:  #open the file in write mode
              json.dump(reportResponse.json(), file_object)
            print('Report Created succesfully.\n')
        validationSuccess = 1
print('Please check for errors in the file Errors.csv.\n')
#############   End User Input  #############