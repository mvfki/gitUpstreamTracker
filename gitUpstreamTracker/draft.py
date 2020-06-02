# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:13:43 2020

@author: Yichen Wang
"""
from urllib.request import urlopen
import time
from gmail import get_credentials, CreateMessage, SendMessage

# Git commit detecting part
def makeURL(owner, repo, branch='master'):
    return 'https://github.com/' + owner + '/' + repo + '/tree/' + branch

def getBody(url):
    html = urlopen(url).read().decode('utf-8')
    return html

def getNCommit(html):
    '''Using a straight forward way to read the HTML text and find the 
    number-string that is displayed on the web page'''
    s = html.split('<li class="commits">')[1].split('span')[1]
    nCommit = ''.join([i for i in s if i.isdigit()])
    nCommit = int(nCommit)
    return nCommit    

# Gmail sending part. See gmail.py
def oath2Gmail(message, sender, receiver):
    subject = 'gitUpstreamTracker Message'
    service = get_credentials()
    msg = CreateMessage(sender, receiver, subject, message)
    SendMessage(service, 'me', msg)

# Main looping part
def periodicalCatcher(owner, repo, senderEmail, receiverEmail, branch = 'master', interval = 3):
    url = makeURL(owner, repo, branch)
    nCommit_Last = getNCommit(getBody(url))
    time.sleep(interval)
    while True:
        try:
            html = getBody(url)
            nCommit_Now = getNCommit(html)
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
    periodicalCatcher(upstreamRepoOwner, upstreamRepoName, sender_email, receiver_email, 
                      upstreamRepoBranch)

