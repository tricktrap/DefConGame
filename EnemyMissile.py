#!/usr/bin/env python

import pygame, gameEngine,random

import Missile

class EnemyMissile(Missile.Missile):
    def __init__(self,scene,initpos,initvel,resetposition):
        Missile.Missile.__init__(self,scene,initpos,initvel)
        
        self.resetposition = resetposition
        self.iff = 1
        self.generator = random.Random()
        
    def run_guidance_package(self):
        if (not self.target):
            return
        else:
            degrees = self.RelAngleToTarget()
            self.adjust(degrees)
            self.thrust(True)
    
    def reset(self):
        
        reset_x = self.generator.choice([1, 639])
        reset_y = self.generator.randrange(1, 240, 1)
        
        self.setPosition((reset_x,reset_y))
        
        self.resetExplosives()
        reset_v_x = 1
        if reset_x < 320:
            reset_v_x = 1
        else:
            reset_v_x = -1
        
        self.setComponents((reset_v_x, 0))