# azure-task-summarizer
Summarizes your Azure DevOps activity (PR comments, tasks completed, etc.) It extracts PR comments, tasks, and more without needing an API key. It is not recommended to paste the report directly into your time tracking software as it is very verbose, and is used as a guide to help you summarize your tasks and time.

The setup process is _way_ too complicated, and the script is _extremely_ messy. It will get better over time as I consolidate some other scripts and make the process more efficient.

## Getting started

```
pip3 install -r requirements.txt
pip3 install cython
pip3 install numpy
pip3 install xlrd
```

If you are on Windows, install https://download.microsoft.com/download/5/f/7/5f7acaeb-8363-451f-9425-68a90f98b238/visualcppbuildtools_full.exe

Next, create an IFFT action that puts your Google Calendar into a spreadsheet that is owned by your organization (i.e. you have to log in to view the sheet.) For the row type, put this: `{{Title}} ||| {{Description}} ||| {{Starts}} ||| {{Ends}}|||{{EventUrl}}||| {{Description}}||| {{Where}}`

To get your organization ID, go to this URL: `https://dev.azure.com/companyname/_apis/projects` and save the id of the project you want to get a report from. Then, go to this URL: `https://dev.azure.com/companyname/_apis/projects/your_project_id` to get the repo id. Replace the company name with your company name slash your project id, then for the project id put the repo id. It's complicated.

Create an Azure task query. Follow the template in `Capture.PNG` in the repo. Go to `https://dev.azure.com/companyname/project/_queries` and then click "Add New Query", then fill in the template.

Also, add in your Google sheet URL to the script (and ensure that it downloads in xlsx form.) Log into your Google account and Azure in Firefox (as the cookies are stored there) before running the script. Substitute your name in the script as shown exactly as in Azure.

## How to run
When generating a report, first download your Azure task query as `Everything I did_AzureQuery.csv` and save it in the same directory as this script. This has to be done everyday. Then, run `python3 azure-task-summarizer.py > report.txt` to generate the report for yesterday. It will take a few minutes.

An example report:

All things that I did on: 2020-01-22 21:22:07.524631
Tasks completed and started:
- Closed Task #1111: Created something cool at 2020-01-22 16:05:45
- Started Task #1112: Created something cool at 2020-01-23 08:05:45

Events attended:
- 2020-01-22 10:00:00 - 2020-01-22 10:30:00: Stand-up, at room name here

- Author name: code review comment
- Author name: code review comment
- Author name: code review comment
- Author name: code review comment

Code Review:
- Commented 14 times on PR #143 total 100 words
- Commented 21 times on PR #333 total 20 words
- Commented 3 times on PR #222 total 30 words
- Commented 0 times on PR #464 total 0 words
- Commented 4 times on PR #262 total 10 words

Code Committed:

Total Changes:
Lines Added: 100
Lines Removed: 322
Lines Edited: 932
