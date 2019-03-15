"""
Package for making games with tkinter
Usage example (draws two squares on the screen):
    import tkgame.scene as scene
    class firstscene:
        def run(inst):
            scene.init(inst)
            sq1 = scene.Square(vector=scene.Vector(2, 2))
            sq2 = scene.Square(vector=scene.Vector(4, 4), scale=scene.Vector(2, 2))
            scene.start()
    import tkgame
    tkgame.run(firstscene)
"""

import sys
from tkinter import *

class GameInstance:
    def _canvconf(self, event):
        self.canvas.config(width=event.width, height=event.height)
    def __init__(self,
            scene, parent=None, usewm=True, fullscreen=False, doloop=True,
            name='TkGame', icon=None, size=None):
        self.parent = parent
        self.fullscreen = fullscreen
        self.name = name
        self.icon = icon
        if not self.parent: self.parent = Tk()
        if usewm:
            self.parent.title(name)
            if self.fullscreen:
                #parent.attributes('-alpha', 0.0)
                self.parent.overrideredirect(True)
                #parent['highlightthickness'] = 0
                if sys.platform[:3] == 'win':
                    self.parent.state('zoomed')
            if self.icon: self.parent.iconbitmap(file=icon)
            if size: (self.parent['width'], self.parent['height']) = size
        self.canvas = Canvas(parent)
        self.canvas.bind('<Configure>', self._canvconf)
        self.canvas.pack(expand=YES, fill=BOTH)
        # for obj in dir(scene):
        #     obj = getattr(scene, obj)
        #     if isinstance(obj, tuple) and len(obj) == 4:
        #         obj = tuple(x * 10 for x in obj)
        #         canvas.create_rectangle(
        #             obj[0],
        #             int(canvas['height']) - obj[1],
        #             obj[0] + obj[2],
        #             int(canvas['height']) - obj[1] + obj[3],
        #             fill='black'
        #         )
        self.parent.after(0, lambda self=self: scene.run(self))
        if doloop: self.parent.mainloop()

def run(*pargs, **kwargs):
    "Run GameInstance.__init__"
    return GameInstance(*pargs, **kwargs)