class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def offset(self, x, y):
        self.x += x
        self.y += y
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

class Descriptor:
    def __init__(self, parent):
        if type(self) == Descriptor:
            raise NotImplementedError
        self.parent = parent
defaultvector   = Vector()
defaultrotation = Rotation()
defaultscale    = Vector(1.0, 1.0)
class Placement(Descriptor):
    def __init__(self, vector=defaultvector, rotation=defaultrotation, scale=defaultscale):
        self.vector = vector
        self.rotation = rotation
        self.scale = scale
class Sprite(Descriptor):
    def __init__(self, parent, color='black', shape='rectangle'):
        Descriptor.__init__(self, parent)
        self.color = color
        self.cmd   = 'canv.create_' + shape
    def preupdate(self):
        #print('deleting', end=' ')
        canv = self.parent.scene.game.canvas
        if hasattr(self, 'obj'):
            canv.delete(self.obj)
            # for attr in ['width', 'height']: #canv.keys()
            #     print(attr, '=>', canv[attr])
        self.obj = eval(self.cmd)(
            self.parent.placement.vector.x * 50,
            int(canv['height']) - self.parent.placement.vector.y * 50,
            (self.parent.placement.vector.x * 50) + self.parent.placement.scale.x * 50,
            (int(canv['height']) - self.parent.placement.vector.y * 50) + self.parent.placement.scale.y * 50,
            fill=self.color
        )

class Behavior(Descriptor):
    def __init__(self, parent):
        Descriptor.__init__(self, parent)

class SceneObj:
    objs = []
    def __init__(self, scene, name='SceneObj', vector=defaultvector, rotation=defaultrotation, scale=defaultscale):
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
        color='black', shape='rectangle'):
        SceneObj.__init__(self, scene, name, vector, rotation, scale)
        self.adddescriptor(Sprite, color=color, shape=shape)

import time
class Scene:
    def __init__(self, fps=1000, displayfps=False):
        import sys
        self.displayfps = displayfps or ('--display-fps' in sys.argv)
        if fps: self.wait = 1000 // fps
        else:   self.wait = 0
    def getobj(self, item):
        return SceneObj.objs[item]
    def getallobjs(self, startlist=SceneObj.objs):
        for obj in startlist:
            yield obj
            for obj in self.getallobjs(obj.objs):
                yield obj
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
        self.game.parent.after(self.wait, self._run)
    def start(self, game):
        self.game = game
        if self.displayfps:
            self.fpslbl = self.game.canvas.create_text(0, 0, anchor='nw')
        self._run()
    def __call__(self, *args, **kwargs):
        self.start(*args, **kwargs)
