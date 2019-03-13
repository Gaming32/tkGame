class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
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
    def __init__(self):
        if type(self) == Descriptor:
            raise NotImplementedError
defaultvector   = Vector()
defaultrotation = Rotation()
defaultscale    = Vector(1.0, 1.0)
class ObjPlacement(Descriptor):
    def __init__(self, vector=defaultvector, rotation=defaultrotation, scale=defaultscale):
        self.vector = vector
        self.rotation = rotation
        self.scale = scale

class SceneObj:
    def __init__(self, name='SceneObj', vector=defaultvector, rotation=defaultrotation, scale=defaultscale):
        self.placement = ObjPlacement(vector, rotation, scale)
        self.name = name
    def getdescriptor(self, descriptor='placement'):
        return eval('self.' + descriptor)
    def __getitem__(self, descriptor):
        return self.getdescriptor(descriptor)
    def adddescriptor(self, descriptor):
        name = descriptor.__name__.capitalize()
        obj = 'self.' + name
        cmd = 'descriptor()'
        istype = isinstance(descriptor, Descriptor)
        ishere = hasattr(self, name)
        if istype and not ishere:
            eval(obj + ' = ' + cmd)
        elif not istype:
            raise TypeError('descriptor %s must be a descriptor' % name)
        else:
            raise ValueError('descriptor %s already on object %s' % (name, self.name))