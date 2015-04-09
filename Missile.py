#!/usr/bin/env python

import pygame, gameEngine


class Missile(gameEngine.SuperSprite):
    def __init__(self,scene,initpos,initvel):
        gameEngine.SuperSprite.__init__(self,scene)
        self.setSpeed(0)
        self.setAngle(0)
        
        self.iff = 0
        self.setImage("missile_bmp.bmp")
        
        tranColor = self.imageMaster.get_at((1,1))
        self.imageMaster.set_colorkey(tranColor)
        self.setPosition(initpos)
        self.setComponents(initvel)
        self.updateVector()
        self.STARTING_SPEED = 3
        self.MAX_TURN_PER_CYCLE = 15
        self.THRUST_AMT = 1
        self.target = None
        self.counter = 0
        
        self.setBoundAction(self.HIDE)
        
        self.code_count = 15
        self.angle_frame_interval = 0
        
        self.should_detonate = False
        
        self.exploded = False
        ## Variables that the user is given access to.
        
    def explode(self):
        self.exploded = True
    
    def hasExploded(self):
        return self.exploded
    
    def checkEvents(self):
        self.counter += 1
        
        if (self.counter >= self.code_count):
            self.counter = 0
            
            self.run_guidance_package()
            
        self.turnBy(self.angle_frame_interval)
        #self.telemetry()
        #FF1F17
        #self.drawTrace((0xFF,0x1F,0x17))
        
    def lock_on(self,target):
        self.target = target
        
    
    def thrust(self,on):
        if (on):
            self.speedUp(self.THRUST_AMT)
    
    def run_guidance_package(self):
        self.target = self.target
        
    def RelAngleToTarget(self):
        if (not self.target):
            return 0
        raw = self.dirTo((self.target.x, self.target.y)) - self.dir
        if raw >= 180:
            raw -= 360
        return raw
    
    def DistanceToTarget(self):
        if (not self.target):
            return -1
        distance = self.distanceTo((self.target.x, self.target.y))
        return distance
        
    def cmdRotateTo(self, relAngle):
        self.angle_frame_interval = relAngle/self.code_count
        
    def adjust(self, turnDeg):
        """ Course correct during an execution loop. Can only turn inside
            of a certain radius.
        """ 
        if abs(turnDeg) > self.MAX_TURN_PER_CYCLE:
            if (turnDeg < 0):
                self.cmdRotateTo(-self.MAX_TURN_PER_CYCLE)
            else:
                self.cmdRotateTo(self.MAX_TURN_PER_CYCLE)
        else:
            self.cmdRotateTo(turnDeg)
    
    def destruct(self):
        self.should_detonate = True
        #self.explode()
    def hide(self):
        self.speed = 0
        self.setPosition((-1000, -1000))
    
    def resetExplosives(self):
        self.exploded = False
        self.should_detonate = False
    def telemetry(self):
        if (not self.target):
            print "<NO TARGET>"
        else:
            print "target: %d %d" % (self.RelAngleToTarget(), self.DistanceToTarget())