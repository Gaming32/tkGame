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
    def __init__(self, parent, color='black'):
        Descriptor.__init__(self, parent)
        self.color = color
    def preupdate(self):
        #print('deleting', end=' ')
        try:
            game.canvas.delete(self.obj)
            # for attr in ['width', 'height']: #game.canvas.keys()
            #     print(attr, '=>', game.canvas[attr])
        except AttributeError: pass
        self.obj = game.canvas.create_rectangle(
            self.parent.placement.vector.x * 50,
            int(game.canvas['height']) - self.parent.placement.vector.y * 50,
            (self.parent.placement.vector.x * 50) + self.parent.placement.scale.x * 50,
            (int(game.canvas['height']) - self.parent.placement.vector.y * 50) + self.parent.placement.scale.y * 50,
            fill=self.color
        )

class Behavior(Descriptor):
    def __init__(self, parent):
        Descriptor.__init__(self, parent)

class SceneObj:
    objs = []
    def __init__(self, name='SceneObj', vector=defaultvector, rotation=defaultrotation, scale=defaultscale):
        self.placement = Placement(vector, rotation, scale)
        self.placement.parent = self
        self.name = name
        self.objs = []
        SceneObj.objs.append(self)
    def getdescriptor(self, descriptor=Placement):
        name = descriptor.__name__.lower()
        return eval('self.' + name)
    def adddescriptor(self, descriptor):
        name = descriptor.__name__.lower()
        obj = 'self.' + name
        cmd = 'descriptor(parent=self)'
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
    def __init__(self, name='Square', vector=defaultvector, rotation=defaultrotation, scale=defaultscale):
        SceneObj.__init__(self, name, vector, rotation, scale)
        self.adddescriptor(Sprite)

def getobj(item):
    return SceneObj.objs[item]
def getallobjs(startlist=SceneObj.objs):
    for obj in startlist:
        yield obj
        for obj in getallobjs(obj.objs):
            yield obj

def init(inst):
    global game
    game = inst

def _update(attr):
    #print('updating', attr)
    for obj in getallobjs():
        for desc in obj.getalldescriptors():
            try: eval('desc.%s()' % attr)
            except AttributeError: pass
import time
lastframelen = 0
_currframelen = None
def _run():
    global _currframelen, lastframelen
    if _currframelen:
        lastframelen = (time.clock() - _currframelen) // 1000
    _currframelen = time.clock()
    _update('preupdate')
    game.parent.update()
    _update('update')
    game.parent.after(wait, _run)
def start(fps=30):
    global wait
    wait = 1000 // fps
    _run()