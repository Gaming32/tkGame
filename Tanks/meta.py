from scene import go as SCENE
NAME = 'Tanks'
FULLSCREEN = True

if __name__ == '__main__':
    import tkgame
    tkgame.run(SCENE, name=NAME, fullscreen=FULLSCREEN)