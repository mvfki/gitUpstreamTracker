# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 22:42:56 2020

@author: Yichen Wang
"""
from tkinter import Tk, Frame, Label, Entry, N, SE, SW, StringVar, Button, FLAT
from tkinter import Toplevel
from tkinter.font import Font
from core import getNCommit
from urllib.error import HTTPError

COLORs = {'bg': '#19222d', 
          'frmLine': '#32414a', 
          'txt': '#f0f0f0',
          'selBg': '#1464a0'}

class UI():
    def __init__(self):
        self.tk = Tk()
        
        self.titleFont = Font(root=self.tk, family="Helvetica", size=15)
        self.labelFont = Font(root=self.tk, family="Helvetica", size=11)
        self.entryFont = Font(root=self.tk, family="Courier", size=10)
        self.stringVars = {}
        self.buildMainWindow()
        self.tk.focus_force()
        # TODOs
        self.tk.mainloop()
    
    # Appearance building vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def buildMainWindow(self):
        self.tk.title("gitUpstreamTracker")
        self.tk.geometry('400x450')
        centerWindow(self.tk)
        self.tk["bg"] = COLORs['bg']
        self.tk.attributes("-alpha",0.95)
        self.addFrame_repoInfo()
        self.addFrame_senderInfo()
        self.addFrame_receiverInfo()
        #self.addRunBtn()
        
    def addFrame_repoInfo(self):
        self.repoInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=190, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self._setTitleLabel(self.repoInfo_frame, "GitHub Repository to Track")
        # Owner entry
        self._setLabel(self.repoInfo_frame, "Owner", 55)
        self.repoInfo_owner_entry = self._setEntry(self.repoInfo_frame, 
                                                   'owner', 55, setFocus=True,
                                                   Return=True)
        # Repo entry
        self._setLabel(self.repoInfo_frame, "Repository", 85)
        self.repoInfo_repo_entry = self._setEntry(self.repoInfo_frame, 
                                                  'repo', 85, Return=True)
        # Branch entry
        self._setLabel(self.repoInfo_frame, "Branch", 115)
        self.repoInfo_branch_entry = self._setEntry(self.repoInfo_frame, 
                                                    'branch', 115, 'master',
                                                    Return=True)
        # Button
        self.repoInfo_btn = Button(self.repoInfo_frame, relief=FLAT,
                                   text="Check Commit Number", 
                                   command=self.openCheckCommitWindow,
                                   bg=COLORs['frmLine'], fg=COLORs['txt'], 
                                   width=20, height=2, font=self.labelFont, 
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
        self._setEntry(self.senderInfo_frame, 'sender', 55)
        
    def addFrame_receiverInfo(self):
        self.receiverInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=75, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self.receiverInfo_frame.pack(pady=10)
        self._setTitleLabel(self.receiverInfo_frame, "Receiver Email")
        self._setLabel(self.receiverInfo_frame, 'Address', 55)
        self._setEntry(self.receiverInfo_frame, 'receiver', 55)

    # Operating Functions vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def openCheckCommitWindow(self):
        owner, repo, branch = (self.stringVars['owner'].get().strip(), 
                               self.stringVars['repo'].get().strip(), 
                               self.stringVars['branch'].get().strip())
        if owner and repo and branch:
            directCheckUI(owner, repo, branch)
    
    # Theme setting for all kinds of widgets vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def _setTitleLabel(self, master, text):
        tl = Label(master, padx=5, text=text, bg=COLORs['bg'], 
                   font=self.titleFont, fg=COLORs['txt'])
        tl.place(anchor=N, x=180, y=-6)
        
    def _setLabel(self, master, text, y):
        l = Label(master, text=text, bg=COLORs['bg'], font=self.labelFont,
                  fg=COLORs['txt'])
        l.place(anchor=SE, x=110, y=y)

    def _setEntry(self, master, varName, y, value=None, setFocus=False,
                  Return=False):
        self.stringVars[varName] = StringVar()
        if value != None:
            self.stringVars[varName].set(value)
        e = Entry(master, font=self.entryFont, bg=COLORs['bg'], bd=1, 
                  fg=COLORs['txt'], textvariable=self.stringVars[varName], 
                  highlightcolor=COLORs['frmLine'], 
                  selectbackground=COLORs['selBg'],
                  insertbackground=COLORs['txt'])
        e.place(anchor=SW, x=120, y=y, height=22, width=180)
        if setFocus:
            e.focus()
        if Return:
            return e
    
class directCheckUI():
    def __init__(self, owner, repo, branch):
        # calculation
        try:
            nCommit = getNCommit(owner, repo, branch)
            msg = f"Number of commit: {str(nCommit)}"
        except HTTPError:
            msg = "Given repository or branch not found"
        #else:
        #    msg = "Other error"
        # main subwindow
        self.tk = Toplevel()
        self.tk.focus_set()
        self.tk.geometry('260x150')
        centerWindow(self.tk)
        self.tk["bg"] = COLORs['bg']
        self.tk.attributes("-alpha",0.95)
        # apearance
        #labelFont = Font(root=self.tk, family="Helvetica", size=15)
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
                          bg=COLORs['frmLine'], fg=COLORs['txt'], relief=FLAT,
                          width=5, height=1, 
                          font=Font(root=self.tk, family="Helvetica", size=11), 
                          activebackground=COLORs['frmLine'], 
                          activeforeground=COLORs['txt'])
        batchBindEvent([self.tk, self.btn], effect=bindPressButtonEffect, 
                       target=self.btn, root=self.tk)
        self.btn.place(anchor=N, x=130, y=105)
        
    def destroyWindow(self):
        self.tk.destroy()
    
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
    root.update_idletasks()
    root.after(50)
    button.config(relief = "raised")
    button.invoke()

if __name__ == '__main__':
    UI()