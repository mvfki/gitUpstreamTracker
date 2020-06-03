# gitUpstreamTracker

This script is itended to help those developers who fork an upstream 
repository and make pull requests. It has been a problem for me that I 
sometimes forget to merge upstream and therefore cause conflicts. The goal of 
this script is to track a (public) repository and inform the developers when 
new commits are updated.  
  
For now, I want to basically make this script a periodically web crawler and a 
conditional email sender.  
  
For further plan, I want to make this an desktop application, that can be 
hidden in the task bar and push a notice right when there is any changes or 
by periodical checks (latter should be simpler...)  

## To start

Although there are easy ways to send a email from Python, I prefer using an 
official, authorized and safe way to access personal email. So here I adopted 
Gmail OAuth2 method. As it is, of course you need to also have a Gmail 
account.  
  
### Step 1
You need these dependencies (run in shell/command line)
```{shell}
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 2
You will want to visit [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python).  
  
Click on the button "*Enable the Gmail API*" under "*Step 1*", and download the 
client configuration and save the file `credentials.json` to your working 
directory.  
  
During the first time you run this script, the browser will be open and you 
will login to your Google account and complete the authorization.  
  
As there will be a file `token.pickle` created to save the authorized 
credentials, you will no longer need to do this again in the future, as long 
as you don't modify this file.  

### Step 3
For now, modify email address as you need in `core.py` and run it.  

## Devel Note
Currently, the UI only contains basic appearance.

## Future plan
The git tracker part will be changed to standard API soon. I know "web crawler" style is stupid.


