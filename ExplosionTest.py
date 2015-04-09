#!/usr/bin/env python

import pygame,gameEngine

import Explosion2


def main():
    game = gameEngine.Scene()
    explosion = Explosion2.Explosion(game)
    
    game.setCaption("Test")
    
    game.sprites = [explosion]
    
    game.start()
    
    
    
if __name__ == "__main__":
    main()
