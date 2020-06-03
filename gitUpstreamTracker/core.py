# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:13:43 2020

@author: Yichen Wang
"""
from urllib.request import urlopen
import time
from gmail import oath2Gmail
from bs4 import BeautifulSoup

# Git commit detecting part
def makeURL(owner, repo, branch='master'):
    return f'https://github.com/{owner}/{repo}/tree/{branch}'

def getNCommit(owner, repo, branch='master'):
    '''Using a BS4 method to make this crawler process readable.'''
    url = makeURL(owner, repo, branch)
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html)
    allSpan = soup.findAll("span", {"class": ["num", "text-emphasized"]})
    nCommit = int(allSpan[0].text.strip().replace(',', ''))
    return nCommit

# Main looping part
def periodicalCatcher(owner, repo, senderEmail, receiverEmail, 
                      branch = 'master', interval = 3):
    nCommit_Last = getNCommit(owner, repo, branch)
    time.sleep(interval)
    while True:
        try:
            nCommit_Now = getNCommit(owner, repo, branch)
            if nCommit_Now != nCommit_Last:
                nNew = nCommit_Now - nCommit_Last
                print(nNew, 'new commit found!')
                message = f'Hi,\nThere are {str(nNew)} new commits found on {owner}/{repo}/{branch}'
            else:
                print(nCommit_Now)
                message = f'Hi,\nthere are currectly {str(nCommit_Now)} commits on {owner}/{repo}/{branch}'
            oath2Gmail(message, senderEmail, receiverEmail)
            # Currectly incompleted, dont want to run it forever.
            break
            nCommit_Last = nCommit_Now
            time.sleep(interval)
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopped")
            break    
        
if __name__ == "__main__":
    upstreamRepoOwner = 'compbiomed'
    upstreamRepoName = 'singleCellTK'
    upstreamRepoBranch = 'devel'
    receiver_email = 'wangych@bu.edu'
    sender_email = 'wangych0428@gmail.com'    
    periodicalCatcher(upstreamRepoOwner, upstreamRepoName, sender_email, 
                      receiver_email, upstreamRepoBranch)

