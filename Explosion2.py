#!/usr/bin/env python

""" Explosion2.py    
    This sprite is actually a utility one that I will swap out at a given location
    for a sprite (or two) that needs to explode.
"""

import pygame, gameEngine


class Explosion(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self,scene)

        # When out of bounds, should be hidden (off stage)

        self.setBoundAction(self.HIDE)

        # Initialize animation
        self.WAITING = 0
        self.EXPLODING = 1

        self.loadImages()

        self.frame = 0
        self.delay = 2
        self.pause = 0

        # NOTE: This is DIFFERENT than the state engine
        # that is built in. NOT A MISTAKE.
        self.state = self.WAITING

        self.setPosition((-30,-30))
        #self.explodeAt((320,240))
        # initialize sound engine here

    def running(self):
        return self.state == self.EXPLODING
    def complete(self):
        return self.state == self.WAITING

    def explodeAt(self,location):
        self.state = self.EXPLODING

        # Would probably play sound here
        self.setPosition(location)

    def checkEvents(self):
        if self.state == self.WAITING:
            self.setPosition((-30, -30))
            #self.image = self.imgList[0]
            self.imageMaster = self.imgList[12]
        elif self.state == self.EXPLODING:
            #print "exploding..." + str(self.frame)
            self.pause += 1
            if self.pause > self.delay:
                # reset pause and advance animation
                self.pause = 0
                self.frame += 1
                if self.frame >= len(self.imgList):
                    self.frame = 0
                    self.state = self.WAITING
                    self.imageMaster = self.imgList[12]
                else:
                    self.imageMaster = self.imgList[self.frame]
        else:
            pass

    #def update(self):
    #
    #    # Pass control back to super class update method
    #    gameEngine.SuperSprite.update(self)
    #
    def loadImages(self):
        """ Yes, it's the same loadImages that Andy used in his
            chopper game, but updated to work with the game
            library, and specific to explosions.

            TODO:   Make general
                    Don't rely on internals of GameLib
        """
        imgMaster = pygame.image.load("explosions.gif")

        imgMaster = imgMaster.convert()
        #print "(%d,%d)" % imgMaster.get_size()
        self.imgList = []

        imgSize = (64, 64)

        offset = []
        for y in range(0, 256, 64):
            for x in range(0, 256, 64):
                offset.append((x,y))
        #        print "x: " + str(x) + "\ty: " + str(y)

        #print "Tiles: " + str(len(offset))
        for i in range(13):
            tmpImg = pygame.Surface(imgSize)
            #print "(%d,%d)" % (offset[i][0], offset[i][1])
            tmpImg.blit(imgMaster, (0,0),
                        (offset[i],imgSize))
            #tmpImg = tmpImg.convert()
            #transColor = tmpImg.get_at((1,1))
            #print "(%d,%d,%d)" % (transColor[0],transColor[1],transColor[2])
            #tmpImg.set_colorkey(transColor)
            tmpImg.set_colorkey((0x00, 0x00,0x00))
            self.imgList.append(tmpImg)
