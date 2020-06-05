# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:13:43 2020

@author: Yichen Wang
"""
from urllib.request import urlopen
import time
from gmail import oath2Gmail
from bs4 import BeautifulSoup
import threading
import logging
from sys import stderr

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(stream=stderr, level=logging.INFO, format=LOG_FORMAT)
#logging.basicConfig(filename=argv[1], level=logging.INFO, format=LOG_FORMAT)

# Git commit detecting part
def makeURL(owner, repo, branch='master'):
    return f'https://github.com/{owner}/{repo}/tree/{branch}'

def getNCommit(owner, repo, branch='master'):
    '''Using a BS4 method to make this crawler process readable.'''
    url = makeURL(owner, repo, branch)
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features="lxml")
    allSpan = soup.findAll("span", {"class": ["num", "text-emphasized"]})
    nCommit = int(allSpan[0].text.strip().replace(',', ''))
    return nCommit

def periodicalCatcher(owner, repo, senderEmail, receiverEmail, 
                      branch, interval):
    try:
        logging.info("Having an initial check")
        nCommit_Last = getNCommit(owner, repo, branch)
        logging.info(f"{owner}/{repo} {branch} currently has {nCommit_Last} commits.")
        time.sleep(interval)
        while True:
            try:
                nCommit_Now = getNCommit(owner, repo, 
                                         branch)
                if nCommit_Now != nCommit_Last:
                    nNew = nCommit_Now - nCommit_Last
                    logging.info(nNew, 'new commit found!')
                    message = f'Hi,\nThere are {str(nNew)} new commits found on {owner}/{repo}/{branch}'
                    oath2Gmail(message, senderEmail, 
                               receiverEmail)
                logging.info(f"{owner}/{repo} {branch} currently has {nCommit_Now} commits.")
                nCommit_Last = nCommit_Now
                time.sleep(interval)
            except KeyboardInterrupt:
                break
    except Exception as e:
        logging.error('Error encountered: ' + str(e))

