#!/usr/bin/env python
""" DefCon.py
    
    Defense Contractor.
    
"""

import pygame, gameEngine
#import Dropship
import EnemyMissile, PlayerMissile, Explosion2, Objective

class Intro(gameEngine.Scene):
    """ introduction. Sets the stage for... DEFCON.
    """
    
    def __init__(self,carrier):
        gameEngine.Scene.__init__(self)
        instructions = gameEngine.MultiLabel()
        instructions.textLines = [
            "You are a defense contractor planning",
            "to sell your latest missile, the",
            "Gipper Mark IV, to the military.",
            "Throughout the missile trials,",
            "defend the green school by using",
            "either custom guidance software",
            "[PlayerMissile.py], or using the",
            "arrow keys to steer and the spacebar",
            "to abort. Don't let your missile leave",
            "the proving grounds!"
        ]
        
        self.carrier = carrier #Carrier(0, True, 10)
        #self.background.fill((153,217,234))
        instructions.size = (400, 300)
        
        instructions.fgColor = (0xFF,0xFF,0xFF)
        instructions.bgColor = (0,0,0)
        instructions.center = (320, 200)
        
        self.buttonManual = gameEngine.Button()
        self.buttonAuto = gameEngine.Button()
        self.buttonManual.center = (200, 400)
        self.buttonManual.text = "Play [manual]"
        
        self.buttonAuto.center = (440, 400)
        self.buttonAuto.text = "Play [auto]"
        
        #self.button = gameEngine.Button()
        #self.button.center = (320, 400)
        #self.button.text = "Play"
        
        self.sprites = [instructions, self.buttonManual, self.buttonAuto]
        self.setCaption("DEFCON")
    
    def update(self):
        if self.buttonManual.clicked:
            self.carrier.playerControl = True
            self.stop()
        elif self.buttonAuto.clicked:
            self.carrier.playerControl = False
            self.stop()
            

class Game(gameEngine.Scene):
    """ primary gameplay state
        manages dropship, missiles
        returns score in carrier object
    """
    
    def update(self):
        
        if self.emissile.should_detonate and not self.emissile.hasExploded():
            self.__induceDestruction(self.emissile)
        if self.fmissile.should_detonate and not self.fmissile.hasExploded():
            self.__induceDestruction(self.fmissile)
        
        if self.state != self.IN_COMBAT:
            self.pause += 1
            
            if self.state == self.IN_EXPLOSION:
                if self.pause > self.explosionDelay:
                    self.pause = 0
                    self.state = self.IN_SANITY
                    
                    #return
            elif self.state == self.IN_SANITY:
                if self.pause > self.sanityDelay:
                    self.pause = 0
                    self.state = self.IN_COMBAT
                    
                    # Add reset code here
                    self.__nextLaunch()
                    #return
            else:
                pass
            
            return
        
        hitMissiles = pygame.sprite.spritecollide(self.fmissile, self.enemyGroup, False)
        
        hitObjective = pygame.sprite.spritecollide(self.objective, self.enemyGroup, False)
        if self.workaroundCounter > 0:
            self.workaroundCounter -= 1
            return
        
        if not self.__in_bounds(self.fmissile) and not self.fmissile.hasExploded():
            #self.launch += 1        # Yet another missile
            #self.ballistics += 1    # Yet another ballistic friendly missile.
            
            #self.objective.reset()
            #self.emissile.reset()
            #self.fmissile.reset()
            
            self.result = self.BALLISTIC
            self.__explodeAt(self.fmissile)
        elif hitObjective:
            #self.launch += 1        # give another missile
            #self.misses += 1        # Missile was NOT intercepted. Poop.
            self.result = self.MISS
            self.__explodeAt(self.objective)
            
            self.emissile.hide()
            
            #self.__nextLaunch()
            #the_missile = hitObjective[0]
            #self.explosion.explodeAt((the_missile.x,the_missile_y))
            #the_missile.reset()
            #self.carrier.score -= 100
            
            #self.fmissile.reset()
            
        elif self.fmissile.hasExploded() and self.emissile.hasExploded():
            # Both missiles have apparently successfully aborted or
            # the enemy missile has missed the objective.
            self.result = self.FIZZLE
            self.state = self.IN_EXPLOSION
            
        elif hitMissiles:
            if not self.__in_bounds(self.emissile):
                self.result = self.FIZZLE
                self.state = self.IN_EXPLOSION
            else:
                self.result = self.HIT
                self.__explodeAt(self.fmissile)
                
                
                self.fmissile.hide()
                self.emissile.hide()
                #self.__nextLaunch()
                #self.fmissile.reset()
                #the_missile.reset()
                ### TODO:
                # Put explosion animation here at intersection point and delay for duration
                
                #if self.carrier.score >= 50000:
                #    self.keepGoing = False
            
                #self.__nextLaunch()
        else:
            # Missiles are still in flight
            pass # let the good times roll!
        if self.launch > self.launches:
            self.keepGoing = False
    
    def __nextLaunch(self, first = False):
        self.fmissile.reset()
        self.emissile.reset()
        self.objective.reset()
        if not first:
            print "Trial %d:" % self.launch
        
        
        if (not first):
            if self.result == self.HIT:
                self.carrier.missile_hits()
                print "\tInterception!"
            elif self.result == self.MISS:
                self.carrier.missile_misses()
                print "\tFailure!"
                #self.sprites.addGroup(self.emissile)
                #print "boom!"
            elif self.result == self.BALLISTIC:
                self.carrier.missile_goes_ballistic()
                print "\tCatastrophic failure!"
            elif self.result == self.FIZZLE:
                self.carrier.missile_fizzles()
                print "\tEnemy missile fizzled."
            else:
                print "\tUnknown"
                #pass # impossible, but who knows
        else:
            pass
        
        self.launch += 1
    
    def __induceDestruction(self,target):
        if target.iff == 2:
            self.explosion_player.explodeAt((target.x,target.y))
            target.explode()
            target.hide()
            
        elif target.iff == 1:
            self.explosion_enemy.explodeAt((target.x,target.y))
            target.explode()
            target.hide()
        else:
            self.explosion.explodeAt((target.x,target.y))
        
        self.sndBoom.play()
        
    def __explodeAt(self,target):
        #print "EXPLOSION[%d\t%d]" % (target.x, target.y)
        self.state = self.IN_EXPLOSION
        self.explosion.explodeAt((target.x,target.y))
        self.sndBoom.play()
        
    def __in_bounds(self,object):
        in_x = object.x >= 0 and object.x <= 640
        in_y = object.y >= 0 and object.y <= 480
        
        return in_x and in_y
    
    def __init__(self,carrier):
        gameEngine.Scene.__init__(self)
        self.carrier = carrier
        
        # Need states
        
        
        self.sndBoom = pygame.mixer.Sound("Explosion-Diode111.ogg")
        self.IN_COMBAT = 0
        self.IN_EXPLOSION = 1
        self.IN_SANITY = 2
        
        self.HIT = 0
        self.MISS = 1
        self.BALLISTIC = 2
        self.FIZZLE = 3
        
        self.launch = 0         # The current missile launch
        self.launches = self.carrier.launches      # The total number of launches
        self.hits = 0           # The number of successful interceptions
        self.misses = 0         # The number of misses (but successful self-detonations)
        self.ballistics = 0     # The number of misses (without successful self-detonations)
        
        #self.dropship = Dropship.Dropship(self)
        self.emissile = EnemyMissile.EnemyMissile(self, (320, 240), (0,0), (320, 240))
        self.fmissile = PlayerMissile.PlayerMissile(self, (320, 479), (0,0), (320, 479), self.carrier.isPlayerControlled())
        
        self.explosion = Explosion2.Explosion(self)
        self.explosion_player = Explosion2.Explosion(self)
        self.explosion_enemy = Explosion2.Explosion(self)
        
        self.objective = Objective.Objective(self)
        
        self.emissile.hide()
        self.fmissile.hide()
        # Hee hee, let the launch-ex begin!
        self.emissile.lock_on(self.objective)
        self.fmissile.lock_on(self.emissile)
        
        
        self.enemyGroup = pygame.sprite.Group(self.emissile)
        
        self.addGroup(self.enemyGroup)
        self.sprites = [self.fmissile, self.objective,self.explosion,
                        self.explosion_player, self.explosion_enemy]
        
        self.setCaption("DEFCON")
        
        self.explosionHappened = False
        self.explosionDelay = 32
        self.sanityDelay = 60
        self.pause = 0
        
        self.state = self.IN_COMBAT
        
        self.result = 42
        
        self.workaroundCounter = 10
        self.background.fill((153,217,234))
        
        self.__nextLaunch(True)
class Carrier(object):
    """ an object meant to hold multi-state
        data:
        score, current number of points
        goAgain: boolean continue
        
        Adapted from Andy's Appendix B.
    """
    
    def __init__(self,score,goAgain,launches,playerControl=True):
        self.score = score
        self.goAgain = goAgain
        self.launches = launches
        self.playerControl = playerControl
        self.reset()
        
    def missile_hits(self):
        self.hits += 1
    
    def missile_misses(self):
        self.misses += 1
        
    def missile_goes_ballistic(self):
        self.ballistics += 1
    
    def isPlayerControlled(self):
        return self.playerControl
    
    def missile_fizzles(self):
        self.fizzles += 1
    def reset(self):
        self.hits = 0
        self.misses = 0
        self.ballistics = 0
        self.fizzles = 0
        
class Report(gameEngine.Scene):
    """ reports the player's score,
        determines if player wants
        to try again
        score and data passed in
        carrier object
    """
    def __init__(self, carrier):
        gameEngine.Scene.__init__(self)
        #self.background.fill((153,217,234))
        self.background.fill((0,0,0))
        self.carrier = carrier
        lblPoints = gameEngine.Label()
        #mlStats = gameEngine.MultiLabel()
        #mlStats.center = (320, 240)
        #mlStats.fgColor = (0xFF,0xFF,0xFF)
        #mlStats.size = (300, 100)
        #mlStats.textLines = [
        #    "Hits: %d Misses: %d Ballistics: %d"
        #]
        
        lblPoints.center = (320, 240)
        lblPoints.fgColor = (0xFF, 0xFF, 0xFF)
        lblPoints.bgColor = (0, 0, 0)
        lblPoints.size = (500, 50)
        lblPoints.text = "Hits: %d Misses: %d Ballistics: %d Fizzles: %d" % (carrier.hits, carrier.misses,
                                                                 carrier.ballistics, carrier.fizzles)
        self.btnAgain = gameEngine.Button()
        self.btnAgain.text = "play again"
        self.btnAgain.center = (100, 400)
        self.btnQuit = gameEngine.Button()
        self.btnQuit.text = "quit"
        self.btnQuit.center = (540, 400)
        self.sprites = [lblPoints, self.btnAgain, self.btnQuit]
    def update(self):
        if self.btnAgain.clicked:
            self.carrier.goAgain = True
            self.stop()
        if self.btnQuit.clicked:
            self.carrier.goAgain = False
            self.stop()
def main():
    carrier = Carrier(0, True, 10)
    pygame.mixer.init()
    if not pygame.mixer:
        print "problem with sound"
    
    intro = Intro(carrier)
    intro.start()


    
    
    while carrier.goAgain:
        game = Game(carrier)
        game.start()
        
        report = Report(carrier)
        report.start()
        carrier.reset()

if __name__ == "__main__":
    main()