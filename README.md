# gitUpstreamTracker

> Well, one day I suddenly found by simply pressing the "Watch" button at the top right you can easily be noticed by GitHub system. This tool is not useful at all. Let's say, this is a nice practice of Python UI and Gmail API for myself.

## Initial intention

This script is intended to help those developers who fork an upstream 
repository and make pull requests. It has been a problem for me that I 
sometimes forget to merge upstream and therefore cause conflicts. The goal of 
this script is to track a (public) repository and inform the developers when 
new commits are updated.  
  
For now, I want to basically make this script a background periodical web crawler and a 
conditional email sender.  
  
Now the UI feature is basically useable, which can be hidden in the background.

## To start

First of all, as I really love the hide-to-tray UI feature, which only works on Windows OS, 
only Windows is supported (for now?).

Although there are easy ways to send an email from Python, I prefer using an 
official, authorized and safe way to access personal email. So here I adopted 
Gmail OAuth2 method. As it is, of course you need to also have a Gmail 
account.  
  
### Step 1
You need these dependencies (run in command line/IPython IDLE)
```{shell}
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Other necessary dependencies includes: `urllib beautifulsoup4 tkinter email`, which you may already have in your environment.  
  
> Be sure to check the environment you are using. e.g. If they are installed from IPython IDLE, it is usually written into Anaconda environment as default. If you encounter an `ImportError` from other platforms, make sure to run with conda activated.

### Step 2
You will want to visit [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python).  
  
Click on the button "*Enable the Gmail API*" under "*Step 1*", and download the 
client configuration and save the file `credentials.json` to your working 
directory. And then you can start to try out the `core.py` script.  
  
During the first time you run it, the browser will be open and you 
will login to your Google account and complete the authorization.  
  
As there will be a file `token.pickle` created to save the authorized 
credentials, you will no longer need to do this again in the future, as long 
as you don't modify this file.  

### Step 3
For now, directly run:
```{shell}
$ python UI.py
```
Make sure all the credential files and the other utilization modules are under the same working directory and Python environment.

## Devel Note
- Now Basic UI function is done, yet polish needed.  
- For compiling to executable
```
cd gitUpstreamTracker
pyinstaller -F UI.spec
```
However, the compiled executable is still having some problem running the background process :(
