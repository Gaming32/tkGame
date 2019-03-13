from tkinter import *

def run(scene, name='TkGame', icon=None, size=None):
    win = Tk()
    win.title(name)
    if icon: win.iconbitmap(BitmapImage(file=icon))
    if size: (win['width'], win['height']) = size
    canvas = Canvas(win)
    canvas.pack(expand=YES, fill=BOTH)
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
    scene.canvas = canvas
    scene.run()
    win.mainloop()