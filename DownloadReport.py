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

#############  Definitions  #############
csvFilePath = ''                                                        # Update this value to skip entering command line input
accessToken = ''                                                        # Update this value to skip entering command line input
templateId = 116;
errorMessage = ''
reportURL = 'https://webexapis.com/v1/reports'         # Webex CH List People API URL
getMyDetailsURL = 'https://webexapis.com/v1/people/me' # Webex CH Get My Details API URL

#############   User Input and Validation  #############
print('This script requires two inputs:')
print('    1. An access token used to authorize the API calls\n       (You can get yours from https://developer.webex.com/docs/api/getting-started)')

validationSuccess = 0

# Loop to allow the user to input an access token until successful.
while (validationSuccess == 0):
    if not accessToken :
        accessToken = input('Please enter your access token:  ')

    # Get People API Call to validate access token.
    validationResponse = requests.post(getMyDetailsURL,
                headers={'Authorization': 'Bearer ' + accessToken})
    if validationResponse.status_code == 401:
        # This means the access token was invalid.
        print('Access Token was invalid.  Please check your access token was entered correctly and hasn\'t expired and try again below.\n')
        accessToken = ''
    else:
        reportFile = open('reportid.json')
        data = json.load(reportFile)
        reportID = data['items']['Id']
        reportFile.close()

        reportResponse = requests.get(reportURL + '?reportId=' + reportID,
                                      headers={'Authorization': 'Bearer ' + accessToken,
                                                'Content-Type': 'application/json'})
        # Pausing script for a 429 Error
        while reportResponse.status_code == 429:
            print('Webex returned a 429 response (too many API calls at once).  Pausing script for 30 seconds...')
            time.sleep(30)
            reportResponse = requests.get(reportURL + '?reportId=' + reportID,
                                      headers={'Authorization': 'Bearer ' + accessToken,
                                                'Content-Type': 'application/json'})
        if reportResponse.status_code != 200:
            # This means something went wrong.
            print('Error: Report Creation API call error', str(reportResponse.status_code))
            errorMessage = reportResponse.json()['message']
            with open('Errors.csv','a') as csvfile:
                csvfile.write(str(reportResponse.status_code) + ',' + errorMessage + '\n')
        else:
            statusDownload = reportResponse.json()['items'][0]['status']
            urlDownload = reportResponse.json()['items'][0]['downloadURL']

            # Save the report file to csv if the download status is successful
            if statusDownload != 'done':
                print('The report generation is in progress. Please try again after sometime', '\n')
            else:
                print('Report download URl: \n', urlDownload, '\n')
                reportDownload = requests.get(urlDownload,
                                        headers={'Authorization': 'Bearer ' + accessToken})
                urlContent = reportDownload.content
                csvFile = open('report.csv', 'wb')
                csvFile.write(urlContent)
                csvFile.close()
                print('The report downloaded successfully. Please check the local folder for file report.csv \n')
        validationSuccess = 1
print('Please check for errors in the file Errors.csv.\n')
#############   End User Input  #############
