#!/usr/bin/env python

import pygame, gameEngine

import Missile

class PlayerMissile(Missile.Missile):
    def __init__(self,scene,initpos,initvel,resetposition,manual=True):
        Missile.Missile.__init__(self,scene,initpos,initvel)
        self.MAX_TURN_PER_CYCLE=20
        self.counter = 10
        self.iff = 2
        self.resetposition = resetposition
        self.manual = manual
    def run_guidance_package(self):
        if (not self.target):
            return
        else:
            keys = pygame.key.get_pressed()
            self.leftKeyPressed = keys[pygame.K_LEFT]
            self.rightKeyPressed = keys[pygame.K_RIGHT]
            self.upKeyPressed = keys[pygame.K_UP]
            self.spaceKeyPressed = keys[pygame.K_SPACE]
            self.control()
        
    def auto_pilot(self):
        ### EDIT ME!
        ### This is where you are free to make changes.
        ### Everything up to the end of the block is the
        ### automatic guidance package. Any code outside
        ### of this block should be considered game code
        ### and modifying it will be modifying the game,
        ### which is completely different :)
        
        ### The bearing to the target, relative to the
        ### missile's flight path.
        degrees = self.RelAngleToTarget()
        
        ### Adjust the flight to this bearing
        self.adjust(degrees)
        
        ### Always be speeding up
        self.thrust(True)
        
        ### If we are in danger of leaving the flight zone,
        ### destroy self. Note that self destruction is
        ### not necessary for destroying the enemy missile
        ### and in fact may hurt your chances of doing so.
        if (self.x <= 200 or self.x >= 500):
            self.destruct()
        if (self.y <= 60):
            self.destruct()
        
        ### END OF EDIT ME!
    def manual_pilot(self):
        if self.leftKeyPressed:
            self.adjust(self.MAX_TURN_PER_CYCLE)
        elif self.rightKeyPressed:
            self.adjust(-self.MAX_TURN_PER_CYCLE)
        
        if self.spaceKeyPressed:
            self.destruct()
        if (self.upKeyPressed):
            self.thrust(True)
        else:
            self.thrust(False)
        
    def control(self):
        if self.manual:
            self.manual_pilot()
        else:
            self.auto_pilot()

    def reset(self):
        self.setPosition(self.resetposition)
        self.setAngle(90)
        self.setSpeed(4)
        self.cmdRotateTo(0) # Reset nav command from last launch
        
        # Reset detonations signal from last launch
        self.resetExplosives()