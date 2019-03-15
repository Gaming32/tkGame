#sq = (5,5,5,5)
import tkgame.scene as scene
def run(inst):
    scene.init(inst)
    #print(inst.canvas is scene.game.canvas)
    sq1 = scene.Square(vector=scene.Vector(2, 2))
    sq2 = scene.Square(vector=scene.Vector(4, 4), scale=scene.Vector(2, 2))
    scene.start()