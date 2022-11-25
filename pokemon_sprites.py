from asyncio.windows_events import NULL
from difflib import Match
from distutils.command.config import config
import pygame, random, threading, csv,time


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
    def __init__(self,mainGame,x,y,width,height,fg,bg,content,font,fontsize,colorkey,scale,image_to_load = False,disable = False):

        self.mainGame = mainGame

        self.font = pygame.font.Font(font,fontsize)

        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg
        self.disable = disable

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
            self.content = f"You encountered a {self.mainGame.encountered_pokemon.name}!"
            self.text = self.font.render(self.content,True,self.fg)
            self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
            self.image.blit(self.text,self.text_rect)

        elif state == 2:
            self.image.fill(self.bg)
            self.content = f"Go {self.mainGame.dawnPokemon.name}!"
            self.text = self.font.render(self.content,True,self.fg)
            self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
            self.image.blit(self.text,self.text_rect)

        elif state == 3:
            self.mainGame.hide_button = True
            self.mainGame.intro_anim = True

        elif state == 4:
            self.mainGame.hide_button = False
            self.mainGame.intro_anim = False

        elif state == 5:
            self.mainGame.hide_button = False
            self.image.fill(self.bg)
            self.content = f"What will {self.mainGame.dawnPokemon.name} do?"
            self.text = self.font.render(self.content,True,self.fg)
            self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
            self.image.blit(self.text,self.text_rect)

        elif state == 6:
            self.mainGame.hide_button = True
            self.mainGame.dawn.kill()

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

        elif state == 10:
            pass


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

class pokemon_prop():
    def __init__(self,mainGame,config,pokemon_num):
        self.mainGame = mainGame
        self.config = config
        self.pokemon_to_load = pokemon_num

        names = open("pokemon-properties.csv")
        reader = csv.reader(names)
        for lines in reader:
            if int(lines[0]) == self.pokemon_num:
                self.name = lines[1]
                self.type1 = lines[2]
                self.type2 = lines[3]
                self.hp_base = int(lines[5])
                self.atk_base = int(lines[6])
                self.def_base = int(lines[7])
                self.spA_base = int(lines[8])
                self.spD_base = int(lines[9])
                self.speed_base = int(lines[10])
                self.isLegendary = lines[12]
                print(self.name,self.type1,self.type2,self.hp_base,self.atk_base,self.def_base,self.spA_base,self.spD_base,self.speed_base,self.isLegendary)
        names.close()
        self.base = [self.hp_base,self.atk_base,self.def_base,self.spA_base,self.spD_base,self.speed_base]

        self.hp_iv = random.randint(0,31)
        self.atk_iv = random.randint(0,31)
        self.def_iv = random.randint(0,31)
        self.spA_iv = random.randint(0,31)
        self.spD_iv = random.randint(0,31)
        self.speed_iv = random.randint(0,31)
        self.ivs = [self.hp_iv,self.atk_iv,self.def_iv,self.spA_iv,self.spD_iv,self.speed_iv]

        self.hp_ev = 0
        self.atk_ev = 0
        self.def_ev = 0
        self.spA_ev = 0
        self.spD_ev = 0
        self.speed_ev = 0
        self.evs = [self.hp_ev,self.atk_ev,self.def_ev,self.spA_ev,self.spD_ev,self.speed_ev]

        self.level = 50
        self.nature = self.mainGame.pkmn_natures(random.randint(1,25))

        self.hp = (((2*self.hp_base+self.hp_iv+(self.hp_ev//4))*self.level)//100)+self.level+10

        self.atk = (((2*self.atk_base+self.atk_iv+(self.atk_ev//4))*self.level)//100)+5
        self.defn = (((2*self.def_base+self.def_iv+(self.def_ev//4))*self.level)//100)+5
        self.spA = (((2*self.spA_base+self.spA_iv+(self.spA_ev//4))*self.level)//100)+5
        self.spD = (((2*self.spD_base+self.spD_iv+(self.spD_ev//4))*self.level)//100)+5
        self.speed = (((2*self.speed_base+self.speed_iv+(self.speed_ev//4))*self.level)//100)+5

        match self.nature:
            case self.mainGame.pkmn_natures.Hardy:
                print(self.nature)

            case self.mainGame.pkmn_natures.Lonely:
                print(self.nature)
                self.atk+=(self.atk//100)*10
                self.defn-=(self.defn//100)*10

            case self.mainGame.pkmn_natures.Brave:
                print(self.nature)
                self.atk+=(self.atk//100)*10
                self.speed-=(self.speed//100)*10

            case self.mainGame.pkmn_natures.Adamant:
                print(self.nature)
                self.atk+=(self.atk//100)*10
                self.spA-=(self.spA//100)*10

            case self.mainGame.pkmn_natures.Naughty:
                print(self.nature)
                self.atk+=(self.atk//100)*10
                self.spD-=(self.spD//100)*10

            case self.mainGame.pkmn_natures.Bold:
                print(self.nature)
                self.atk-=(self.atk//100)*10
                self.defn+=(self.defn//100)*10

            case self.mainGame.pkmn_natures.Docile:
                print(self.nature)

            case self.mainGame.pkmn_natures.Relaxed:
                print(self.nature)
                self.speed-=(self.speed//100)*10
                self.defn+=(self.defn//100)*10

            case self.mainGame.pkmn_natures.Impish:
                print(self.nature)
                self.spA-=(self.atk//100)*10
                self.defn+=(self.defn//100)*10

            case self.mainGame.pkmn_natures.Lax:
                print(self.nature)
                self.spD-=(self.atk//100)*10
                self.defn+=(self.defn//100)*10

            case self.mainGame.pkmn_natures.Timid:
                print(self.nature)
                self.atk-=(self.atk//100)*10
                self.speed+=(self.speed//100)*10

            case self.mainGame.pkmn_natures.Hasty:
                print(self.nature)
                self.defn-=(self.defn//100)*10
                self.speed+=(self.speed//100)*10

            case self.mainGame.pkmn_natures.Serious:
                print(self.nature)

            case self.mainGame.pkmn_natures.Jolly:
                print(self.nature)
                self.spA-=(self.spA//100)*10
                self.speed+=(self.speed//100)*10

            case self.mainGame.pkmn_natures.Naive:
                print(self.nature)
                self.spD-=(self.spD//100)*10
                self.speed+=(self.speed//100)*10

            case self.mainGame.pkmn_natures.Modest:
                print(self.nature)
                self.spA+=(self.spA//100)*10
                self.atk-=(self.atk//100)*10

            case self.mainGame.pkmn_natures.Mild:
                print(self.nature)
                self.spA+=(self.spA//100)*10
                self.defn-=(self.defn//100)*10

            case self.mainGame.pkmn_natures.Quiet:
                print(self.nature)
                self.spA+=(self.spA//100)*10
                self.speed-=(self.speed//100)*10

            case self.mainGame.pkmn_natures.Bashful:
                print(self.nature)

            case self.mainGame.pkmn_natures.Rash:
                print(self.nature)
                self.spA+=(self.spA//100)*10
                self.spD-=(self.spD//100)*10

            case self.mainGame.pkmn_natures.Calm:
                print(self.nature)
                self.spD+=(self.spA//100)*10
                self.atk-=(self.atk//100)*10

            case self.mainGame.pkmn_natures.Gentle:
                print(self.nature)
                self.spD+=(self.spA//100)*10
                self.defn-=(self.defn//100)*10

            case self.mainGame.pkmn_natures.Sassy:
                print(self.nature)
                self.spD+=(self.spA//100)*10
                self.speed-=(self.speed//100)*10

            case self.mainGame.pkmn_natures.Careful:
                print(self.nature)
                self.spA-=(self.spA//100)*10
                self.spD+=(self.spD//100)*10

            case self.mainGame.pkmn_natures.Quirky:
                print(self.nature)

        self.stats = [self.hp,self.atk,self.defn,self.spA,self.spD,self.speed]
        print(self.base,self.ivs,self.evs,self.stats)



class Pokemon(pygame.sprite.Sprite,pokemon_prop):
    def __init__(self,mainGame,config,x,y,rect,num):
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

        self.pokemon_num = num
        pokemon_prop.__init__(self,self.mainGame,self.config,self.pokemon_num)


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
        self.animation_frames = 10
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
            if self.current_frame == 9:
                self.mainGame.hide_button == False
                self.mainGame.text_state+=1

class DawnPokemon(pygame.sprite.Sprite,pokemon_prop):
    def __init__(self,mainGame,config,x,y,rect,num):
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

        self.pokemon_num = num
        pokemon_prop.__init__(self,self.mainGame,self.config,self.pokemon_num)

    def update(self):
        pass

class hp_bars():
    def __init__(self,mainGame,config,pokemon,dmg,rect,font):
        self.mainGame = mainGame
        self.config = config
        self.pokemon = pokemon
        self.name = self.pokemon.name
        self.max_hp = self.pokemon.hp
        if self.mainGame.turn == 0:
            self.current_hp = self.pokemon.hp-dmg
        else:
            self.current_hp = self.current_hp-dmg
        self.lvl = self.pokemon.level
        self.rect = pygame.Rect(rect)
        self.nameFont = pygame.font.Font(font,60)
        self.lvlFont = pygame.font.Font(font,60)
        print(self.max_hp,self.current_hp,"HP2")
        if self.current_hp == 0:
            self.hp_percentage = self.current_hp+1
        else:
            self.hp_percentage = (self.max_hp/self.current_hp)

        self.background = pygame.Surface((self.rect.width-10,self.rect.height-10))
        self.background.fill((240,240,240))

        self.background_outline = pygame.Surface((self.rect.width,self.rect.height))
        self.background_outline.fill((0,0,0))

        self.bar = pygame.Surface((300,40))
        self.bar.fill((0,0,0))
        self.bar_rect = self.bar.get_rect(x=75,y=75)

        self.hp_fill = pygame.Surface(((300*self.hp_percentage)-10,30))
        self.hp_fill.fill((0,230,0))
        self.hp_fill_rect = self.hp_fill.get_rect(x=5,y=5)

        self.pkmn_name = self.nameFont.render(f"{self.name}",True,(0,0,0))
        self.name_rect = self.pkmn_name.get_rect(x=10,y=10)

        self.pkmn_lvl = self.lvlFont.render(f"Lvl  {self.lvl}",True,(0,0,0))
        self.lvl_rect = self.pkmn_lvl.get_rect(x=250,y=10)

        self.pkmn_hp = self.nameFont.render(f"HP",True,(0,0,0))
        self.hp_rect = self.pkmn_hp.get_rect(x=25,y=70)

        self.bar.blit(self.hp_fill,self.hp_fill_rect)
        self.background.blit(self.bar,self.bar_rect)
        self.background.blit(self.pkmn_hp,self.hp_rect)
        self.background.blit(self.pkmn_name,self.name_rect)
        self.background.blit(self.pkmn_lvl,self.lvl_rect)
        self.background_outline.blit(self.background,(self.rect.x+5,self.rect.y+5,self.rect.width,self.rect.height))







        
