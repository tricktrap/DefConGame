#!/usr/bin/env python

""" Explosion.py
    Generalized class representing an explosion.
    
    In all my years as a programmer and a pyromaniac, I never dreamed I would
    one day write a code file with a name like "Explosion.py", let alone for
    points in a CS class. Life is good.
"""

import pygame, gameEngine

class Explosion(gameEngine.SuperSprite):
    def __init__(self,scene,radius,linger=5):
        gameEngine.SuperSprite.__init__(self,scene,location)
        
        self.setAngle(0)
        self.setSpeed(0)
        self.setPosition(location)
        self.setImage("explosions/explosion_01.bmp")
        tranColor = self.imageMaster.get_at((1,1))
        self.imageMaster.set_colorkey(tranColor)
        
        self.NUM_FRAMES = 10
        self.img = []
        self.loadPics()
        self.pic_index = 0  # What stage of the explosion
        self.linger = 1     # How long to linger per frame
        
        self.have_lingered = 0
        self.am_done = False
    
    def amDone(self):
        return self.am_done
    
    def checkEvents(self):
        self.have_lingered += 1
        if self.have_lingered == self.linger:
            self.pic_index += 1
            if self.pic_index == self.NUM_FRAMES:
                self.pic_index = 0
                self.am_done = True
            self.image = self.img[self.pic_index]
            
    def loadPics(self):
        for i in range(self.NUM_FRAMES):
            imgName = "explosions/explosion_0%d.bmp" % (i+1)
            tmpImg = pygame.image.load(imgName)
            tmpImg.convert()
            tranColor = tmpImg.get_at((0,0))
            tmpImg.set_colorkey(tranColor)
            self.img.append(tempImg)
            