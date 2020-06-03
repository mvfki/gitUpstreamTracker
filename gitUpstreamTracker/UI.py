# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 22:42:56 2020

@author: Yichen Wang
"""
from tkinter import Tk, Frame, Label, Entry, N, SE, SW, StringVar, Button
from tkinter.font import Font
from draft import makeURL, getBody, getNCommit

COLORs = {'bg': '#19222d', 'frmLine': '#32414a', 'txt': '#f0f0f0',
              'selBg': '#1464a0'}

class UI():
    def __init__(self):
        self.tk = Tk()
        self.titleFont = Font(root=self.tk, family="Helvetica", size=15)
        self.labelFont = Font(root=self.tk, family="Helvetica", size=11)
        self.entryFont = Font(root=self.tk, family="Courier", size=10)
        self.buildMainWindow()
        
        # TODOs
        self.tk.mainloop()
        
    def buildMainWindow(self):
        self.tk.title("gitUpstreamTracker")
        self.tk.geometry('400x450')
        _centerWindow(self.tk)
        self.tk["bg"] = COLORs['bg']
        self.tk.attributes("-alpha",0.95)
        self.addFrame_repoInfo()
        self.addFrame_senderInfo()
        self.addFrame_receiverInfo()
        self.addRunBtn()
        
    def addFrame_repoInfo(self):
        self.repoInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=135, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self.repoInfo_frame.pack(pady=20)
        self.repoInfo_title_label = Label(self.repoInfo_frame, padx=5,
                                          text="GitHub Repository to Track",
                                          bg=COLORs['bg'], 
                                          font=self.titleFont,
                                          fg=COLORs['txt'])
        self.repoInfo_title_label.place(anchor=N, x=180, y=-6)
        # Owner entry
        self.repoInfo_owner_label = Label(self.repoInfo_frame, 
                                          text='Owner', bg=COLORs['bg'], 
                                          font=self.labelFont,
                                          fg=COLORs['txt'])
        self.repoInfo_owner_label.place(anchor=SE, x=110, y=55)
        self.owner = StringVar()
        self.repoInfo_owner_entry = Entry(self.repoInfo_frame, 
                                          font=self.entryFont,
                                          bg=COLORs['bg'],
                                          bd=1, fg=COLORs['txt'], 
                                          textvariable=self.owner,
                                          highlightcolor=COLORs['frmLine'],
                                          selectbackground=COLORs['selBg'])
        self.repoInfo_owner_entry.place(anchor=SW, x=120, y=55, 
                                        height=22, width=180)
        # Repo entry
        self.repoInfo_repo_label = Label(self.repoInfo_frame, 
                                         text='Repository', bg=COLORs['bg'], 
                                         font=self.labelFont,
                                         fg=COLORs['txt'])
        self.repoInfo_repo_label.place(anchor=SE, x=110, y=85)
        self.repo = StringVar()
        self.repoInfo_repo_entry = Entry(self.repoInfo_frame, 
                                         font=self.entryFont,
                                         bg=COLORs['bg'], 
                                         bd=1, fg=COLORs['txt'], 
                                         textvariable=self.repo,
                                         highlightcolor=COLORs['frmLine'],
                                         selectbackground=COLORs['selBg'])
        self.repoInfo_repo_entry.place(anchor=SW, x=120, y=85, 
                                       height=22, width=180)
        # Branch entry
        self.repoInfo_branch_label = Label(self.repoInfo_frame, 
                                           text='Branch', bg=COLORs['bg'], 
                                           font=self.labelFont,
                                           fg=COLORs['txt'])
        self.repoInfo_branch_label.place(anchor=SE, x=110, y=115)
        self.branch = StringVar()
        self.branch.set('master')
        self.repoInfo_branch_entry = Entry(self.repoInfo_frame, 
                                           font=self.entryFont,
                                           bg=COLORs['bg'],
                                           bd=1, fg=COLORs['txt'], 
                                           textvariable=self.branch,
                                           highlightcolor=COLORs['frmLine'],
                                           selectbackground=COLORs['selBg'])
        self.repoInfo_branch_entry.place(anchor=SW, x=120, y=115, 
                                         height=22, width=180)
    
    def addFrame_senderInfo(self):
        self.senderInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=75, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self.senderInfo_frame.pack(pady=10)
        self.senderInfo_title_label = Label(self.senderInfo_frame, padx=5,
                                          text="Sender Gmail",
                                          bg=COLORs['bg'], 
                                          font=self.titleFont,
                                          fg=COLORs['txt'])
        self.senderInfo_title_label.place(anchor=N, x=180, y=-6)
        # Sender entry
        self.senderInfo_label = Label(self.senderInfo_frame, 
                                      text='Address', bg=COLORs['bg'], 
                                      font=self.labelFont,
                                      fg=COLORs['txt'])
        self.senderInfo_label.place(anchor=SE, x=110, y=55)
        self.sender = StringVar()
        self.senderInfo_entry = Entry(self.senderInfo_frame, 
                                      font=self.entryFont,
                                      bg=COLORs['bg'],
                                      bd=1, fg=COLORs['txt'], 
                                      textvariable=self.sender,
                                      highlightcolor=COLORs['frmLine'],
                                      selectbackground=COLORs['selBg'])
        self.senderInfo_entry.place(anchor=SW, x=120, y=55, 
                                    height=22, width=180)
        
    def addFrame_receiverInfo(self):
        self.receiverInfo_frame = Frame(self.tk, bg=COLORs['bg'], width=360, 
                                    height=75, relief='groove',
                                    highlightbackground=COLORs['frmLine'], 
                                    highlightthickness=1)
        self.receiverInfo_frame.pack(pady=10)
        self.receiverInfo_title_label = Label(self.receiverInfo_frame, padx=5,
                                          text="Receiver Email",
                                          bg=COLORs['bg'], 
                                          font=self.titleFont,
                                          fg=COLORs['txt'])
        self.receiverInfo_title_label.place(anchor=N, x=180, y=-6)
        # Sender entry
        self.receiverInfo_label = Label(self.receiverInfo_frame, 
                                      text='Address', bg=COLORs['bg'], 
                                      font=self.labelFont,
                                      fg=COLORs['txt'])
        self.receiverInfo_label.place(anchor=SE, x=110, y=55)
        self.receiver = StringVar()
        self.receiverInfo_entry = Entry(self.receiverInfo_frame, 
                                      font=self.entryFont,
                                      bg=COLORs['bg'],
                                      bd=1, fg=COLORs['txt'], 
                                      textvariable=self.receiver,
                                      highlightcolor=COLORs['frmLine'],
                                      selectbackground=COLORs['selBg'])
        self.receiverInfo_entry.place(anchor=SW, x=120, y=55, 
                                    height=22, width=180)
        
    def addRunBtn(self):
        self.btn = Button(self.tk, text="PrintInput", command=self.TakeInput)
        self.btn.place(anchor=N, x=200, y=380)
        
    def TakeInput(self):
        url = makeURL(self.owner.get(), self.repo.get(), self.branch.get())
        print("GitHub URL:", url)
        print("Sender Gmail:", self.sender.get())
        print("Receiver Email:", self.receiver.get())
        nCommit_Last = getNCommit(getBody(url))
        print("Number of Commit", nCommit_Last)
        
def _centerWindow(win):
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
    #win.deiconify()
    
if __name__ == '__main__':
    UI()