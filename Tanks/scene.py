#sq = (self.speed,self.speed,self.speed,self.speed)
import keyboard
import tkgame.scene as scene
myscene = scene.Scene(displayfps=True)
# myscene.camera.vector.offset(-5, -5)
# myscene.camera.scale.offset(-25, -25)
# class Mover1(Mover):
#     speed = 5
#     up    = 'up arrow'
#     down  = 'down arrow'
#     left  = 'left arrow'
#     right = 'right arrow'
class Handler(scene.Behavior):
    roundnum = 0
    def winner(self, text, player, loser):
        text += ' Wins!'
        # print('\n' + player)
        player.getdescriptor(scene.Text).text = 'Winner!'
        loser .getdescriptor(scene.Text).text = ''
        sq2.placement.vector = scene.Vector(23, 5)
        sq1.placement.vector = scene.Vector(2, 5)
        self.roundnum += (myscene.gametime - self.roundnum)
    # def preupdate(self):
    #     myscene.camera.vector.x = (sq1.placement.vector.x + sq2.placement.vector.x) / 2
    #     myscene.camera.vector.y = (sq1.placement.vector.y + sq2.placement.vector.y) / 2
    def update(self):
        self.parent.getdescriptor(scene.Text).text = (
            '%02i seconds remaining' % (30 - (myscene.gametime - self.roundnum)))
        # print('%02i' % (30 - (myscene.gametime - self.roundnum)), end='\r')
        if sq2.getdescriptor(scene.Sprite).within(sq1):
            self.winner('Red', sq2, sq1)
        elif myscene.gametime >= self.roundnum + 30:
            self.winner('Green', sq1, sq2)
        # self.parent.getdescriptor(scene.Sprite).within(sq2, 'RED')
    # def update(self):
    #     myscene.scale -= 1.5 * myscene.lastframelen
    #     self.speed    += myscene.lastframelen
# class Mover2(Mover):
#     speed = 7.5
#     up    = 'W'
#     down  = 'S'
#     left  = 'A'
#     right = 'D'
#     # def update(self):
#     #     self.speed += myscene.lastframelen
#     #     if myscene.scale < 1:
#     #         print('Green Wins!')
#     #         myscene.scale = 50
#     #         myscene.switchscene(myscene)
#     # def update(self):
#     #     # print(self.parent.getdescriptor(scene.Sprite).within(sq2), end='\r')
#     #     self.parent.getdescriptor(scene.Sprite).within(sq2, 'GRN')
from tkgame.descriptor.player import Mover
sq1 = scene.Square(myscene, vector=scene.Vector(2, 5),  color='green', shape=scene.Shapes.Oval)
sq1.adddescriptor(Mover, keys={'up':'W', 'down':'S', 'left':'A', 'right': 'D'}, speed=7.5)
sq1.adddescriptor(scene.Text)
# sq1.adddescriptor(scene.Text, text='Test')
# sq1.adddescriptor(Mover2)
sq2 = scene.Square(myscene, vector=scene.Vector(23, 5), color='red',   scale=scene.Vector(2, 2))
sq2.adddescriptor(Mover)
sq2.adddescriptor(scene.Text)
# sq2.getdescriptor(scene.Sprite).doalso = True
handle = scene.SceneObj(myscene, vector=scene.Vector(5, 6))
handle.adddescriptor(Handler)
handle.adddescriptor(scene.Text, text='30 seconds remaining')
# sq2.adddescriptor(Mover1)

# def run(inst):
#     scene.init(inst)
#     #print(inst.canvas is scene.game.canvas)
#     sq1 = scene.Square(vector=scene.Vector(2, 2))
#     sq2 = scene.Square(vector=scene.Vector(4, 4), scale=scene.Vector(2, 2))
# #    sq2.adddescriptor(Mover)
#     scene.start()