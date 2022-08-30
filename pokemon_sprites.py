import pygame

class SpriteSheet:
    def __init__(self,spritesheet):
        self.spritesheet = pygame.image.load(spritesheet)
        
    def spec_sprite(self,rectangle):
        rect = pygame.Rect(rectangle)
        sprite_img = pygame.Surface(rect.size)

        sprite_img.blit(self.spritesheet,(0,0),rect)
        sprite_img.set_colorkey((0,0,0))

        return sprite_img

    def multi_sprite(self,rects):
        sprites = []
        for elem in rects:
            sprites.append(self.spec_sprite(elem))
        return sprites

class background_env(pygame.sprite.Sprite):
    def __init__(self,mainGame,config):
        pygame.sprite.Sprite.__init__(self)

        self.screen = mainGame.screen
        self.config = config

        self.background_sprite = mainGame.env_sprites.spec_sprite((384,352,32,32))

        self.sprite_rect = self.background_sprite.get_rect()
        
    def blit_env(self):
        for x in range(0,self.config.screen_width,32):
            for y in range(0,self.config.screen_height,32):
                self.screen.blit(self.background_sprite,(x,y))

class Player:
    def __init__(self,main_game):
        self.sprite = None
        self.name = ''

        self.screen = main_game.screen

        self.x, self.y = 0.0,0.0
