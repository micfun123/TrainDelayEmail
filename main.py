import requests
import json
import sys
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


TrainDelaysAPIURl = "https://api.tfl.gov.uk/line/mode/tube/status"
data = requests.get(TrainDelaysAPIURl)
data = data.json()

Lines = []

for i in range(len(data)):
    name = data[i]["name"]
    problems = data[i]["disruptions"]
    status = data[i]["lineStatuses"][0]["statusSeverityDescription"]
    summary = f"{name} has these problems: {problems}. It is {status}."
    Lines.append(summary)

print(Lines)
#email users lines







    