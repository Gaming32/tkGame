from copy import copy
from enum import Enum
class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def offset(self, x, y):
        self.x += x
        self.y += y
    def __str__(self):
        return '(%r,%r)' % (self.x, self.y)
    def __repr__(self):
        return '%s%s' % (self.__class__.__qualname__, self)
import math
class Rotation:
    def __init__(self):
        self.__degrees = 0
    @staticmethod
    def degrees(rot=0):
        obj = Rotation()
        obj.__degrees = rot
        return obj
    @staticmethod
    def radians(rot=0):
        obj = Rotation()
        obj.__degrees = rot * 180 / math.pi
        return obj
    
    def getdeg(self):
        return self.__degrees
    def getrad(self):
        return self.__degrees * math.pi / 180

    def __str__(self):
        return '%r°' % self.__degrees

class Descriptor:
    def __init__(self, parent):
        if type(self) == Descriptor:
            raise NotImplementedError
        self.parent = parent
defaultvector   = Vector()
defaultrotation = Rotation()
defaultscale    = Vector(1.0, 1.0)
class Placement(Descriptor):
    def __init__(self, vector=None, rotation=None, scale=None):
        if not vector:
            vector = copy(defaultvector)
        if not rotation:
            rotation = copy(defaultrotation)
        if not scale:
            scale = copy(defaultscale)
        self.vector = vector
        self.rotation = rotation
        self.scale = scale
class Shapes(Enum):
    Arc  = 'arc'
    Line = 'line'
    Oval = 'oval'
    Poly = 'polygon'
    Rect = 'rectangle'
class _Graphic(Descriptor):
    _poslogic = ("(place.vector.x - cam.vector.x) * cam.scale.x,"
            "int(canv['height']) - (place.vector.y + cam.vector.y) * cam.scale.y,"
            "(place.vector.x * (cam.scale.x - cam.vector.x)) + place.scale.x * cam.scale.x,"
            "(int(canv['height']) - (place.vector.y + cam.vector.y) * cam.scale.y) + place.scale.y * cam.scale.y")
    _poscut = 114
    def __init__(self, parent, color='black', style=Shapes.Rect.value):
        Descriptor.__init__(self, parent)
        self.kw = {}
        self.color = color
        self.cmd   = 'canv.create_' + style
    def preupdate(self):
        #print('deleting', end=' ')
        canv  = self.parent.scene.game.canvas
        place = self.parent.placement
        cam   = self.parent.scene.camera
        if hasattr(self, 'obj'):
            canv.delete(self.obj)
            # for attr in ['width', 'height']: #canv.keys()
            #     print(attr, '=>', canv[attr])
        tup = (eval(self._poslogic))
        # if self.doalso: print('%04.4f %04.4f %04.4f %04.4f' % tup, end='\r')
        self.obj = eval(self.cmd)(*tup, fill=self.color, **self.kw)
    def within(self, other):
        canv  = self.parent.scene.game.canvas
        place = self.parent.placement
        cam   = self.parent.scene.camera
        # print( '%s => %05.2f & %05.2f & %05.2f & %05.2f' % (d,
        #     place.vector.x * scale,
        #     int(canv['height']) - place.vector.y * scale,
        #     (place.vector.x * scale) + place.scale.x * scale,
        #     (int(canv['height']) - place.vector.y * scale) + place.scale.y * scale
        # ))
        tup = (eval(self._poslogic))
        sprites = canv.find_overlapping(*tup)
        obj = other.getdescriptor(self.__class__).obj
        #print(desc, sprites, end='\r')
        return (obj in sprites)
    def __contains__(self, other):
        return self.__class__.within(self, other)
class Sprite(_Graphic):
    def __init__(self, parent, color='black', shape=Shapes.Rect):
        _Graphic.__init__(self, parent, color, shape.value)
class Text(_Graphic):
    def __init__(self, parent, text='', color='black'):
        _Graphic.__init__(self, parent, color, 'text')
        self._poslogic = self._poslogic[:self._poscut]
        self.kw['text'] = text
    def __setattr__(self, attr, value):
        if attr == 'text':
            self.kw['text'] = value
        else: object.__setattr__(self, attr, value)

class Behavior(Descriptor):
    def __init__(self, parent):
        Descriptor.__init__(self, parent)

class SceneObj:
    objs = []
    def __init__(self, scene, name='SceneObj', vector=None, rotation=None, scale=None):
        if not vector:
            vector = copy(defaultvector)
        if not rotation:
            rotation = copy(defaultrotation)
        if not scale:
            scale = copy(defaultscale)
        self.scene = scene
        self.placement = Placement(vector, rotation, scale)
        self.placement.parent = self
        self.name = name
        self.objs = []
        SceneObj.objs.append(self)
    def getdescriptor(self, descriptor=Placement):
        name = descriptor.__name__.lower()
        return eval('self.' + name)
    def adddescriptor(self, descriptor, **kw):
        name = descriptor.__name__.lower()
        obj = 'self.' + name
        cmd = 'descriptor(parent=self, **kw)'
        istype = issubclass(descriptor, Descriptor)
        ishere = hasattr(self, name)
        if istype and not ishere:
            exec(obj + ' = ' + cmd)
        elif not istype:
            raise TypeError('descriptor %s must be a descriptor' % name)
        else:
            raise ValueError('descriptor %s already on object %s' % (name, self.name))
    def getalldescriptors(self):
        for obj in dir(self):
            if issubclass(type(eval('self.%s' % obj)), Descriptor):
                yield self.__dict__[obj]
    def getchild(self, child):
        return self.objs[child]
    def __getitem__(self, child):
        self.getchild(child)
class Square(SceneObj):
    def __init__(self, scene, name='Square',
        vector=defaultvector, rotation=defaultrotation, scale=defaultscale,
        color='black', shape=Shapes.Rect):
        SceneObj.__init__(self, scene, name, vector, rotation, scale)
        self.adddescriptor(Sprite, color=color, shape=shape)

import time
class Scene:
    def __init__(self, scale=50, fps=1000, displayfps=False):
        self.scale = scale
        import sys
        self.displayfps = displayfps or ('--display-fps' in sys.argv)
        if fps: self.wait = 1000 // fps
        else:   self.wait = 0
        self.camera = Placement(scale=Vector(50, 50))
    def getobj(self, item):
        return SceneObj.objs[item]
    def getallobjs(self, startlist=SceneObj.objs):
        for obj in startlist:
            yield obj
            for obj in self.getallobjs(obj.objs):
                yield obj
    def quit(self):
        self.game.canvas.destroy()
    def _switchscene(self, scene):
        self.game.parent.after_cancel(self._next)
        self.game._startscene(scene)
    def  switchscene(self, scene):
        self.game.parent.after(0, lambda scene=scene: self._switchscene(scene))
    def _update(self, attr):
        #print('updating', attr)
        for obj in self.getallobjs():
            for desc in obj.getalldescriptors():
                try: eval('desc.%s()' % attr)
                except AttributeError: pass
                    # import traceback
                    # traceback.print_exc()
    lastframelen = 0
    _currframelen = None
    def _run(self):
        if self._currframelen:
            self.lastframelen = time.clock() - self._currframelen
            if self.displayfps:
                self.game.canvas.itemconfig(self.fpslbl, text=('fps => %.2f' % (1 / self.lastframelen)))
        self._currframelen = time.clock()
        self._update('preupdate')
        self.game.parent.update()
        self._update('update')
        self._next = self.game.parent.after(self.wait, self._run)
    def start(self, game):
        self.game = game
        if self.displayfps:
            self.fpslbl = self.game.canvas.create_text(0, 0, anchor='nw')
        self._run()
    def __call__(self, *args, **kwargs):
        self.start(*args, **kwargs)
    def __getattr__(self, attr):
        if attr == 'gametime':
            if self._currframelen:
                return self._currframelen
            else: raise ValueError('scene %r not initialized' % self)
        else: raise AttributeError('instance of %s has no attribute %s' % (self.__class__.__qualname__, attr))