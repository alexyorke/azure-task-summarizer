import io
import time
import requests
import browser_cookie3
import os
import json
from pandas.tseries.offsets import BDay
import dateparser
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
YOUR_NAME = "ADD NAME HERE"

COMPANY = "COMPANY NAME SLASH ORG ID"
KEY = "PROJECT ID"
url = "EXCEL LINK TO YOUR GOOGLE CALENDAR SPREADSHEET"

def truncate(data, len):
    return data[:len] + (data[len:] and '...')


df = pd.read_csv("Everything I did_AzureQuery.csv")
for col in ["Closed Date", "Created Date", "Finish Date", "Start Date"]:
    df[col] = df[col].apply(
        lambda x: dateparser.parse(
            str(x)).replace(
            tzinfo=None))


# pd.datetime is an alias for datetime.datetime
previousDate = pd.datetime.today() - timedelta(1)

print("All things that I did on: " + str(previousDate))
filteredDf = df[(df['Closed Date'] > previousDate.replace(hour=0, minute=0)) & (
    df['Closed Date'] < previousDate.replace(hour=23, minute=59))]

# tasks completed/started
print("Tasks completed and started:")
for index, row in filteredDf.iterrows():
    print("- " +
          row['State'] +
          " " +
          row['Work Item Type'] +
          " #" +
          str(row['ID']) +
          ": " +
          row['Title'] +
          " at " +
          str(row['Closed Date']))

cj = browser_cookie3.firefox()

r = requests.get(url, cookies=cj, stream=True)

with io.BytesIO(r.content) as fh:
    dfs = pd.io.excel.read_excel(fh, sheet_name="Sheet1")

# fix dates
for col in ["Start Date", "End Date"]:
    dfs[col] = dfs[col].apply(
        lambda x: dateparser.parse(
            str(x)).replace(
            tzinfo=None))
filteredDf = dfs[(dfs['Start Date'] > previousDate.replace(hour=0, minute=0)) & (
    dfs['End Date'] < previousDate.replace(hour=23, minute=59))]


print("\nEvents attended:")
for index, row in filteredDf.iterrows():
    print("- " +
          str(row['Start Date']) +
          " - " +
          str(row['End Date']) +
          ": " +
          str(row['Event Title']) +
          ", " +
          truncate(str(row['Description']), 40) +
          " at " +
          str(row['Location']))


# Code Review

# Commented #n times (#totalWords words) on PR #prTitle by #author
print("\nCode Review:")

url = "https://dev.azure.com/" + COMPANY + "/_apis/git/repositories/" + \
    KEY + "/pullRequests/?searchCriteria.status=completed"

r = requests.get(url, cookies=cj)

data = json.loads(r.content)

threadFiles = {}
i = 0
for val in data["value"]:
    r = requests.get("https://dev.azure.com/" + COMPANY + "/_apis/git/repositories/" +
                     KEY + "/pullRequests/" + str(val["pullRequestId"]) + "/threads", cookies=cj)
    threadFiles[str(val["pullRequestId"])] = r.content
    time.sleep(4)
    i = i + 1
    if (i > 4):
        break

for aPRNumber, aThreadFile in threadFiles.items():
    totalComments = 0
    totalWords = 0
    data = json.loads(aThreadFile)
    for value in data["value"]:
        for comment in value["comments"]:
            if ("content" in comment):
                if (YOUR_NAME == comment["author"]["displayName"]) and (
                        "system" != comment["commentType"]):
                    if (
                        dateparser.parse(
                            comment["publishedDate"]).replace(
                            tzinfo=None) > previousDate.replace(
                            hour=0, minute=0).replace(
                            tzinfo=None)) and (
                        dateparser.parse(
                            comment["publishedDate"]).replace(
                            tzinfo=None) < previousDate.replace(
                                hour=23, minute=59).replace(
                                    tzinfo=None)):
                        print(
                            comment["author"]["displayName"] +
                            ":" +
                            comment["content"])
                        totalComments = totalComments + 1
                        totalWords = totalWords + \
                            len(comment["content"].split())

    print(
        "- Commented " +
        str(totalComments) +
        " times on PR #" + aPRNumber +
        " total " +
        str(totalWords) +
        " words")

print("\nCode Committed:")
commits = []
changeCounts = []
url = "https://dev.azure.com/" + COMPANY + \
    "/_apis/git/repositories/" + KEY + "/commits"
r = requests.get(url, cookies=cj)
totalComments = 0
totalWords = 0
data = json.loads(r.content)
for value in data["value"]:
    publishedOn = value["author"]["date"]
    if (
        value["author"]["name"] == YOUR_NAME) and (
        dateparser.parse(publishedOn).replace(
            tzinfo=None) > previousDate.replace(
            hour=0, minute=0).replace(
                tzinfo=None)) and (
                    dateparser.parse(publishedOn).replace(
                        tzinfo=None) < previousDate.replace(
                            hour=23, minute=59).replace(
                                tzinfo=None)):
        commits.append("- " + value["comment"])  # value["changeCounts"]
        changeCounts.append(value["changeCounts"])

commits = list(set(commits))

for commit in commits:
    print(commit)

print("\nTotal Changes:")
print("Lines Added: " + str(sum(c["Add"] for c in changeCounts)))
print("Lines Removed: " + str(sum(c["Delete"] for c in changeCounts)))
print("Lines Edited: " + str(sum(c["Edit"] for c in changeCounts)))
