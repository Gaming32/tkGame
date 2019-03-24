"""
Package for making games with tkinter;
The scene passed into the run function must be a namespace of some sort
which defines a run function which accepts an instance object which it must
immediately pass to tkgame.scene.init
Usage example (draws two squares on the screen):
    import tkgame.scene as scene
    class firstscene:
        def run(self, inst):
            scene.init(inst)
            sq1 = scene.Square(vector=scene.Vector(2, 2))
            sq2 = scene.Square(vector=scene.Vector(4, 4), scale=scene.Vector(2, 2))
            scene.start()
    import tkgame
    tkgame.run(firstscene())
"""

import sys
from tkinter import *

class GameInstance:
    """
    Starts the game
        scene:
            A namespace of some sort which defines a run function which accepts
            an instance object which it must immediately pass to tkgame.scene.init
        parent:
            The tkinter parent object in which to host the game canvas (generally
            is a Tk, Toplevel, Frame, Canvas, or Text)
            If not specified, it will default to its own window (and NOT to the default
            Tk)
        usewm:
            Boolean which specifies whether the GameInstance has control over the
            border, size, title, and icon of the parent
            If not specified, it will default to True
        fullscreen:

    """
    def _canvconf(self, event):
        self.canvas.config(width=event.width, height=event.height)
    def __init__(self,
            scene, parent=None, usewm=True, fullscreen=False, doloop=True,
            name='TkGame', icon=None, size=(500, 500)):
        self.parent = parent
        self.fullscreen = fullscreen
        self.name = name
        self.icon = icon
        if not self.parent: self.parent = Tk()
        if usewm:
            self.parent.title(name)
            self.parent.geometry('%dx%d+1000+300' % size)
            if self.fullscreen:
                #parent.attributes('-alpha', 0.0)
                self.parent.overrideredirect(True)
                #parent['highlightthickness'] = 0
                if sys.platform[:3] == 'win':
                    self.parent.state('zoomed')
                else:
                    self.parent.geometry('%sx%s+0+0' % (
                        self.parent.winfo_screenwidth(),
                        self.parent.winfo_screenheight()))
            if self.icon: self.parent.iconbitmap(file=icon)
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
        self.parent.after(0, lambda self=self: scene(self))
        if doloop: self.parent.mainloop()

def run(*args, **kwargs):
    """
    Same thing as GameInstance
    See GameInstance doc for help
    """
    return GameInstance(*args, **kwargs)