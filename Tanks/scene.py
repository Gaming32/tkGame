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
    def update(self):
        if self.parent.getdescriptor(scene.Sprite).within(sq1):
            print('Red Wins!')
            myscene.game.canvas.create_text(500, 500, text='Red Wins!')
            sq2.placement.vector = scene.Vector(23, 5)
            sq1.placement.vector = scene.Vector(2, 5)
        # self.parent.getdescriptor(scene.Sprite).within(sq2, 'RED')
    # def update(self):
    #     myscene.scale -= 1.5 * myscene.lastframelen
    #     self.speed    += myscene.lastframelen
class Mover2(Mover):
    speed = 7.5
    up    = 'W'
    down  = 'S'
    left  = 'A'
    right = 'D'
    # def update(self):
    #     self.speed += myscene.lastframelen
    #     if myscene.scale < 1:
    #         print('Green Wins!')
    #         myscene.scale = 50
    #         myscene.switchscene(myscene)
    # def update(self):
    #     # print(self.parent.getdescriptor(scene.Sprite).within(sq2), end='\r')
    #     self.parent.getdescriptor(scene.Sprite).within(sq2, 'GRN')
sq1 = scene.Square(myscene, vector=scene.Vector(2, 5),  color='green', shape=scene.Shapes.Oval)
sq1.adddescriptor(Mover2)
sq2 = scene.Square(myscene, vector=scene.Vector(23, 5), color='red',   scale=scene.Vector(2, 2))
sq2.adddescriptor(Mover1)

# def run(inst):
#     scene.init(inst)
#     #print(inst.canvas is scene.game.canvas)
#     sq1 = scene.Square(vector=scene.Vector(2, 2))
#     sq2 = scene.Square(vector=scene.Vector(4, 4), scale=scene.Vector(2, 2))
# #    sq2.adddescriptor(Mover)
#     scene.start()