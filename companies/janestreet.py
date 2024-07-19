
#Imports
from smtplib import SMTP
import numpy as np
import pandas as pd
import requests
import bs4
import re


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pickle as pkl

#Parsing HTML
import time 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Safari 
from selenium.webdriver.common.by import By 

# from encryption import decrypt_password


def janestreet():
    url = r"https://boards.greenhouse.io/janestreet/"

    result = requests.get(url = url)

    soup = bs4.BeautifulSoup(result.content, 'html.parser')

    # titles = soup.find_all(lambda tag: "uantitative" in tag.get_text() and 'United States' in tag.get_text())
    # Define the list of target texts to search for within the <a> tags
    target_texts = ["uantitative", "software", "achine learning", "ntern"] 
     
    
    # Define the href pattern
    href_pattern = re.compile(r'^/janestreet/jobs/\d+$')
    
    matching_tags = soup.find_all('a', attrs={'data-mapped': 'true'})
    ans = []
    for tag in matching_tags:
        if any(target_text in tag.get_text() for target_text in target_texts) and href_pattern.match(tag['href']):
            ans.append(tag)

    for tag in ans:
        print(f"Tag: {tag}, Href: {tag['href']}")



    print("Done!")





if __name__ == "__main__":
    janestreet()