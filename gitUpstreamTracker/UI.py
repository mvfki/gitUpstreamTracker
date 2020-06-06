# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 22:42:56 2020

@author: Yichen Wang
"""
from tkinter import Tk, Frame, Label, Entry, N, SE, SW, StringVar, Button, END
from tkinter import Toplevel, Spinbox, DISABLED, NORMAL, IntVar, Text, FLAT
from tkinter.font import Font
from infi.systray import SysTrayIcon
from bs4 import BeautifulSoup
from multiprocessing import Process, Manager, freeze_support
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import time, re
from sys import stdout

from gmail import oath2Gmail



EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
GMAIL_REGEX = re.compile(r"[^@]+@gmail.com")
COLORs = {'bg': '#19222d', 
          'frmLine': '#32414a', 
          'txt': '#f0f0f0',
          'selBg': '#1464a0',
          'dis': "#787878"}

# Status record variables used when hiding in the tray
# Here it applies the "pointer" feature of list and dict
# Don't overwrite these variables but set values by subscribing!
VALs = {'owner': None, 
        'repo': None,
        'branch': 'master',
        'sender': None,
        'receiver': None,
        'hour': 0,
        'min': 1}

RUNNING = [False] # Whether panel window is open
ui = []
PROC = []
SYSTRAY = []

class UI():
    def __init__(self, sysTrayIcon=None, vals=None):
        global RUNNING
        global ui
        RUNNING[0] = True
        ui.append(self)
        self.tk = Tk()
        self.vals = vals
        self.titleFont = Font(root=self.tk, family="Helvetica", size=15)
        self.labelFont = Font(root=self.tk, family="Helvetica", size=11)
        self.entryFont = Font(root=self.tk, family="Courier", size=10)
        self.stringVars = {}
        self.buildMainWindow()
        self.tk.focus_force()
        self.tk.protocol("WM_DELETE_WINDOW", self.hideToTray)
        try:
            getNCommit('mvfki', 'gitUpstreamTracker', 'master')
        except URLError:
            self.check_start_btn['state'] = DISABLED
            self.repoInfo_btn['state'] = DISABLED
            self.tk.geometry('400x550')
            self._setLabel(self.tk, 'Internet connection error\nPlease check and restart.', 
                           x=290, y=540)
        self.tk.mainloop()
    
    # Appearance building vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def buildMainWindow(self):
        logger("debug", "Building window.")
        self.tk.title("gitUpstreamTracker")
        self.tk.geometry('400x510')
        centerWindow(self.tk)
        self.tk["bg"] = COLORs['bg']
        self.tk.attributes("-alpha",0.95)
        self.addFrame_repoInfo()
        self.addFrame_senderInfo()
        self.addFrame_receiverInfo()
        self.addOperationPanel()
        
    def addFrame_repoInfo(self):
        self.repoInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=180, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self._setTitleLabel(self.repoInfo_frame, "GitHub Repository to Track")
        # Owner entry
        self._setLabel(self.repoInfo_frame, "Owner", 55)
        self.repoInfo_owner_entry = self._setEntry(self.repoInfo_frame, 
                                                   'owner', 55, 
                                                   self.vals['owner'], 
                                                   setFocus=True)
        # Repo entry
        self._setLabel(self.repoInfo_frame, "Repository", 85)
        self.repoInfo_repo_entry = self._setEntry(self.repoInfo_frame, 
                                                  'repo', 85, 
                                                  self.vals['repo'])
        # Branch entry
        self._setLabel(self.repoInfo_frame, "Branch", 115)
        self.repoInfo_branch_entry = self._setEntry(self.repoInfo_frame, 
                                                    'branch', 115, 
                                                    self.vals['branch'])
        # Button
        self.repoInfo_btn = Button(self.repoInfo_frame, relief=FLAT,
                                   text="Check Commit Number", 
                                   command=self.openCheckCommitWindow,
                                   bg=COLORs['frmLine'], fg=COLORs['txt'], 
                                   width=18, height=1, font=self.labelFont, 
                                   activebackground=COLORs['frmLine'], 
                                   activeforeground=COLORs['txt'])
        batchBindEvent([self.repoInfo_frame,
                        self.repoInfo_owner_entry, 
                        self.repoInfo_repo_entry,
                        self.repoInfo_branch_entry,
                        self.repoInfo_btn], 
                       effect=bindPressButtonEffect, 
                       target=self.repoInfo_btn, root=self.tk)
        self.repoInfo_btn.place(anchor=N, x=180, y=130)
        self.repoInfo_frame.pack(pady=20)
        
    def addFrame_senderInfo(self):
        self.senderInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=75, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self.senderInfo_frame.pack(pady=10)
        self._setTitleLabel(self.senderInfo_frame, "Sender Gmail")
        # Sender entry
        self._setLabel(self.senderInfo_frame, "Address", 55)
        self.senderInfo_entry = self._setEntry(self.senderInfo_frame, 
                                               'sender', 55, 
                                               self.vals['sender'])
        
    def addFrame_receiverInfo(self):
        self.receiverInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=75, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self.receiverInfo_frame.pack(pady=10)
        self._setTitleLabel(self.receiverInfo_frame, "Receiver Email")
        self._setLabel(self.receiverInfo_frame, 'Address', 55)
        self.receiverInfo_entry = self._setEntry(self.receiverInfo_frame, 
                                                 'receiver', 55,
                                                 self.vals['receiver'])
        
    def addOperationPanel(self):
        self.OP_frame = Frame(self.tk, bg=COLORs['bg'], width=360, height=35)
        self.OP_frame.pack()
        self._setLabel(self.OP_frame, 'Check Every', 25, 90)
        self.stringVars['hour'] = IntVar()
        self.stringVars['hour'].set(self.vals['hour'])
        self.freq_hour_spin = Spinbox(self.OP_frame, from_=0, to=24,
                                      textvariable=self.stringVars['hour'],
                                      width=2, bg=COLORs['bg'], 
                                      fg=COLORs['txt'],
                                      disabledbackground=COLORs['bg'],
                                      disabledforeground=COLORs['dis'])
        self.freq_hour_spin.place(anchor=SE, y=23,x=120)
        self._setLabel(self.OP_frame, 'h', 25, 135)
        self.stringVars['min'] = IntVar()
        self.stringVars['min'].set(self.vals['min'])
        self.freq_min_spin = Spinbox(self.OP_frame, from_=1, to=59,
                                      textvariable=self.stringVars['min'],
                                      width=2, bg=COLORs['bg'], 
                                      fg=COLORs['txt'],
                                      disabledbackground=COLORs['bg'],
                                      disabledforeground=COLORs['dis'])
        self.freq_min_spin.place(anchor=SE, y=23,x=165)
        self._setLabel(self.OP_frame, 'min', 25, 195)
        self.check_start_btn = Button(self.OP_frame, relief=FLAT, 
                                      text='Start', bg=COLORs['frmLine'],
                                      fg=COLORs['txt'], width=6, height=1,
                                      font=self.labelFont, 
                                      command=self.startLoop,
                                      activebackground=COLORs['frmLine'], 
                                      activeforeground=COLORs['txt'])
        batchBindEvent([self.freq_min_spin, 
                        self.freq_hour_spin,
                        self.check_start_btn], 
                       effect=bindPressButtonEffect, 
                       target=self.check_start_btn, root=self.tk)
        self.check_start_btn.place(anchor=SE, y=30, x=270)
        self.check_stop_btn = Button(self.OP_frame, relief=FLAT, 
                                      text='Stop', bg=COLORs['frmLine'],
                                      fg=COLORs['txt'], width=6, height=1,
                                      font=self.labelFont, state=DISABLED,
                                      activebackground=COLORs['frmLine'], 
                                      activeforeground=COLORs['txt'],
                                      command=self.stopLoop)
        self.check_stop_btn.place(anchor=SE, y=30, x=350)
        global PROC
        if len(PROC) == 1 and PROC[0].is_alive():
            self.repoInfo_owner_entry['state'] = DISABLED
            self.repoInfo_repo_entry['state'] = DISABLED
            self.repoInfo_branch_entry['state'] = DISABLED
            self.senderInfo_entry['state'] = DISABLED
            self.receiverInfo_entry['state'] = DISABLED
            self.check_start_btn['state'] = DISABLED
            self.freq_min_spin['state'] = DISABLED
            self.freq_hour_spin['state'] = DISABLED
            self.check_stop_btn['state'] = NORMAL
        elif len(PROC) == 0 and self.entryAllEntered():
            self.check_start_btn['state'] = NORMAL
            self.check_stop_btn['state'] = DISABLED
        elif len(PROC) == 0 and not self.entryAllEntered():
            self.check_start_btn['state'] = DISABLED
            self.check_stop_btn['state'] = DISABLED
        else:
            logger("error", "Process running abnormally when building the window")
            logger("error", f"len(PROC)=={len(PROC)}, PROC[0].is_alive()=={str(PROC[0].is_alive())}")
        self.window_hide = Button(self.tk, relief=FLAT,
                          text="Hide to Tray", 
                          command=self.hideToTray,
                          bg=COLORs['frmLine'], fg=COLORs['txt'], 
                          width=12, height=1, font=self.labelFont, 
                          activebackground=COLORs['frmLine'], 
                          activeforeground=COLORs['txt'])
        self.window_hide.place(anchor=N, x=120, y=460)
        self.window_quit = Button(self.tk, relief=FLAT,
                          text="Quit", 
                          command=SYSTRAY[0].shutdown,
                          bg=COLORs['frmLine'], fg=COLORs['txt'], 
                          width=12, height=1, font=self.labelFont, 
                          activebackground=COLORs['frmLine'], 
                          activeforeground=COLORs['txt'])
        self.window_quit.place(anchor=N, x=280, y=460)

    # Operating Functions vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def openCheckCommitWindow(self):
        owner, repo, branch = (self.stringVars['owner'].get().strip(), 
                               self.stringVars['repo'].get().strip(), 
                               self.stringVars['branch'].get().strip())
        if owner and repo and branch:
            directCheckUI(owner, repo, branch)
    
    def hideToTray(self):
        global VALs
        global RUNNING
        global ui
        VALs['owner'] = self.stringVars['owner'].get().strip()
        VALs['repo'] = self.stringVars['repo'].get().strip()
        VALs['branch'] = self.stringVars['branch'].get().strip()
        VALs['receiver'] = self.stringVars['receiver'].get().strip()
        VALs['sender'] = self.stringVars['sender'].get().strip()
        VALs['hour'] = self.stringVars['hour'].get()
        VALs['min'] = self.stringVars['min'].get()
        RUNNING[0] = False
        self.tk.destroy()
        del ui[0]

    def startLoop(self):
        global PROC
        logger("info", "Check button pressed")
        if self.entryAllEntered():
            self.check_start_btn['state'] = DISABLED
            self.repoInfo_owner_entry['state'] = DISABLED
            self.repoInfo_repo_entry['state'] = DISABLED
            self.repoInfo_branch_entry['state'] = DISABLED
            self.senderInfo_entry['state'] = DISABLED
            self.receiverInfo_entry['state'] = DISABLED
            self.freq_min_spin['state'] = DISABLED
            self.freq_hour_spin['state'] = DISABLED
            intervalSec = self.stringVars['hour'].get() * 60 * 60 + \
                          self.stringVars['min'].get() * 60
            try:
                getNCommit(self.stringVars['owner'].get().strip(), 
                           self.stringVars['repo'].get().strip(), 
                           self.stringVars['branch'].get().strip())
                logger("info", "Abled to run the process")
                PROC.append(Process(target=periodicalCatcher, 
                            args=(self.stringVars['owner'].get().strip(), 
                                  self.stringVars['repo'].get().strip(), 
                                  self.stringVars['sender'].get().strip(), 
                                  self.stringVars['receiver'].get().strip(),
                                  self.stringVars['branch'].get().strip(), 
                                  intervalSec, LOGS)))
                PROC[0].start()
                VALs['owner'] = self.stringVars['owner'].get().strip()
                VALs['repo'] = self.stringVars['repo'].get().strip()
                VALs['branch'] = self.stringVars['branch'].get().strip()
                VALs['receiver'] = self.stringVars['receiver'].get().strip()
                VALs['sender'] = self.stringVars['sender'].get().strip()
                VALs['hour'] = self.stringVars['hour'].get()
                VALs['min'] = self.stringVars['min'].get()
                time.sleep(1)
                self.check_stop_btn['state'] = NORMAL
            except Exception as e:
                logger("error", 'Error encountered: ' + str(e))
                self.check_stop_btn['state'] = DISABLED
                self.check_start_btn['state'] = NORMAL
                self.repoInfo_owner_entry['state'] = NORMAL
                self.repoInfo_repo_entry['state'] = NORMAL
                self.repoInfo_branch_entry['state'] = NORMAL
                self.senderInfo_entry['state'] = NORMAL
                self.receiverInfo_entry['state'] = NORMAL
                self.freq_min_spin['state'] = NORMAL
                self.freq_hour_spin['state'] = NORMAL


    def stopLoop(self):
        global PROC
        self.check_stop_btn['state'] = DISABLED
        if len(PROC) == 1 and PROC[0].is_alive():
            logger("info", "Stopping process normally")
            PROC[0].terminate()
            PROC[0].join()
            del PROC[0]
        elif len(PROC) == 1 and not PROC[0].is_alive():
            logger("warning", "Process is not alive. Stop anyway.")
            PROC[0].terminate()
            PROC[0].join()
            del PROC[0]
        elif len(PROC) > 1:
            logger("error", "Unknown number of process running. Stop them all.")
            for p in PROC:
                p.terminate()
                p.join()
            for i in range(len(PROC)):
                del PROC[0]
        time.sleep(1)
        self.check_start_btn['state'] = NORMAL
        self.repoInfo_owner_entry['state'] = NORMAL
        self.repoInfo_repo_entry['state'] = NORMAL
        self.repoInfo_branch_entry['state'] = NORMAL
        self.senderInfo_entry['state'] = NORMAL
        self.receiverInfo_entry['state'] = NORMAL
        logger("info", "Successfully stopped")

    def entryAllEntered(self):
        allArgs = [self.stringVars['owner'].get().strip(), 
                   self.stringVars['repo'].get().strip(), 
                   self.stringVars['sender'].get().strip(), 
                   self.stringVars['receiver'].get().strip(),
                   self.stringVars['branch'].get().strip()]
        if '' not in allArgs and None not in allArgs:
            if not GMAIL_REGEX.match(allArgs[2]) or \
               not EMAIL_REGEX.match(allArgs[3]):
                return False
            else:
                return True
        else:
            return False

    def entryEntered(self, *args):
        if self.entryAllEntered():
            self.check_start_btn['state'] = NORMAL
        else:
            self.check_start_btn['state'] = DISABLED

    # Theme setting for all kinds of widgets vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def _setTitleLabel(self, master, text):
        tl = Label(master, padx=5, text=text, bg=COLORs['bg'], 
                   font=self.titleFont, fg=COLORs['txt'])
        tl.place(anchor=N, x=180, y=-6)
        
    def _setLabel(self, master, text, y, x=110):
        l = Label(master, text=text, bg=COLORs['bg'], font=self.labelFont,
                  fg=COLORs['txt'])
        l.place(anchor=SE, x=x, y=y)

    def _setEntry(self, master, varName, y, value=None, setFocus=False):
        self.stringVars[varName] = StringVar()
        if value != None:
            self.stringVars[varName].set(value)
        self.stringVars[varName].trace("w", self.entryEntered)
        e = Entry(master, font=self.entryFont, bg=COLORs['bg'], bd=1, 
                  fg=COLORs['txt'], textvariable=self.stringVars[varName], 
                  highlightcolor=COLORs['frmLine'], 
                  selectbackground=COLORs['selBg'],
                  insertbackground=COLORs['txt'],
                  disabledbackground=COLORs['bg'],
                  disabledforeground=COLORs['dis'])
        e.place(anchor=SW, x=120, y=y, height=22, width=180)
        if setFocus:
            e.focus()
        
        return e
    
class directCheckUI():
    def __init__(self, owner, repo, branch):
        # calculation
        try:
            nCommit = getNCommit(owner, repo, branch)
            msg = f"Number of commit: {str(nCommit)}"
        except HTTPError:
            msg = "Given repository or branch not found"
        self.tk = Toplevel()
        self.tk.focus_set()
        self.tk.geometry('260x150')
        centerWindow(self.tk)
        self.tk["bg"] = COLORs['bg']
        self.tk.attributes("-alpha",0.95)
        # apearance
        Label(self.tk, text=f"{owner}/{repo}", bg=COLORs['bg'], 
              font=Font(root=self.tk, family="Helvetica", size=13), 
              fg=COLORs['txt']).place(anchor=N, x=130, y=15)
        Label(self.tk, text=branch, bg=COLORs['bg'], 
              font=Font(root=self.tk, family="Helvetica", size=11), 
              fg=COLORs['txt']).place(anchor=N, x=130, y=35)
        Label(self.tk, text=msg, bg=COLORs['bg'], 
              font=Font(root=self.tk, family="Helvetica", size=11), 
              fg=COLORs['txt']).place(anchor=N, x=130, y=65)
        self.btn = Button(self.tk, text="Close", 
                          command=(lambda: self.destroyWindow()),
                          bg=COLORs['frmLine'], fg=COLORs['txt'], 
                          relief=FLAT, width=5, height=1, 
                          font=Font(root=self.tk, family="Helvetica", 
                                    size=11), 
                          activebackground=COLORs['frmLine'], 
                          activeforeground=COLORs['txt'])
        batchBindEvent([self.tk, self.btn], effect=bindPressButtonEffect, 
                       target=self.btn, root=self.tk)
        self.btn.place(anchor=N, x=130, y=105)
        
    def destroyWindow(self):
        self.tk.destroy()

class statusBox():
    def __init__(self, systray):
        self.tk = Tk()
        self.tk.focus_set()
        self.tk.geometry('500x200-1-42')
        self.tk.overrideredirect(True)
        self.tk['bg'] = COLORs['bg']
        self.tk.attributes("-alpha",0.95)
        self.tk.bind("<FocusOut>", self.quit)
        self.refresh()
        self.refreshBtn = Button(self.tk, text='Refresh', relief=FLAT,
                                 bg=COLORs['frmLine'], fg=COLORs['txt'], 
                                 width=8, height=1, command=self.refresh,
                                 font = Font(root=self.tk, family="Helvetica", 
                                             size=11),
                                 activebackground=COLORs['frmLine'], 
                                 activeforeground=COLORs['txt'])
        self.refreshBtn.place(anchor="ne", x=480, y=10)
        self.tk.mainloop()

    def quit(self, event):
        self.tk.destroy()

    def refresh(self):
        global LOGS
        if len(PROC) == 1 and PROC[0].is_alive():
            l = f"Tracking {VALs['owner']}/{VALs['repo']} {VALs['branch']}"
            self.label = Label(self.tk, text=l, bg=COLORs['bg'], 
                               fg=COLORs['txt'], 
                               font=Font(root=self.tk, family="Helvetica", 
                                         size=11))
        else:
            self.label = Label(self.tk, text="Not running", bg=COLORs['bg'], 
                               fg=COLORs['txt'], 
                               font=Font(root=self.tk, family="Helvetica", 
                                         size=11))
        self.label.place(anchor="nw", x=20, y=12)
        self.textFrame = Text(self.tk, bg='#0f1823', width=65, height=8,
                              padx=5, pady=5, fg=COLORs['txt'], spacing1=2, 
                              spacing2=1, spacing3=2, wrap='word',
                              selectbackground=COLORs['selBg'], 
                              highlightthickness=0, relief=FLAT)
        self.textFrame.insert(END, '\n'.join(list(LOGS)))
        self.textFrame.see(END)
        self.textFrame.place(anchor=N, x=250,y=45)

def centerWindow(win):
    """
    centers a tkinter window
     win: tkinter.Tk object. The window to center
    @reference: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry(f'{width}x{height}+{x}+{y}')

def batchBindEvent(widgets, event=None, function=None, effect=None, target=None, root=None):
    if event == None and function == None and effect != None and target != None and root != None:
        for w in widgets:
            effect(w, target, root)
    elif event != None and function != None and effect == None and target == None and root == None:
        for w in widgets:
            w.bind(event, function)
                
def bindPressButtonEffect(widget, button, root):
    widget.bind("<KeyPress-Return>", (lambda event, button=button: pressButton(event, button)))
    widget.bind("<KeyRelease-Return>", (lambda event, root=root, button=button: releaseButton(root, event, button)))

def pressButton(event, button):
    button.config(relief = "sunken")

def releaseButton(root, event, button):
    button.config(relief = "raised")
    button.invoke()

def restoreUI(sysTrayIcon):
    global RUNNING
    global VALs
    global PROC
    if RUNNING[0] == False:
        UI(vals=VALs)

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
                      branch, interval, logs):
    def logger(level, *args):
        body =  f"{time.strftime('%Y-%m-%d %H:%M')} - {level.upper()} - "
        pieces = [str(i) for i in args]
        msg = body + ' '.join(pieces)
        stdout.write(msg + '\n')
        logs.append(msg)
    try:
        #print(id(logger))
        logger("info", "Having an initial check")
        nCommit_Last = getNCommit(owner, repo, branch)
        logger("info", f"{owner}/{repo} {branch} currently has {nCommit_Last} commits.")
        time.sleep(interval)
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
                time.sleep(interval)
            except KeyboardInterrupt:
                break
    except Exception as e:
        logger("error", 'Error encountered: ' + str(e))


def writeLogs():
    global LOGS
    logs = list(LOGS)
    logIO = open('gTU.log', 'a')
    logIO.write('\n'.join(logs) + '\n')
    logIO.close()

def on_quit_callback(systray):
    global PROC
    global ui
    global RUNNING
    global LOGS
    if len(PROC) == 1 and PROC[0].is_alive():
        PROC[0].terminate()
        PROC[0].join()
        del PROC[0]
    elif len(PROC) == 0:
        pass
    else:
        logger("warning", "Abnormal process running status on quit. Exitting anyway.")
    if RUNNING[0]:
        ui[0].tk.quit()
    writeLogs()

def logger(level, *args):
    global LOGS
    body =  f"{time.strftime('%Y-%m-%d %H:%M')} - {level.upper()} - "
    pieces = [str(i) for i in args]
    msg = body + ' '.join(pieces)
    stdout.write(msg + '\n')
    LOGS.append(msg)

def main():
    logger("info", "Thanks for using this script.")
    menu_options = (("Show panel", None, restoreUI),
                    ("Show status log", None, statusBox))
    SYSTRAY.append(SysTrayIcon(None, "gitUpstreamTracker", menu_options,
                               on_quit=on_quit_callback))
    SYSTRAY[0].start()
    UI(vals=VALs)

if __name__ == '__main__':  
    manager = Manager()
    LOGS = manager.list()
    main()

