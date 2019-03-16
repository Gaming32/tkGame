#sq = (5,5,5,5)
#import keyboard
import tkgame.scene as scene
# class Mover(scene.Behavior):
#     def update(self):
#         if keyboard.is_pressed('right'):
#             self.parent.placement.vector.offset(5 * scene.lastframelen, 0)
#         elif keyboard.is_pressed('left'):
#             self.parent.placement.vector.offset(-5 * scene.lastframelen, 0)
#         elif keyboard.is_pressed('up'):
#             self.parent.placement.vector.offset(0, 5 * scene.lastframelen)
#         elif keyboard.is_pressed('down'):
#             self.parent.placement.vector.offset(0, -5 * scene.lastframelen)
def run(inst):
    scene.init(inst)
    #print(inst.canvas is scene.game.canvas)
    sq1 = scene.Square(vector=scene.Vector(2, 2))
    sq2 = scene.Square(vector=scene.Vector(4, 4), scale=scene.Vector(2, 2))
#    sq2.adddescriptor(Mover)
    scene.start()