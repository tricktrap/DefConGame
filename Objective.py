#!/usr/bin/env python

""" Objective.py
    
    A nice big target for the enemy missiles to aim at. Should sit squarely
    on the "ground" and not move.
    
"""
import pygame, gameEngine,random

class Objective(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self,scene)
        self.setImage("greenbase.bmp")
        tranColor = self.imageMaster.get_at((1,1))
        self.imageMaster.set_colorkey(tranColor)
        self.setSpeed(0)
        #self.setAngle(90)
        
        self.iff = 0
        self.generator = random.Random()
        
        self.reset()
        #self.setPosition((340,240))
    def reset(self):
        self.setPosition((self.generator.randrange(40, 600, 1), 459))
        