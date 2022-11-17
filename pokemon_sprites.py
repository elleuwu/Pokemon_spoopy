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
    def __init__(self,mainGame,config,position):
        pygame.sprite.Sprite.__init__(self)

        self.mainGame = mainGame

        self.screen = mainGame.screen
        self.config = config

        self.sprite_forwards0 = mainGame.player_sprites.spec_sprite((172,2,32,32),(136,184,176))
        self.sprite_forwards1 = mainGame.player_sprites.spec_sprite((206,2,32,32),(136,184,176))
        self.sprite_forwards2 = mainGame.player_sprites.spec_sprite((274,2,32,32),(136,184,176))

        self.sprite_backwards0 = mainGame.player_sprites.spec_sprite((172,36,32,32),(136,184,176))
        self.sprite_backwards1 = mainGame.player_sprites.spec_sprite((206,36,32,32),(136,184,176))
        self.sprite_backwards2 = mainGame.player_sprites.spec_sprite((274,36,32,32),(136,184,176))

        self.sprite_left0 = mainGame.player_sprites.spec_sprite((172,104,32,32),(136,184,176))
        self.sprite_left1 = mainGame.player_sprites.spec_sprite((206,104,32,32),(136,184,176))
        self.sprite_left2 = mainGame.player_sprites.spec_sprite((274,104,32,32),(136,184,176))

        self.sprite_right0 = mainGame.player_sprites.spec_sprite((172,70,32,32),(136,184,176))
        self.sprite_right1 = mainGame.player_sprites.spec_sprite((206,70,32,32),(136,184,176))
        self.sprite_right2 = mainGame.player_sprites.spec_sprite((274,70,32,32),(136,184,176))


        self.images_right = [self.sprite_right0,self.sprite_right1,self.sprite_right0,self.sprite_right2]
        self.images_left = [self.sprite_left0,self.sprite_left1,self.sprite_left0,self.sprite_left2]
        self.images_up = [self.sprite_backwards0,self.sprite_backwards1,self.sprite_backwards0,self.sprite_backwards2]
        self.images_down = [self.sprite_forwards0,self.sprite_forwards1,self.sprite_forwards0,self.sprite_forwards2]

        self.name = ''

        self.x, self.y = position[0],position[1]

        self.velocity = 1

        self.pose = self.sprite_forwards0
        self.index = 0

        self.animation_frames = 4
        self.current_frame = 0

    def blit_player(self):
        self.screen.blit(self.pose,(self.x,self.y))

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x-=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_right)
                self.pose = self.images_right[self.index]

        elif keys[pygame.K_d]:
            self.x+=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_left)
                self.pose = self.images_left[self.index]

        elif keys[pygame.K_w]:
            self.y-=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_up)
                self.pose = self.images_up[self.index]

        elif keys[pygame.K_s]:
            self.y+=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_down)
                self.pose = self.images_down[self.index]
        

