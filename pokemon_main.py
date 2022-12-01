from asyncio.windows_events import NULL
from logging import exception
import pygame,sys,random,time,threading,cv2,numpy as np, os,csv
from enum import Enum
from pokemon_config import *
from pokemon_sprites import *

class mainGame:
    
    """Class to manage the game assets and behaviour"""

    def __init__(self):
        pygame.init()

        self.fontH = pygame.font.Font("Pokemon Hollow.ttf",50)
        self.fontS = pygame.font.Font("Pokemon Solid.ttf",50)
        self.fontS2 = pygame.font.Font("Pokemon Solid.ttf",54)
        self.fontsP = pygame.font.Font("pokemon_pixel_font.ttf",60)

        self.config = Config()

        self.player_sprites = SpriteSheet("sprites//Dawn Trainer.png")
        self.env_sprites = SpriteSheet("sprites//PokemonTerrainSprites.png")
        self.trainer_sprites = SpriteSheet("sprites//Overworld Trainer Pack//Overworld_Trainers.png")
        self.pokemon_sprites_f1 = SpriteSheet("sprites//diamond-pearl-1.png")
        self.pokemon_sprites_f2 = SpriteSheet("sprites//diamond-pearl-frame2.png")
        self.pokemon_sprites_back = SpriteSheet("sprites//diamond-pearl-back.png")

        self.intro_background = pygame.image.load("pokemon start screen.jpg")
        self.text_box = pygame.image.load("sprites//text_box.png")
        self.battle_background = pygame.image.load("Battle Background.png")

        self.pokemon_properties = open("pokemon-properties.csv","r")
        reader = csv.reader(self.pokemon_properties)
        self.legendaries = []
        for lines in reader:
            if lines[12] == "TRUE":
                self.legendaries.append(int(lines[0]))

        self.all_sprite_group = pygame.sprite.LayeredUpdates()
        self.player_sprite_group = pygame.sprite.LayeredUpdates()
        self.env_sprite_group_col = pygame.sprite.LayeredUpdates()
        self.env_sprite_group_nocol = pygame.sprite.LayeredUpdates()
        self.enemy_sprite_group = pygame.sprite.LayeredUpdates()
        self.grass_sprite_group = pygame.sprite.LayeredUpdates()
        self.pokemon_sprite_group = pygame.sprite.LayeredUpdates()
        self.battle_sprite_group = pygame.sprite.LayeredUpdates()
        self.trainer_intro_group = pygame.sprite.LayeredUpdates()
        self.trainer_pokemon_group = pygame.sprite.LayeredUpdates()

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((self.config.screen_width,self.config.screen_height))
        pygame.display.set_caption("Pokemon Remake Early Alpha Test 01")
        self.screen_rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.scale = 1.2
        self.internal_surf_size = (1920,1080)
        self.internal_surf = pygame.surface.Surface((self.config.screen_width,self.config.screen_height),pygame.SRCALPHA)
        self.internal_surf_rect = self.internal_surf.get_rect(center = (self.config.screen_width//2,self.config.screen_height//2))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()

        self.createMap()

        self.canEncounter = False
        self.talk_trainer = False
        self.enc_timer_started = False

        self.enc_timer = threading.Thread(target = self.encounter_timer,daemon = True)

        self.random_encounter_chance = 1.1

        self.grass_encounter_video = cv2.VideoCapture('Videos\\Trainer encounter_Trim.mp4')
        self.grass_success, self.grass_encounter_frame = self.grass_encounter_video.read()
        self.grass_encounter_frame = cv2.resize(self.grass_encounter_frame,(1248,736))
        self.grass_shape = self.grass_encounter_frame.shape[1::-1]

        self.background_rect = self.battle_background.get_rect()
        self.background = pygame.Surface((self.background_rect.width,self.background_rect.height))
        self.background.fill((255,255,255))
        self.background.blit(self.battle_background,self.background_rect)

        self.encountered = False
        self.battle_music = False
        self.in_battle = False
        self.turn = 0
        self.text_state = 0
        self.sub_state = 0
        self.mainText = Button(self,15,581,750,150,(0,0,0),(230,230,230),"","pokemon_pixel_font.ttf",70,False,2)
        self.hide_button = False
        self.intro_anim = False
        self.encounter_anim = False
        self.overworld_music_playing = False
        self.dmg_once = False
        self.dawn_dmg,self.wild_dmg = 0,0
        self.trainer_battle = False

        self.battle_music_list = ["Music\\Necrozma battle song.wav","Music\\Vs blue battle song.wav","Music\\Vs cyrus battle song.wav","Music\\Zekrom reshiram battle song.wav"]

        self.pkmn_natures = Enum("Natures",[("Sassy",1),("Lonely",2),("Brave",3),("Adamant",4),("Naughty",5),("Bold",6),("Docile",7),("Relaxed",8),
                                            ("Impish",9),("Lax",10),("Timid",11),("Hasty",12),("Serious",13),("Jolly",14),("Naive",15),("Modest",16),
                                            ("Mild",17),("Quiet",18),("Bashful",19),("Rash",20),("Calm",21),("Gentle",22),("Hardy",23),("Careful",24),
                                            ("Quirky",25)])

        self.types = ["Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic","Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]

    def createMap(self):
        self.trainer_pos = []
        for i, row in enumerate(self.config.map):
            for j, column in enumerate(row):
                Ground(self,self.config,j,i)
                if column == "B":
                    Block(self,self.config,j,i,self.env_sprites.spec_sprite((0,0,32,32),(0,0,0)),True)
                if column == "G":
                    WildGrassEncounters(self,self.config,j,i,self.env_sprites.spec_sprite((32,0,32,32),(0,0,0)))
                if column == "P":
                    self.player = Player(self,self.config,j,i)
                if column == "T":
                    self.trainer = Enemy(self,self.config,j,i,(self.config.TILESIZE*random.randrange(0,30)),(self.config.TILESIZE*random.randrange(0,21)))
                    self.trainer_pos.append(self.trainer.rect)


    def run_game(self):
        self.start_screen()
        if pygame.mixer.get_init():
            self.music = pygame.mixer.music.load("Music//Viridian city theme.wav")
            pygame.mixer.music.play(loops=-1)
        self.overworld_music_playing = True
        while True:
            if self.talk_trainer == True:
                self.text_screen()
                self.events()
                self.updates()

            elif self.canEncounter == True:
                if self.overworld_music_playing:
                    pass
                else:
                    if pygame.mixer.get_init():
                        self.music = pygame.mixer.music.load("Music//Viridian city theme.wav")
                        pygame.mixer.music.play(loops=-1) 
                    self.overworld_music_playing = True
                if not self.in_battle:
                    self.encounter_events()
                    self.updates()
                    self.wild_battle()
                elif self.in_battle:
                    while self.in_battle:
                        self.encounter_events()
                        self.updates_encounter()
                        self.draw_encounter()
            else:
                self.events()
                self.updates()
                self.draw()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()



    def encounter_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.text_state < 5:
                        if self.mainText.is_pressed(event.pos):
                            self.text_state+=1
                    else:
                        if self.fight.is_pressed(event.pos):
                            self.text_state = 6
                        if self.bag.is_pressed(event.pos):
                            self.text_state = 7
                        if self.Pokemon.is_pressed(event.pos):
                            self.text_state = 8
                        if self.run.is_pressed(event.pos):
                            self.text_state = 9

                    if self.text_state == 6:
                        if self.move_back.is_pressed(event.pos):
                            if self.move_back.disable:
                                time.sleep(0.01)
                                self.move_back.disable = False
                            else:
                                self.text_state = 5
                                self.move_back.disable = True

                        if self.move1.is_pressed(event.pos):
                            self.text_state = 10
                            self.move = self.dawnPokemon.all_moves[0]
                            print(self.move)
                        if self.move2.is_pressed(event.pos):
                            self.text_state = 10
                            self.move = self.dawnPokemon.all_moves[1]
                        if self.move3.is_pressed(event.pos):
                            self.text_state = 10
                            self.move = self.dawnPokemon.all_moves[2]
                        if self.move4.is_pressed(event.pos):
                            self.text_state = 10
                            self.move = self.dawnPokemon.all_moves[3]

                    if self.text_state == 11:
                        if self.mainText.is_pressed(event.pos):
                            self.dmg_once = False
                            if self.enemy_hp_bar.hp_anim:
                                pass
                            else:
                                if self.fainted:
                                    self.text_state = 15
                                    self.mainText.disable = True
                                else:
                                    if self.first_move:
                                        if self.dawn_dmg[1]:
                                            self.text_state = 13
                                            self.mainText.disable = True
                                            self.end = False
                                            self.state = 11
                                        else:
                                            self.text_state = 12
                                    else:
                                        if self.dawn_dmg[1]:
                                            self.text_state = 13
                                            self.mainText.disable = True
                                            self.end = True
                                        else:
                                            self.text_state = 5
                                            self.turn +=1



                    elif self.text_state == 12:
                        if self.mainText.is_pressed(event.pos):
                            self.dmg_once = False
                            if self.dawn1_hp_bar.hp_anim:
                                pass
                            else:
                                if self.fainted:
                                    self.text_state = 14
                                    self.mainText.disable = True
                                else:
                                    if self.first_move:
                                        if self.wild_dmg[1]:
                                            self.text_state = 13
                                            self.mainText.disable = True
                                            self.end = True
                                        else:
                                            self.text_state = 5
                                            self.turn += 1
                                    else:
                                        if self.wild_dmg[1]:
                                            self.text_state = 13
                                            self.mainText.disable = True
                                            self.end = False
                                            self.state = 12
                                        else:
                                            self.text_state = 11

                    if self.text_state == 13:
                        if self.mainText.is_pressed(event.pos):
                            if self.mainText.disable:
                                time.sleep(0.01)
                                self.mainText.disable = False
                            else:
                                if self.end:
                                    self.text_state = 5
                                    self.turn = 1
                                    self.crit = False
                                else:
                                    if self.state == 11:
                                        self.text_state = 12
                                        self.crit = False
                                    else:
                                        self.text_state = 11
                                        self.crit = False

                    if self.text_state == 14 or self.text_state == 15:
                        if self.mainText.is_pressed(event.pos):
                            if self.mainText.disable:
                                time.sleep(0.01)
                                self.mainText.disable = False
                            else:   
                                self.text_state = 9


        if self.canEncounter == True:
            if not self.enc_timer_started:
                print("thread started")
                self.enc_timer_started = True
                self.enc_timer.start()


    def wild_battle(self):
        if self.random_encounter_chance <= 0.9 and self.random_encounter_chance>0:
            self.encountered = True

        if self.encountered == True:
            self.wild_pokemon = self.random_pokemon()
            self.encountered_pokemon = Pokemon(self,self.config,24,7,self.wild_pokemon,self.random_pokemon_num)
            self.draw_encounter()
            self.in_battle = True
            self.turn = 0
            self.encounter_anim = True

            self.mainText = Button(self,15,581,750,150,(0,0,0),(230,230,230),"","pokemon_pixel_font.ttf",70,False,2,disable=True)
            self.mainTextOutline = Button(self,10,576,760,160,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.dawn = DawnThrowPokemon(self,self.config,0,13)
            self.player_pokemon = self.random_pokemon(250,False)
            self.dawnPokemon = DawnPokemon(self,self.config,2,9,self.player_pokemon,250)

            self.fight = Button(self,800,576,200,70,(0,0,0),(240,240,240),"Fight","pokemon_pixel_font.ttf",70,False,2)
            self.fightOutline = Button(self,795,571,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.bag = Button(self,1015,576,200,70,(0,0,0),(240,240,240),"Bag","pokemon_pixel_font.ttf",70,False,2)
            self.bagOutline = Button(self,1010,571,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.Pokemon = Button(self,800,661,200,70,(0,0,0),(240,240,240),"Pokemon","pokemon_pixel_font.ttf",70,False,2)
            self.PokemonOutline = Button(self,795,656,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.run = Button(self,1015,661,200,70,(0,0,0),(240,240,240),"Run","pokemon_pixel_font.ttf",70,False,2)
            self.runOutline = Button(self,1010,656,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.move1 = Button(self,15,581,365,65,(0,0,0),(240,240,240),self.dawnPokemon.move1,"pokemon_pixel_font.ttf",70,False,2)
            self.move1_outline = Button(self,10,576,375,75,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.move2 = Button(self,395,581,365,65,(0,0,0),(240,240,240),self.dawnPokemon.move2,"pokemon_pixel_font.ttf",70,False,2)
            self.move2_outline = Button(self,390,576,375,75,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.move3 = Button(self,15,661,365,65,(0,0,0),(240,240,240),self.dawnPokemon.move3,"pokemon_pixel_font.ttf",70,False,2)
            self.move3_outline = Button(self,10,656,375,75,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.move4 = Button(self,395,661,365,65,(0,0,0),(240,240,240),self.dawnPokemon.move4,"pokemon_pixel_font.ttf",70,False,2)
            self.move4_outline = Button(self,390,656,375,75,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.move_back = Button(self,800,550,410,175,(0,0,0),(240,240,240),"Back","pokemon_pixel_font.ttf",70,False,2,disable=True)
            self.move_back_outline = Button(self,795,545,420,185,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2,disable=True)

            self.enemy_hp_bar = hp_bars(self,self.config,self.encountered_pokemon,0,(0,0,400,150),"pokemon_pixel_font.ttf")

            self.dawn1_hp_bar = hp_bars(self,self.config,self.dawnPokemon,0,(0,0,400,150),"pokemon_pixel_font.ttf")

            self.pokemonai = pokemonAI(self,self.dawnPokemon,self.encountered_pokemon)

        else:
            self.draw()

    def random_pokemon(self,set_mon=0,randoms=True):
        if randoms:
            self.random_pokemon_num = random.randint(0,493)
            for i in self.legendaries:
                if i == self.random_pokemon_num:
                    keep_legendary = random.random()
                    if keep_legendary >= 0.5:
                        self.random_pokemon_num = random.randint(0,493)
        else:
            self.random_pokemon_num = set_mon
        pkmn_y = ((self.random_pokemon_num*80)//2240)
        if self.random_pokemon_num%28 == 0:
            pkmn_y-=1
        pkmn_x = (self.random_pokemon_num-(28*(pkmn_y)))
        print(pkmn_y,pkmn_x)
        if pkmn_x == 0:
            rect = pygame.Rect(pkmn_x*80,pkmn_y*80,80,80)
        else:
            rect = pygame.Rect((pkmn_x*80)-80,pkmn_y*80,80,80)
        print(rect,"Rect")
        return rect
        

    def updates(self):
        self.all_sprite_group.update()

    def updates_encounter(self):
        if self.intro_anim:
            self.trainer_intro_group.update()
        self.pokemon_sprite_group.update()
        self.trainer_pokemon_group.update()

    def draw(self):
        self.internal_surf.fill((0,0,0))

        self.screen.fill((0,0,0))

        self.all_sprite_group.draw(self.internal_surf)

        scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surf_size_vector * self.scale)
        scaled_rect = scaled_surf.get_rect(center = (self.config.screen_width//2,self.config.screen_height//2))

        self.screen.blit(scaled_surf,scaled_rect)

        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_encounter(self):
        if self.turn >= 0:
            self.mainText.text_state(self.text_state)
            frame_counter = 0
            while self.encounter_anim:
                frame_counter+=1
                if self.encountered==True:
                    if self.battle_music:
                        pass
                    else:
                        self.draw()
                        song = random.randint(0,3)
                        if pygame.mixer.get_init():
                            self.music = pygame.mixer.music.load(self.battle_music_list[song])
                            pygame.mixer.music.play(loops=-1)
                        self.battle_music = True
                        self.overworld_music_playing = False

                    self.clock.tick(self.fps)
                    if frame_counter != int(self.grass_encounter_video.get(cv2.CAP_PROP_FRAME_COUNT)):
                        self.grass_success, self.grass_encounter_frame = self.grass_encounter_video.read()
                        self.grass_encounter_frame = cv2.resize(self.grass_encounter_frame,(1248,736))
                        surface = pygame.image.frombuffer(self.grass_encounter_frame.tobytes(), self.grass_shape, "BGR")
                        surface.set_colorkey((15,250,5,255))
                        self.screen.blit(surface,(0, 0))
                        pygame.display.update()
                
                    else:
                        self.encounter_anim = False
                        frame_counter = 0
                        self.grass_encounter_video.set(cv2.CAP_PROP_POS_FRAMES,0)

                        pygame.display.update()

            self.screen.blit(self.background,(0,0))

            if self.text_state >= 4:
                self.trainer_pokemon_group.draw(self.screen)
                self.screen.blit(self.dawn1_hp_bar.background_outline,(100,100))
                self.screen.blit(self.enemy_hp_bar.background_outline,(750,25))

            if self.text_state == 5:
                self.screen.blit(self.fightOutline.image,self.fightOutline.rect)
                self.screen.blit(self.fight.image,self.fight.rect)
                self.screen.blit(self.bagOutline.image,self.bagOutline.rect)
                self.screen.blit(self.bag.image,self.bag.rect)
                self.screen.blit(self.PokemonOutline.image,self.PokemonOutline.rect)
                self.screen.blit(self.Pokemon.image,self.Pokemon.rect)
                self.screen.blit(self.runOutline.image,self.runOutline.rect)
                self.screen.blit(self.run.image,self.run.rect)

            if self.text_state == 6:

                self.screen.blit(self.move1_outline.image,self.move1_outline.rect)
                self.screen.blit(self.move1.image,self.move1.rect)
                self.screen.blit(self.move2_outline.image,self.move2_outline.rect)
                self.screen.blit(self.move2.image,self.move2.rect)
                self.screen.blit(self.move3_outline.image,self.move3_outline.rect)
                self.screen.blit(self.move3.image,self.move3.rect)
                self.screen.blit(self.move4_outline.image,self.move4_outline.rect)
                self.screen.blit(self.move4.image,self.move4.rect)

                self.screen.blit(self.move_back_outline.image,self.move_back_outline.rect)
                self.screen.blit(self.move_back.image,self.move_back.rect)

            if self.text_state == 10:
                self.fainted = False
                self.dmg_once = False
                #self.pokemonai.supereffective()

                if self.pokemonai.effective == 2:
                    self.random_move = self.pokemonai.possible_moves[random.randint(0,len(self.pokemonai.possible_moves)-1)]
                else:
                    self.random_move = self.encountered_pokemon.all_moves[random.randint(0,3)]
                self.pokemonai.possible_moves.clear()

                self.dawn_dmg = self.calc_damage(self.move,self.dawnPokemon,self.encountered_pokemon)
                self.wild_dmg = self.calc_damage(self.random_move,self.encountered_pokemon,self.dawnPokemon)

                if self.dawnPokemon.speed >= self.encountered_pokemon.speed:
                    self.first_move = True
                if self.dawnPokemon.speed < self.encountered_pokemon.speed:
                    self.first_move = False

                if self.first_move:
                    self.text_state = 11
                else:
                    self.text_state = 12
            
            if self.hide_button == False:
                self.screen.blit(self.mainTextOutline.image,(self.mainTextOutline.rect))
                self.screen.blit(self.mainText.image,(self.mainText.rect))

            if self.hide_button == True:
                self.trainer_intro_group.draw(self.screen)

            self.clock.tick(self.fps)
            self.battle_sprite_group.draw(self.screen)

        pygame.display.update()

    def calc_damage(self,move,pokemon1,pokemon2):
        move_used = move
        atk_pokemon = pokemon1
        def_pokemon = pokemon2
        level = atk_pokemon.level

        effective = 0
        if move_used[2] == atk_pokemon.type1 or atk_pokemon.type2:
            stab = 1.5
        else:
            stab = 1
        
        if move_used[2] == "Fire":
            if def_pokemon.type1 == "Grass" or def_pokemon.type1 == "Ice" or def_pokemon.type1 == "Bug" or def_pokemon.type1 == "Steel":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Fire" or def_pokemon.type1 == "Water" or def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Dragon":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Grass" or def_pokemon.type2 == "Ice" or def_pokemon.type2 == "Bug" or def_pokemon.type2 == "Steel":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Fire" or def_pokemon.type2 == "Water" or def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Dragon":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Normal":
            if def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Steel":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Ghost":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Steel":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Ghost":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Fighting":
            if def_pokemon.type1 == "Normal" or def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Ice" or def_pokemon.type1 == "Dark":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Flying" or def_pokemon.type1 == "Poison" or def_pokemon.type1 == "Bug" or def_pokemon.type1 == "Psychic" or def_pokemon.type1 == "Fairy":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Ghost":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Normal" or def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Ice" or def_pokemon.type2 == "Dark":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Flying" or def_pokemon.type2 == "Poison" or def_pokemon.type2 == "Bug" or def_pokemon.type2 == "Psychic" or def_pokemon.type2 == "Fairy":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Ghost":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Water":
            if def_pokemon.type1 == "Ground" or def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Fire":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Water" or def_pokemon.type1 == "Grass" or def_pokemon.type1 == "Dragon":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Ground" or def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Fire":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Water" or def_pokemon.type2 == "Grass" or def_pokemon.type2 == "Dragon":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Flying":
            if def_pokemon.type1 == "Fighting" or def_pokemon.type1 == "Bug" or def_pokemon.type1 == "Grass":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Electric":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Fighting" or def_pokemon.type2 == "Bug" or def_pokemon.type2 == "Grass":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Electric":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Grass":
            if def_pokemon.type1 == "Ground" or def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Water":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Flying" or def_pokemon.type1 == "Poison" or def_pokemon.type1 == "Bug" or def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Fire" or def_pokemon.type1 == "Grass" or def_pokemon.type1 == "Dragon":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Ground" or def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Water":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Flying" or def_pokemon.type2 == "Poison" or def_pokemon.type2 == "Bug" or def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Fire" or def_pokemon.type2 == "Grass" or def_pokemon.type2 == "Dragon":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Poison":
            if def_pokemon.type1 == "Grass" or def_pokemon.type1 == "Fairy":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Poison" or def_pokemon.type1 == "Ground" or def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Ghost":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Steel":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Grass" or def_pokemon.type2 == "Fairy":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Poison" or def_pokemon.type2 == "Ground" or def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Ghost":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Steel":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Electric":
            if def_pokemon.type1 == "Flying" or def_pokemon.type1 == "Water":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Grass" or def_pokemon.type1 == "Electric" or def_pokemon.type1 == "Dragon":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Ground":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Flying" or def_pokemon.type2 == "Water":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Grass" or def_pokemon.type2 == "Electric" or def_pokemon.type2 == "Dragon":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Ground":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Ground":
            if def_pokemon.type1 == "Poison" or def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Fire" or def_pokemon.type1 == "Electric":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Bug" or def_pokemon.type1 == "Grass":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Flying":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Poison" or def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Fire" or def_pokemon.type2 == "Electric":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Bug" or def_pokemon.type2 == "Grass":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Flying":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Psychic":
            if def_pokemon.type1 == "Fighting" or def_pokemon.type1 == "Poison":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Psychic":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Dark":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Fighting" or def_pokemon.type2 == "Poison":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Psychic":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Dark":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Rock":
            if def_pokemon.type1 == "Flying" or def_pokemon.type1 == "Bug" or def_pokemon.type1 == "Fire" or def_pokemon.type1 == "Ice":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Fighting" or def_pokemon.type1 == "Ground" or def_pokemon.type1 == "Steel":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Flying" or def_pokemon.type2 == "Bug" or def_pokemon.type2 == "Fire" or def_pokemon.type2 == "Ice":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Fighting" or def_pokemon.type2 == "Ground" or def_pokemon.type2 == "Steel":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Ice":
            if def_pokemon.type1 == "Flying" or def_pokemon.type1 == "Ground" or def_pokemon.type1 == "Grass" or def_pokemon.type1 == "Dragon":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Fire" or def_pokemon.type1 == "Water" or def_pokemon.type1 == "Ice":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Flying" or def_pokemon.type2 == "Ground" or def_pokemon.type2 == "Grass" or def_pokemon.type2 == "Dragon":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Fire" or def_pokemon.type2 == "Water" or def_pokemon.type2 == "Ice":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Bug":
            if def_pokemon.type1 == "Grass" or def_pokemon.type1 == "Psychic" or def_pokemon.type1 == "Dark":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Fighting" or def_pokemon.type1 == "Flying" or def_pokemon.type1 == "Poison" or def_pokemon.type1 == "Ghost" or def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Fire" or def_pokemon.type1 == "Fairy":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Grass" or def_pokemon.type2 == "Psychic" or def_pokemon.type2 == "Dark":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Fighting" or def_pokemon.type2 == "Flying" or def_pokemon.type2 == "Poison" or def_pokemon.type2 == "Ghost" or def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Fire" or def_pokemon.type2 == "Fairy":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Dragon":
            if def_pokemon.type1 == "Dragon":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Steel":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Fairy":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Dragon":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Steel":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Fairy":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Ghost":
            if def_pokemon.type1 == "Ghost" or def_pokemon.type1 == "Psychic":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Dark":
                type1_dmg = 0.5
                effective = 1
            elif def_pokemon.type1 == "Normal":
                type1_dmg = 0
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Ghost" or def_pokemon.type2 == "Psychic":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Dark":
                type2_dmg = 0.5
                effective = 1
            elif def_pokemon.type2 == "Normal":
                type2_dmg = 0
            else:
                type2_dmg = 1

        elif move_used[2] == "Dark":
            if def_pokemon.type1 == "Ghost" or def_pokemon.type1 == "Psychic":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Fighting" or def_pokemon.type1 == "Dark" or def_pokemon.type1 == "Fairy":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Ghost" or def_pokemon.type2 == "Psychic":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Fighting" or def_pokemon.type2 == "Dark" or def_pokemon.type2 == "Fairy":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Steel":
            if def_pokemon.type1 == "Rock" or def_pokemon.type1 == "Ice" or def_pokemon.type1 == "Fairy":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Fire" or def_pokemon.type1 == "Water" or def_pokemon.type1 == "Electric":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Rock" or def_pokemon.type2 == "Ice" or def_pokemon.type2 == "Fairy":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Fire" or def_pokemon.type2 == "Water" or def_pokemon.type2 == "Electric":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        elif move_used[2] == "Fairy":
            if def_pokemon.type1 == "Fighting" or def_pokemon.type1 == "Dragon" or def_pokemon.type1 == "Dark":
                type1_dmg = 2
                effective = 2
            elif def_pokemon.type1 == "Poison" or def_pokemon.type1 == "Steel" or def_pokemon.type1 == "Fire":
                type1_dmg = 0.5
                effective = 1
            else:
                type1_dmg = 1

            if def_pokemon.type2 == "Fighting" or def_pokemon.type2 == "Dragon" or def_pokemon.type2 == "Dark":
                type2_dmg = 2
                effective = 2
            elif def_pokemon.type2 == "Poison" or def_pokemon.type2 == "Steel" or def_pokemon.type2 == "Fire":
                type2_dmg = 0.5
                effective = 1
            else:
                type2_dmg = 1

        crit_hit = random.random()
        if crit_hit <=0.12:
            crit_dmg = 2
            crit = True
        else:
            crit_dmg = 1
            crit = False

        random_hit = random.random()*100
        if random_hit <=2.56:
            random_dmg = 100
        elif random_hit <=5.13:
            dmg = [86,88,91,93,95,97,99]
            random_dmg = dmg[random.randint(0,6)]
        elif random_hit <= 7.69:
            dmg = [85,87,89,90,92,94,96,98]
            random_dmg = dmg[random.randint(0,7)]
        else:
            random_dmg = 93

        if move_used[3] == "Physical":
            damage = (((((((2*level)/5)+2)*int(move_used[6])*(atk_pokemon.atk/def_pokemon.defn))/50)+2)*(crit_dmg*random_dmg*stab*type1_dmg*type2_dmg)/100)
        elif move_used[3] == "Special":
            damage = (((((((2*level)/5)+2)*int(move_used[6])*(atk_pokemon.spA/def_pokemon.spD))/50)+2)*(crit_dmg*random_dmg*stab*type1_dmg*type2_dmg)/100)
        elif move_used[3] == "Status":
            damage = 1
        int_damage = round(damage)
        move_name = move_used[1]
        print(int_damage)


        properties = [int_damage,crit,move_name,effective]
        return properties
    
    def start_screen(self):
        intro = True
        if pygame.mixer.get_init():
            self.music = pygame.mixer.music.load("Music//Gold theme song.wav")
            pygame.mixer.music.play(loops=-1)

        title = self.fontS.render('Pokemon Demo Test',True,(255,203,5))
        title_rect = title.get_rect(x=395,y=35)

        play_button = Button(self,530,100,200,150,(255,203,5),(0,0,0),'Play',("Pokemon Solid.ttf"),100,True,1)
        play_button_outline = Button(self,505,75,250,200,(40,61,112),(0,0,0),"Play",("Pokemon Solid.ttf"),110,True,1)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        intro = False
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play_button.is_pressed(event.pos):
                            intro = False

            self.screen.blit(self.intro_background,(0,0))

            self.screen.blit(title,title_rect)

            self.screen.blit(play_button_outline.image,play_button_outline.rect)
            self.screen.blit(play_button.image,play_button.rect)

            self.clock.tick(self.fps)
            pygame.display.update()

    def text_screen(self):

        trainer_name = self.fontsP.render("Trainer",True,(0,0,0))
        trainer_name_rect = trainer_name.get_rect(x=175,y=580)

        color = (255,255,255)

        text_box = Button(self,90,560,700,200,(0,0,0),(225,225,225),"So you want to battle? Fine!","pokemon_pixel_font.ttf",60,True,1,self.text_box)

        options_y = Button(self,800,585,100,45,(0,0,0),color,"Yes","pokemon_pixel_font.ttf",60,False,1)
        options_outline_y = Button(self,795,580,110,55,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",60,False,1)

        options_n = Button(self,800,660,100,45,(0,0,0),color,"No","pokemon_pixel_font.ttf",60,False,1)
        options_outline_n = Button(self,795,655,110,55,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",60,False,1)


        self.screen.blit(text_box.image,text_box.rect)
        self.screen.blit(trainer_name,trainer_name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if text_box.is_pressed(event.pos):
                        self.screen.blit(options_outline_y.image,options_outline_y.rect)
                        self.screen.blit(options_y.image,options_y.rect)

                        self.screen.blit(options_outline_n.image,options_outline_n.rect)
                        self.screen.blit(options_n.image,options_n.rect)

                    if options_y.is_pressed(event.pos):
                        self.talk_trainer = False
                        self.canEncounter = True
                        self.encountered = True
                        self.trainer_battle = True

                    if options_n.is_pressed(event.pos):
                        self.talk_trainer = False

       
        pygame.display.update()

    def encounter_timer(self):
        while True:
            if self.canEncounter:
                self.random_encounter_chance = random.random()

            else:
                self.random_encounter_chance = 1.1

            time.sleep(random.uniform(1.5, 2.5))





if __name__ == "__main__":
    game = mainGame()

    game.run_game()