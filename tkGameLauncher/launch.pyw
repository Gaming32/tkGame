from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import sys, os, zipfile
from python_tools.tkwidg import LabelFile
import python_tools.path
import tkgame
win = Tk()
lbl = LabelFile(win, redir_stdout=YES, buffered=False)
lbl.pack(fill=X)
try: path = sys.argv[1]
except IndexError:
    path = askopenfilename(parent=win, defaultextension='.tkg', filetypes=[('tkGame Archive', '*.tkg')])

def init():
    print('Preparing...')
    tkg = zipfile.ZipFile(path, compression=zipfile.ZIP_DEFLATED)
    hashed = tkg.read('hash').decode('ascii')
    cachepath = 'cache/%%s/%s' % hashed
    print('Extracting...')
    #if os.path.exists(cachepath % 'run'):
    #   python_tools.path.deldir(cachepath % 'run')
    tkg.extractall(cachepath % 'run')
    os.remove(os.path.join(cachepath % 'run', 'mainfile'))
    os.remove(os.path.join(cachepath % 'run', 'hash'))
    savefile = ('cache/saves/%s' % hashed) + '.tgs'
    if os.path.isfile(savefile):
        print('Extracting Save at %s...' % savefile)
        tgs = zipfile.ZipFile(savefile, compression=zipfile.ZIP_DEFLATED)
        for finame in tgs.namelist():
            os.remove(os.path.join(cachepath % 'run'), finame)
        tgs.extractall(cachepath % 'run')
    print('Ready')
    lbl.pack_forget()
    go(cachepath % 'run', tkg)
def go(path, tkg):
    sys.path.insert(0, path)
    meta = __import__(os.path.splitext(tkg.read('mainfile').decode('utf-8'))[0])
    #del sys.path[0]
    kw = {}
    for item in dir(meta):
        if item[:2] != '__' and item[-2:] != '__' and item.isupper():
            kw[item.lower()] = getattr(meta, item)
    kw['parent'] = win
    kw['doloop'] = False
    tkgame.run(**kw)

def runapp():
    try: init()
    except:
        win.update()
        showerror('tkGame', 'Fatal Error:\n%s\n%s' % sys.exc_info()[:2], parent=win)
        win.quit()
win.after(0, runapp)
win.mainloop()