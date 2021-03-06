#!/usr/bin/python

import csv
import sys
import requests
from HTMLParser import HTMLParser

project = ""


class MyHTMLParser(HTMLParser):

    foundBlock = False
    foundLanguage = False
    foundCodeLines = False
    foundTotalLines = False
    foundPercentage = False

    language = ""
    codeLines = -1
    totalLines = -1
    percentage = -1

    tdCounter = 0

    def handle_starttag(self, tag, attrs):
        if self.foundBlock and tag == 'a':
            self.foundLanguage = True
        elif self.foundLanguage and tag == 'td':
            self.foundCodeLines = True
            self.foundLanguage = False
        elif self.codeLines != -1 and tag == 'td' and len(attrs) > 0 and attrs[0][1] == "center":
            if self.tdCounter == 3:
                self.tdCounter = 0
                self.foundTotalLines = True
            else:
                self.tdCounter += 1


        elif tag == 'tr' and len(attrs) > 0 and attrs[0][0] == "class":
            self.foundBlock = True

        elif tag == 'span' and len(attrs) > 0 and attrs[0][1] == "pull-right":
            self.foundPercentage = True

    def handle_data(self, data):
        if self.foundLanguage and self.language == "":
            self.language = data
        elif self.foundCodeLines and self.codeLines == -1:
            self.foundCodeLines = False
            self.codeLines = data
        
        if self.foundTotalLines:
            self.foundTotalLines = False
            self.totalLines = data

        if self.foundPercentage:
            self.foundPercentage = False
            self.percentage = data.replace("%","").strip()

    def handle_endtag(self, tag):
        if tag == 'tr' and self.foundBlock:
            #Final output
            if float(self.percentage) >= 0.5 and languages.__contains__(self.language):
                print(project + "|" + self.language + "|" + self.codeLines + "|" + self.totalLines + "|" + self.percentage)
            self.foundBlock = False
            self.language = ""
            self.codeLines = -1
            self.totalLines = -1
            self.percentage = -1


#OpenHub main URL
URL = "https://www.openhub.net/p/{0}/analyses/latest/languages_summary"

# Line command CSV file argument
projectFile = sys.argv[1]
languageFile = sys.argv[2]

languages = set()

print("Project|Language|CodeLines|TotalLines|Percentage")

with open(languageFile, 'rU') as f:
    freader = csv.reader(f)
    for row in freader:
        languages.add(row[0])

with open(projectFile, 'rU') as f:
    freader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in freader:
        project = row[0]

        resp = requests.get(url=URL.format(project))
        parser = MyHTMLParser()
        parser.feed(resp.text)
