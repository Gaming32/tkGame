import zipfile
import hashlib
from modulefinder import ModuleFinder
import sys
import os

def maketkg(meta):
    modfind = ModuleFinder()
    modfind.run_script(meta)
    try: gamename = modfind.modules['__main__'].NAME
    except AttributeError: gamename = 'tkGame'
    tkgpath = os.path.join(os.path.split(meta)[0], 'dist')
    if not os.path.isdir(tkgpath): os.mkdir(tkgpath)
    tkgpath = os.path.join(tkgpath, gamename + '.tkg')
    #if os.path.isfile(tkgpath): os.remove(tkgpath)
    #open(tkgpath, 'w+').close()
    tkg = zipfile.ZipFile(tkgpath, 'w')
    for (name, mod) in modfind.modules.items():
        modfile = mod.__file__
        if not modfile: continue
        path = os.path.basename(modfile)
        for fol in sys.path:
            testpath = os.path.relpath(modfile, fol)
            if not '..' in testpath:
                path = testpath
                break
        print(name, '=>', path)
        if name == '__main__':
            tkg.writestr('mainfile', path)
        #if '__pycache__' in modfile:
        #    path = os.path.join('__pycache__', path)
        tkg.write(modfile, path)

if __name__ == '__main__':
    maketkg('Tanks/meta.py')