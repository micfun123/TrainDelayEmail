from matplotlib.style import context
import requests
import json
import sys
import smtplib
import email
from email.message import EmailMessage
import os
import ssl
import time

from sqlalchemy import true

while True:
    TrainDelaysAPIURl = "https://api.tfl.gov.uk/line/mode/tube/status"
    Londonoverground = "https://api.tfl.gov.uk/Line/london-overground/stoppoints"
    data = requests.get(TrainDelaysAPIURl)
    data = data.json()  
    londonabovegrounddata = requests.get(Londonoverground)
    londonabovegrounddata = londonabovegrounddata.json()

    Lines = []  
    abovegroundLines = []

    for i in range(len(data)):
        name = data[i]["name"]
        problems = data[i]["disruptions"]
        status = data[i]["lineStatuses"][0]["statusSeverityDescription"]
        summary = f"{name} has these problems: {problems}. It is {status}."
        Lines.append(summary)   

    for i in range(len(londonabovegrounddata)):
        name = londonabovegrounddata[i]["commonName"]
        status = londonabovegrounddata[i]["status"]
        print(name, status)
        if status == True:
            status = "Operational"
        else:
            status = "Not Operational"
        summary = f"{name} is {status}."
        abovegroundLines.append(summary)

    print(Lines)
    #email users lines  

    password = os.environ["GMAIL_PASSWORD"]
    users =[""]
    fromuser = os.environ["GMAIL_USER"]
    touser = users  

    subject = "Trains in London"
    body = "\n".join(Lines) + "\n\n" + "\n".join(abovegroundLines)

    em = EmailMessage()
    em.set_content(body)
    em['From'] = fromuser
    em['To'] = touser
    em['Subject'] = subject 

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(fromuser, password)
        server.send_message(em)
        print("Email sent")
        server.quit()  
        #update every 30 minutes 
        time.sleep(1800)






    