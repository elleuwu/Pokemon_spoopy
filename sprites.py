import pygame
class SpriteSheet:


    


class Player:
    def __init__(self,main_game):
        self.sprite = None
        self.name = ''

        self.screen = main_game.screen

        self.x, self.y = 0.0,0.0

    def blitplayer(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x,self.y
        self.screen.blit(self.image,self.rect)