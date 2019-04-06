import keyboard
from .. import scene

class Mover(scene.Descriptor):
    """Basic moving Descriptor
    keys:
        A dict which has the keys up, down, left, and right
        which specify what keys move the player
        If not specified, it will default to
        dict(up    = 'up arrow',
             down  = 'down arrow',
             left  = 'left arrow',
             right = 'right arrow')
    speed:
        The speed at which the player will move in
        units per second
        If not specified, it will default to 5"""
    def __init__(self, keys=None, speed=5):
        if not keys:
            keys = dict(
                up    = 'up arrow',
                down  = 'down arrow',
                left  = 'left arrow',
                right = 'right arrow')
        self.keys = keys
        self.speed = speed
    def preupdate(self):
        if keyboard.is_pressed(self.keys['right']):
            self.parent.placement.vector.offset(self.speed * self.parent.scene.lastframelen, 0)
        if keyboard.is_pressed(self.keys['left']):
            self.parent.placement.vector.offset(-self.speed * self.parent.scene.lastframelen, 0)
        if keyboard.is_pressed(self.keys['up']):
            self.parent.placement.vector.offset(0, self.speed * self.parent.scene.lastframelen)
        if keyboard.is_pressed(self.keys['down']):
            self.parent.placement.vector.offset(0, -self.speed * self.parent.scene.lastframelen)