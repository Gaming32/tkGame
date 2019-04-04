from scene import myscene as SCENE
NAME = 'Tanks'
FULLSCREEN = False

if __name__ == '__main__':
    import tkgame
    tkgame.run(SCENE, name=NAME, fullscreen=FULLSCREEN)