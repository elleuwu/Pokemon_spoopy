import pygame

class SpriteSheet:
    def __init__(self,spritesheet):
        self.spritesheet = pygame.image.load(spritesheet)
        
    def spec_sprite(self,rectangle,colorkey):
        rect = pygame.Rect(rectangle)
        sprite_img = pygame.Surface(rect.size)

        sprite_img.blit(self.spritesheet,(0,0),rect)
        sprite_img.set_colorkey(colorkey)

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

        self.background_sprite = mainGame.env_sprites.spec_sprite((384,352,32,32),(0,0,0))
        self.background_border = mainGame.env_sprites.spec_sprite((352,352,32,32),(0,0,0))

        self.sprite_rect = self.background_sprite.get_rect()
        
    def blit_env(self):
        x = 0
        y = 0
        for row in self.config.map:
            for elem in row:
                if elem == "B":
                    self.screen.blit(self.background_sprite,(x,y))
                    self.screen.blit(self.background_border,(x,y))
                    x+=32
                elif elem == ".":
                    self.screen.blit(self.background_sprite,(x,y))
                    x+=32
            x=0
            y+=32


class Player(pygame.sprite.Sprite):
    def __init__(self,mainGame,config):
        pygame.sprite.Sprite.__init__(self)

        self.screen = mainGame.screen
        self.config = config

        self.sprite = mainGame.player_sprites.spec_sprite((172,2,32,32),(136,184,176))
        self.name = ''

        self.x, self.y = 0.0,0.0

    def blit_player(self):
        self.screen.blit(self.sprite,(500,500))