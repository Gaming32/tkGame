import zipfile
import hashlib
from modulefinder import ModuleFinder
import sys
import os
from python_tools.path import bestrel
import pickle
printfaker = lambda *p, **kw: None

if __name__ == '__main__':
    trace = print
else:
    trace = printfaker

if '-v' in sys.argv and trace != printfaker:
    verbose = print
else:
    verbose = printfaker
#verbose = print

def maketkg(meta, reset_battery=False):
    trace('Initializing...')
    savepath = sys.path[0]
    sys.path[0] = os.path.dirname(meta)
    modfind = ModuleFinder()
    modfind.run_script(meta)
    mainmodfile = modfind.modules['__main__'].__file__
    mainmod = __import__(os.path.splitext(os.path.basename(mainmodfile))[0])
    verbose('\t__main__ globals =>', [globalname for globalname in dir(mainmod) if
        globalname[:2] != '__' and globalname[-2:] != '__'])
    try: gamename = mainmod.NAME
    except AttributeError: gamename = 'tkGame'
    tkgpath = os.path.join(os.path.dirname(mainmodfile), 'dist')
    if not os.path.isdir(tkgpath): os.mkdir(tkgpath)
    tkgpath = os.path.join(tkgpath, gamename + '.tkg')
    #if os.path.isfile(tkgpath): os.remove(tkgpath)
    #open(tkgpath, 'w+').close()
    tkg = zipfile.ZipFile(tkgpath, 'w', zipfile.ZIP_DEFLATED)
    hasher = hashlib.md5()
    cachedir = os.path.join(os.path.dirname(__file__), 'cache')
    hashfilename = os.path.join(cachedir, 'tkg_hash.bin')
    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)
    if not os.path.isfile(hashfilename):
        hashfile = open(hashfilename, 'wb+')
    else:
        hashfile = open(hashfilename, 'rb+')
    try:
        hashdict = pickle.load(hashfile)
    except EOFError:
        hashdict = {}
    trace('Copying Modules...')
    for (name, mod) in modfind.modules.items():
        modfile = mod.__file__
        if not modfile: continue
        path = os.path.basename(modfile)
        path = bestrel(modfile, *sys.path)
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
    if modfind.badmodules:
        trace('\t', 'Errors occured while importing modules:')
        for mod in modfind.badmodules:
            trace('\t \t', mod)
    trace('Hashing...')
    hashed = hasher.hexdigest()
    verbose('\t', 'hashed =>', hashed)
    verbose('\t', 'hashfile =>', hashfilename)
    # hashfile.seek(0)
    absmmfi = os.path.abspath(mainmodfile)
    if not absmmfi in hashdict or reset_battery:
        hashdict[absmmfi] = hashed
    tkg.writestr('hash', hashdict[absmmfi])
    pickle.dump(hashdict, hashfile)
    # where = hashfile.read().find(absmmfi.encode())
    # if where == -1:
    #     hashfile.seek(0, 2)
    #     hashfile.writelines([absmmfi.encode(), b'\n', hashed, b'\n'])
    #     tkg.writestr('hash', hashed)
    # else:
    #     if reset_battery:
    #         hashfile.seek(0)
    #     lines = hashfile.readlines()
    #     for (i, line) in enumerate(lines):
    #         if line == absmmfi:
    #             del lines[i], lines[i + 1]
    #     hashfile.truncate(0)
    #     for line in lines:
    #         hashfile.write(line + b'\n')
    #     hashfile.seek(where + len(absmmfi) + 1)
    #     tkg.writestr('hash', hashfile.read(16))
    trace('Finishing...')
    sys.path[0] = savepath
    hashfile.close()
    tkg.close()
    trace('Done')

if __name__ == '__main__':
    maketkg(sys.argv[1], '--reset-battery' in sys.argv)