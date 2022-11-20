from asyncio.windows_events import NULL
import pygame, random, threading

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

class Block(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y,image_to_load,collide_flag):

        self.mainGame = mainGame
        self.screen = mainGame.screen
        self.config = config

        self._layer = self.config.BLOCK_LAYER
        self.collide = collide_flag
        if self.collide == True:
            self.groups = self.mainGame.all_sprite_group, self.mainGame.env_sprite_group_col
        if self.collide == False:
            self.groups = self.mainGame.all_sprite_group, self.mainGame.env_sprite_group_nocol
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * self.config.TILESIZE
        self.y = y * self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.image = image_to_load
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



class Player(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y):

        self.mainGame = mainGame
        self.screen = mainGame.screen
        self.config = config

        self._layer = self.config.PLAYER_LAYER
        self.groups = self.mainGame.all_sprite_group, self.mainGame.player_sprite_group

        pygame.sprite.Sprite.__init__(self,self.groups)

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

        self.x = x*self.config.TILESIZE
        self.y = y*self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.velocity = 2

        self.image = self.sprite_forwards0

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0
        self.y_change = 0

        self.index = 0

        self.animation_frames = 4
        self.current_frame = 0

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collide("x")
        self.collide_enemy("x")
        self.rect.y += self.y_change
        self.collide("y")
        self.collide_enemy("y")
        self.collide_grass()


        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.mainGame.all_sprite_group:
                sprite.rect.x += self.velocity

            self.x_change-=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_right)
                self.image = self.images_right[self.index]


        elif keys[pygame.K_d]:
            for sprite in self.mainGame.all_sprite_group:
                sprite.rect.x -= self.velocity

            self.x_change+=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_left)
                self.image = self.images_left[self.index]

        elif keys[pygame.K_w]:
            for sprite in self.mainGame.all_sprite_group:
                sprite.rect.y += self.velocity

            self.y_change-=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_up)
                self.image = self.images_up[self.index]

        elif keys[pygame.K_s]:
            for sprite in self.mainGame.all_sprite_group:
                sprite.rect.y -= self.velocity

            self.y_change+=self.velocity
            self.current_frame+=1

            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(self.images_down)
                self.image = self.images_down[self.index]



    def collide(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self,self.mainGame.env_sprite_group_col,False)

            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.x += self.velocity

                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.x -= self.velocity


        if direction == "y":
            hits = pygame.sprite.spritecollide(self,self.mainGame.env_sprite_group_col, False)

            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.y += self.velocity

                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.y -= self.velocity


    def collide_enemy(self,direction):
        hits = pygame.sprite.spritecollide(self,self.mainGame.enemy_sprite_group,False)

        if direction == "x":
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.x += self.velocity

                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.x -= self.velocity

        if direction == "y":
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.y += self.velocity

                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.mainGame.all_sprite_group:
                        sprite.rect.y -= self.velocity
                    self.mainGame.talk_trainer = True


    def collide_grass(self):
        hits = pygame.sprite.spritecollide(self,self.mainGame.grass_sprite_group,False)

        if hits:
            self.mainGame.canEncounter = True
            
        else:
            self.mainGame.canEncounter = False


class Ground(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y):
        self.mainGame = mainGame
        self.screen = mainGame.screen
        self.config = config

        self._layer = self.config.GROUND_LAYER
        self.groups = self.mainGame.all_sprite_group
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*self.config.TILESIZE
        self.y = y*self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.background_sprite = mainGame.env_sprites.spec_sprite((64,0,32,32),(0,0,0))

        self.image = self.background_sprite

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self,mainGame,x,y,width,height,fg,bg,content,font,fontsize,colorkey,scale,image_to_load = False):

        self.mainGame = mainGame

        self.font = pygame.font.Font(font,fontsize)

        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        if image_to_load:
            img = pygame.transform.scale(image_to_load,(int(width*scale),int(height*scale)))
            img_rect = img.get_rect()
            self.image = pygame.Surface((width,height))
            self.image.fill(self.bg)
            if colorkey == True:
                self.image.set_colorkey(self.bg)
            self.image.blit(img,img_rect)

        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill(self.bg)
            if colorkey == True:
                self.image.set_colorkey(self.bg)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content,True,self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
        self.image.blit(self.text,self.text_rect)

    def is_pressed(self,pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def is_hover(self,pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def text_state(self,state):
        if state == 1:
            self.content = "You encountered a Pokemon!"
            self.text = self.font.render(self.content,True,self.fg)
            self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
            self.image.blit(self.text,self.text_rect)

        elif state == 2:
            self.image.fill(self.bg)
            self.content = "Go pokemon!"
            self.text = self.font.render(self.content,True,self.fg)
            self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
            self.image.blit(self.text,self.text_rect)

        elif state == 3:
            self.mainGame.intro_anim = True

        elif state == 4:
            self.mainGame.intro_anim = False

        elif state == 5:
            self.image.fill(self.bg)
            self.content = "What will your Pokemon do?"
            self.text = self.font.render(self.content,True,self.fg)
            self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
            self.image.blit(self.text,self.text_rect)

        elif state == 9:
            self.mainGame.encountered = False
            self.mainGame.in_battle = False
            self.mainGame.random_encounter_chance = 0
            self.mainGame.text_state = 0
            self.mainGame.encountered_pokemon.kill()
            self.mainGame.dawn.kill()
            self.mainGame.dawnPokemon.kill()
            self.mainGame.battle_music = False
            self.mainGame.encounter_anim = False




        

class Enemy(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y,rectx,recty):
        self.mainGame = mainGame
        self.config = config
        self._layer = self.config.ENEMY_LAYER
        self.groups = self.mainGame.all_sprite_group, self.mainGame.enemy_sprite_group
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*self.config.TILESIZE
        self.y = y*self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.image =  mainGame.trainer_sprites.spec_sprite((rectx,recty,self.width,self.height),(0,0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass

class WildGrassEncounters(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y,image_to_load):
        self.mainGame = mainGame
        self.config = config
        self._layer = self.config.GRASS_LAYER
        self.groups = self.mainGame.all_sprite_group, self.mainGame.grass_sprite_group
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*self.config.TILESIZE
        self.y = y*self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.image = image_to_load
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        pass

class Pokemon(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y,rect):
        self.mainGame = mainGame
        self.config = config
        self._layer = self.config.POKEMON_LAYER
        self.groups = self.mainGame.pokemon_sprite_group, self.mainGame.battle_sprite_group
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*self.config.TILESIZE
        self.y = y*self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.image_surface = self.mainGame.pokemon_sprites_f1.spec_sprite(rect,(0,0,0))
        self.image_rect = self.image_surface.get_rect()
        self.image_vector = pygame.math.Vector2((self.image_rect.width,self.image_rect.height))


        self.frame2 = self.mainGame.pokemon_sprites_f2.spec_sprite(rect,(0,0,0))
        self.images_anim = [self.frame2,self.image_surface]

        self.image = pygame.transform.scale(self.image_surface,self.image_vector * 4)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.index = 0

        self.animation_frames = 60
        self.current_frame = 0

    def update(self):
        self.idle()

    def idle(self):
        self.current_frame+=1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images_anim)
            self.image = pygame.transform.scale(self.images_anim[self.index],self.image_vector * 4)

class DawnThrowPokemon(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y):
        self.mainGame = mainGame
        self.config = config
        self._layer = self.config.TRAINER_INTRO_LAYER
        self.groups = self.mainGame.trainer_intro_group
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*self.config.TILESIZE
        self.y = y*self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.imageN = self.mainGame.player_sprites.spec_sprite((411,322,80,80),(0,128,128))
        self.image1 = self.mainGame.player_sprites.spec_sprite((2,322,80,80),(136,184,176))
        self.image2 = self.mainGame.player_sprites.spec_sprite((84,322,80,80),(136,184,176))
        self.image3 = self.mainGame.player_sprites.spec_sprite((166,322,80,80),(136,184,176))
        self.image4 = self.mainGame.player_sprites.spec_sprite((248,322,80,80),(136,184,176))
        self.image5 = self.mainGame.player_sprites.spec_sprite((330,322,80,80),(136,184,176))

        self.anim_list = [self.image1,self.image2,self.image3,self.image4,self.image5]

        self.index = 0
        self.animation_frames = 15
        self.current_frame = 0

        self.image = self.imageN
        self.rect = self.image.get_rect()
        self.image_vector = pygame.math.Vector2((self.rect.width,self.rect.height))
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.play_anim()

    def play_anim(self):
        self.current_frame+=1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.anim_list)
            self.image = pygame.transform.scale(self.anim_list[self.index],self.image_vector * 4)

        if self.index == 4:
            if self.current_frame == 14:
                self.mainGame.intro_anim == False
                self.mainGame.text_state+=1

class DawnPokemon(pygame.sprite.Sprite):
    def __init__(self,mainGame,config,x,y,rect):
        self.mainGame = mainGame
        self.config = config
        self._layer = self.config.TRAINER_POKEMON_LAYER
        self.groups = self.mainGame.trainer_pokemon_group
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*self.config.TILESIZE
        self.y = y*self.config.TILESIZE
        self.width = self.config.TILESIZE
        self.height = self.config.TILESIZE

        self.image_surface = self.mainGame.pokemon_sprites_back.spec_sprite(rect,(0,0,0))
        self.image_rect = self.image_surface.get_rect()
        self.image_vector = pygame.math.Vector2((self.image_rect.width,self.image_rect.height))

        self.image = pygame.transform.scale(self.image_surface,self.image_vector * 4)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass





        
