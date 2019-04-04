#sq = (self.speed,self.speed,self.speed,self.speed)
import keyboard
import tkgame.scene as scene
myscene = scene.Scene(displayfps=True)
class Mover(scene.Behavior):
    def preupdate(self):
        if keyboard.is_pressed(self.right):
            self.parent.placement.vector.offset(self.speed * myscene.lastframelen, 0)
        if keyboard.is_pressed(self.left):
            self.parent.placement.vector.offset(-self.speed * myscene.lastframelen, 0)
        if keyboard.is_pressed(self.up):
            self.parent.placement.vector.offset(0, self.speed * myscene.lastframelen)
        if keyboard.is_pressed(self.down):
            self.parent.placement.vector.offset(0, -self.speed * myscene.lastframelen)
class Mover1(Mover):
    speed = 5
    up    = 'up arrow'
    down  = 'down arrow'
    left  = 'left arrow'
    right = 'right arrow'
class Mover2(Mover):
    speed = 7.5
    up    = 'W'
    down  = 'S'
    left  = 'A'
    right = 'D'
sq1 = scene.Square(myscene, vector=scene.Vector(2, 2), color='green', shape='circle')
sq1.adddescriptor(Mover2)
sq2 = scene.Square(myscene, vector=scene.Vector(4, 4), color='red',   scale=scene.Vector(2, 2))
sq2.adddescriptor(Mover1)

# def run(inst):
#     scene.init(inst)
#     #print(inst.canvas is scene.game.canvas)
#     sq1 = scene.Square(vector=scene.Vector(2, 2))
#     sq2 = scene.Square(vector=scene.Vector(4, 4), scale=scene.Vector(2, 2))
# #    sq2.adddescriptor(Mover)
#     scene.start()