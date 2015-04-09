=============================================================================
DEFCON ReadMe
=============================================================================

==The Story==

As a DEFense CONtractor, you are trying to sell your newest missile, the
state of the art Gipper Mark IV, to the various branches of the military.

The Gipper IV is designed to directly intercept inbound missiles directed
at ground targets. While it boasts a high launch speed and reasonable
maneuverability, its biggest feature is the high adaptability of its guidance
module.

The setting is the Proving Grounds, a remote field where missiles are tried
and tested before being allowed to protect real targets. Here stands a
cheap and easily rebuilt school replica, designed to be a valuable target
for the opposing missile and a key objective for you to protect.

You must intercept the missile before it hits the school. Here are the test
guidelines:

An interception means you hit the missile, and it explodes.

A miss means you don't hit the missile, and it hits the school.

A fizzle means that the enemy missile doesn't hit the school, but you
maintain control.

Finally, a ballistic means that your missile went "ballistic", out of
guided control. It left the proving grounds and probably hit a
casino in nearby Las Vegas or an orphanage for all you know. This is not good.

==The Gameplay: Manual==
You can play this game one of two ways. The first and most immediate way
is to fly the missile yourself, playing the part of the guidance module.

Press the Up key to apply thrust.
Press the Left key to rotate left.
Press the Right key to rotate right.
Press the Space key to abort the missile and detonate it in mid-air.

Note that you will have to detonate if your missile is in danger of leaving
the proving grounds airspace.

==The Gameplay: Auto==
This is the interesting form of gameplay. Your job takes place in a code
editor of your choice. That's right. Open PlayerMissile.py and look for the
EDIT ME comments. You can change this code to your heart's content using
valid Python code. Your objectives remain the same as in manual, but now
let the computer do the hard work.

The methods you have access to include:

self.RelAngleToTarget()
    The offset in degrees from your flight path to the target. Returns angle
    in [-180,180]

self.DistanceToTarget()
    The distance to the target in pixels.
    
self.destruct()
    Instructs the missile to detonate prematurely, for the sole purpose of
    avoiding losing control
    
self.adjust(degrees)
    Rotate the missile over a period of one half second to a new heading
    by the degrees parameter. Negative for left, Positive for right.
    
self.Thrust(on)
    Turn the thrusters on or off. Thrusters will make the missile fly
    faster, but remember, you cannot slow down again!
    
self.x [readonly]
    X coordinate, in pixels

self.y [readonly]
    Y coordinate, in pixels
    
Note: Gameplay is also managed inside this codefile. While you are free
to modify and improve the game as you see fit, you really only get bragging
rights in an unmodified game.