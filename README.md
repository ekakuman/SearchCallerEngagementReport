# webexControlHubScripts
Scripts utilizing the Cisco Webex Control Hub APIs

The objective of these scripts is to give the ability for the users to search for users grouped by 'Call ID' from the report generated using Calling Engagement Report template.

There are three scripts here to achieve this goal. 

First, CreateReport.py will make an API call with the right duration based on the template ID. The API call will generate the report. The report is not instant. Typically it takes 25-30 minutes based on the size of the report. DownloadReport.py will download the report from Webex Org into a CSV file locally. SearchReport.py then can be executed to search for the users and group them by Call ID.

Filename | Language | Description
--- | --- | ---
CreateReport.py | Python | Script to Create Report leveraring API calls to the Webex Org
DownloadReport.py | Python | Script to Download Report leveraring API calls to the Webex Org
SearchReport.py | Python | Script to Seach Users and group them by Call ID

Usage: python3 scriptfilename

Note: SearchReport.py can be executed independently if the report is already made available through other means. 
