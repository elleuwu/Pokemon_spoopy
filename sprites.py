import pygame
class SpriteSheet:
    def __init__(self,spritesheet):
        self.spritesheet = pygame.image.load(spritesheet).convert()
        
    def spec_sprite(self,rectangle):
        rect = pygame.Rect(rectangle)
        sprite_img = pygame.Surface(rect.size).convert()

        sprite_img.blit(self.spritesheet,(0,0),rect)
        sprite_img.set_colorkey((0,0,0))

        return sprite_img

    def multi_sprite(self,rects):
        sprites = []
        for elem in rects:
            sprites.append(self.spec_sprite(elem))
        return sprites

    


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