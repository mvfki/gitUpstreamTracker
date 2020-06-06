# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 22:42:56 2020

@author: Yichen Wang

Due to wierd multiprocessing package feature, the job send to Process() has to
be something imported from a submodule. So...
"""
from time import strftime, sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sys import stdout

from .gmail import oath2Gmail

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
                      branch, interval, logs):
    def logger(level, *args):
        body =  f"{strftime('%Y-%m-%d %H:%M')} - {level.upper()} - "
        pieces = [str(i) for i in args]
        msg = body + ' '.join(pieces)
        stdout.write(msg + '\n')
        logs.append(msg)
    try:
        #print(id(logger))
        logger("info", "Having an initial check")
        nCommit_Last = getNCommit(owner, repo, branch)
        logger("info", f"{owner}/{repo} {branch} currently has {nCommit_Last} commits.")
        sleep(interval)
        while True:
            try:
                nCommit_Now = getNCommit(owner, repo, 
                                         branch)
                if nCommit_Now != nCommit_Last:
                    nNew = nCommit_Now - nCommit_Last
                    logger("info", nNew, 'new commit found!')
                    message = f'Hi,\nThere are {str(nNew)} new commits found on {owner}/{repo}/{branch}'
                    oath2Gmail(message, senderEmail, 
                               receiverEmail)
                logger("info", 
                       f"{owner}/{repo} {branch} currently has {nCommit_Now} commits.")
                nCommit_Last = nCommit_Now
                sleep(interval)
            except KeyboardInterrupt:
                break
    except Exception as e:
        logger("error", 'Error encountered: ' + str(e))