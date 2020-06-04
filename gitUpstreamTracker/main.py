from infi.systray import SysTrayIcon
from UI import UI, RUNNING, VALs, ui
import subprocess, os, signal


def restoreUI(sysTrayIcon):
    global RUNNING
    global VALs
    if RUNNING[0] == False:
        UI(vals=VALs)

def on_quit_callback(systray):
    global proc1
    os.kill(proc1.pid, signal.Signals(1))
    if RUNNING[0]:
        global ui
        ui[0].tk.destroy()

if __name__ == '__main__':
    proc1 = subprocess.Popen("python process.py", shell = True)
    menu_options = (("Show panel", None, restoreUI),)
    systray = SysTrayIcon(None, "gitUpstreamTracker", menu_options,
                          on_quit=on_quit_callback)
    systray.start()
    UI(vals=VALs)