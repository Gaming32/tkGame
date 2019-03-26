from tkinter import *
from tkinter.filedialog import askopenfilename
import sys, zipfile
from python_tools.tkwidg import LabelFile
win = Tk()
LabelFile(win, redir_stdout=YES).pack(fill=X)
def help():
    pass
try: path = sys.argv[1]
except IndexError:
    path = askopenfilename(parent=win, defaultextension='.tkg', filetypes=[('tkGame Archive', '*.tkg')])
def init():
    print('Preparing...')
    tkg = zipfile.ZipFile(path, compression=zipfile.ZIP_DEFLATED)
    cachepath = 'cache/%%s/%s' % tkg.read('hash').decode('ascii')
    print('Extracting Runner...')
    tkg.extractall(cachepath % 'run')
    print('Extracting Comparer...')
    tkg.extractall(cachepath % 'compare')
win.after(0, init)
win.mainloop()