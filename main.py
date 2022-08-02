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

while True:
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

    password = os.environ["GMAIL_PASSWORD"]
    users =[""]
    fromuser = os.environ["GMAIL_USER"]
    touser = users  

    subject = "Tube Status"
    body = "\n".join(Lines) 

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
        time.sleep(1800)






    