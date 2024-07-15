"""
A script that will use Beautiful Soup and other webscraping techniques to ping the user if new jobs are posted.

"""

#Imports
from smtplib import SMTP
import numpy as np
import pandas as pd

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#Getting HTML
import requests
from requests_html import HTMLSession

#Parsing HTML
from bs4 import BeautifulSoup
import urllib
import json
import re

import time 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Safari 
from selenium.webdriver.common.by import By 
import pickle as pkl

from encryption import decrypt_password

def main():
    url = r"https://www.palantir.com/careers/"

    #We need to let JS load in the additional elements on the page, so we add the headless argument and other config
    options = webdriver.SafariOptions()
    options.add_argument("--headless")
    options.page_load_strategy = "none"
    driver = Safari(options=options) 
    driver.implicitly_wait(60)

    #Get the url data and wait https://www.zenrows.com/blog/scraping-javascript-rendered-web-pages#requirements
    driver.get(url)
    time.sleep(60) 


    #To verify that the elements loaded with JS are actually there, we will verify that the header "Internships" is been pulled in
    print("Internships are loaded in?")
    if "nternship" in driver.page_source:
        print("Yes!")
    else:
        print("No! Flagging Error")
        raise

    #Find the elements that contain the word 'Internship'. NOTE: This will include elements that are not what we are looking for. 
    content = driver.find_elements(by = By.XPATH, value = r"//*[contains(text(), 'Internship')]")
    print("Internships were found")

    #Edge case for the special "Semester at Palantir" co-op
    try:
        semester = driver.find_elements(by = By.XPATH, value = r"//*[contains(text(), 'emester')]")
    except:
        print("The 'Semester at Palantir' Internship is not available")

    
    # A note to get element's children. This is not used here but it is useful
    # https://stackoverflow.com/questions/45174799/how-to-find-the-child-elements-of-a-specific-webelement-which-i-dont-know-the

    #Determine if each job is 1) an actual job on the website (and not just a banner) and 2) NEW
    job_name_list = []
    for element in content:
        job_name = element.text


        ####################################
        ######### Text Processing #########
        ####################################
        #Replace the arrow they have on the website
        job_name = job_name.replace("→", "")
        #Clear leading and trialing whitespace
        job_name = job_name.strip()
        words = job_name.split(" ")

        if len(words) > 1: #Actual job, not just the word Internship on the page somewhere
            job_name_list.append(job_name)

    #Pull yesterday's jobs
    with open("yesterdays_jobs.txt", "r") as f:
        yesterdays_jobs = f.readlines()
    
    yesterdays_jobs = set(yesterdays_jobs)

    #Determine which of today's jobs are new and notify
    new_jobs = []
    for job in job_name_list:
        if job not in yesterdays_jobs:
            new_jobs.append(job)
            
    notify(new_jobs)



    #Overwrite yesterday's jobs by writing ALL of today's jobs
    with open("yesterdays_jobs.txt", "w") as f:
        f.writelines(job_name_list)


def notify(new):
    
    # Email credentials
    smtp_server = 'smtp.gmail.com'  # For Gmail
    smtp_port = 587
    sender_email = decrypt_password(open("sender.bin", 'rb').read())
    sender_password = decrypt_password(open("pass.bin", 'rb').read())  # Use App Password if 2FA is enabled
    receiver_email = decrypt_password(open("reciever.bin", 'rb').read())

    # Email content
    subject = 'Palantir Jobs'
    body = " ".join(new)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server and login
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        print('Email sent successfully')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        # Close the connection
        server.quit()


if __name__ == "__main__":
    main()