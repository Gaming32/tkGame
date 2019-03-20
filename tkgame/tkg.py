import zipfile
import hashlib
from modulefinder import ModuleFinder
import sys
import os
from python_tools.path import bestrel
printfaker = lambda *p, **kw: None

if __name__ == '__main__':
    trace = print
else:
    trace = printfaker

if '-v' in sys.argv and trace != printfaker:
    verbose = print
else:
    verbose = printfaker
verbose = print

def maketkg(meta):
    trace('Initializing...')
    modfind = ModuleFinder()
    modfind.run_script(meta)
    try: gamename = modfind.modules['__main__'].NAME
    except AttributeError: gamename = 'tkGame'
    tkgpath = os.path.join(os.path.split(meta)[0], 'dist')
    if not os.path.isdir(tkgpath): os.mkdir(tkgpath)
    tkgpath = os.path.join(tkgpath, gamename + '.tkg')
    #if os.path.isfile(tkgpath): os.remove(tkgpath)
    #open(tkgpath, 'w+').close()
    tkg = zipfile.ZipFile(tkgpath, 'w', zipfile.ZIP_DEFLATED)
    hasher = hashlib.md5()
    trace('Copying Modules...')
    for (name, mod) in modfind.modules.items():
        modfile = mod.__file__
        if not modfile: continue
        path = os.path.basename(modfile)
        path = bestrel(modfile, os.path.dirname(modfind.modules['__main__'].__file__), *sys.path[1:])
        # for fol in sys.path:
        #     testpath = os.path.relpath(modfile, fol)
        #     if not '..' in testpath:
        #         path = testpath
        #         break
        verbose('\t', name, '=>', path)
        if name == '__main__':
            tkg.writestr('mainfile', path)
        #if '__pycache__' in modfile:
        #    path = os.path.join('__pycache__', path)
        hasher.update(open(modfile, 'rb').read())
        tkg.write(modfile, path)
    trace('Hashing...')
    tkg.writestr('hash', hasher.digest())
    trace('Done')

if __name__ == '__main__':
    maketkg('Tanks/meta.py')