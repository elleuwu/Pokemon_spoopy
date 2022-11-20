from asyncio.windows_events import NULL
from logging import exception
import pygame,sys,random,time,threading,cv2,numpy as np, os

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
        self.screen = pygame.display.set_mode((self.config.screen_width,self.config.screen_height),pygame.NOFRAME)
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

        self.grass_encounter_video = cv2.VideoCapture('Videos\\Trainer encounter.mp4')
        self.grass_success, self.grass_encounter_frame = self.grass_encounter_video.read()
        self.grass_encounter_frame = cv2.resize(self.grass_encounter_frame,(1248,736))
        self.grass_shape = self.grass_encounter_frame.shape[1::-1]

        self.encountered = False
        self.battle_music = False
        self.in_battle = False
        self.turn = 500
        self.text_state = 0
        self.mainText = NULL
        self.intro_anim = False

        self.battle_music_list = ["Music\\Necrozma battle song.wav","Music\\Vs blue battle song.wav","Music\\Vs cyrus battle song.wav","Music\\Zekrom reshiram battle song.wav"]


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
        self.music = pygame.mixer.music.load("Music//Viridian city theme.wav")
        pygame.mixer.music.play(loops=-1)
        while True:
            if self.talk_trainer == True:
                self.text_screen()
                self.events()
                self.updates()

            elif self.canEncounter == True:
                if not self.in_battle:
                    self.encounter_events()
                    self.updates()
                    self.wild_battle()
                else:
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

        if self.canEncounter == True:
            if not self.enc_timer_started:
                print("thread started")
                self.enc_timer_started = True
                self.enc_timer.start()





    def wild_battle(self):
        if self.random_encounter_chance <= 0.9:
            self.encountered = True

        if self.encountered == True:
            self.wild_pokemon = self.random_pokemon()
            self.encountered_pokemon = Pokemon(self,self.config,24,7,self.wild_pokemon)
            self.draw_encounter()
            self.in_battle = True
            self.turn = 0
            self.mainText = Button(self,15,581,750,150,(0,0,0),(230,230,230),"","pokemon_pixel_font.ttf",70,False,2)
            self.mainTextOutline = Button(self,10,576,760,160,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.dawn = DawnThrowPokemon(self,self.config,0,13)
            self.dawnPokemon = DawnPokemon(self,self.config,2,8,(1280,1360,80,80))

            self.fight = Button(self,800,576,200,70,(0,0,0),(230,230,230),"Fight","pokemon_pixel_font.ttf",70,False,2)
            self.fightOutline = Button(self,795,571,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.bag = Button(self,1015,576,200,70,(0,0,0),(230,230,230),"Bag","pokemon_pixel_font.ttf",70,False,2)
            self.bagOutline = Button(self,1010,571,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.Pokemon = Button(self,800,661,200,70,(0,0,0),(230,230,230),"Pokemon","pokemon_pixel_font.ttf",70,False,2)
            self.PokemonOutline = Button(self,795,656,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

            self.run = Button(self,1015,661,200,70,(0,0,0),(230,230,230),"Run","pokemon_pixel_font.ttf",70,False,2)
            self.runOutline = Button(self,1010,656,210,80,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",70,False,2)

        else:
            self.draw()

    def random_pokemon(self):
        random_pokemon_num = random.randint(0,493)
        pkmn_y = ((random_pokemon_num*80)//2240)
        pkmn_x = (random_pokemon_num-(28*(pkmn_y)))
        rect = pygame.Rect((pkmn_x*80)-80,pkmn_y*80,80,80)
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
        background_rect = self.battle_background.get_rect()
        background = pygame.Surface((background_rect.width,background_rect.height))
        background.blit(self.battle_background,background_rect)

        if self.turn == 0:
            self.mainText.text_state(self.text_state)
            while self.grass_success:
                if self.encountered==True:
                    if self.battle_music:
                        pass
                    else:
                        song = random.randint(0,3)
                        self.music = pygame.mixer.music.load(self.battle_music_list[song])
                        pygame.mixer.music.play(loops=-1)
                        self.battle_music = True

                self.clock.tick(self.fps)
                try:
                    self.grass_success, self.grass_encounter_frame = self.grass_encounter_video.read()
                    self.grass_encounter_frame = cv2.resize(self.grass_encounter_frame,(1248,736))
                    surface = pygame.image.frombuffer(self.grass_encounter_frame.tobytes(), self.grass_shape, "BGR")
                    surface.set_colorkey((15,250,5))
                    self.screen.blit(surface,(0, 0))
                    pygame.display.update()
                
                except:
                    self.grass_success = False

                pygame.display.update()

            self.screen.blit(background,(0,0))

            if self.text_state >= 4:
                self.trainer_pokemon_group.draw(self.screen)
            if self.text_state == 5:
                self.screen.blit(self.fightOutline.image,self.fightOutline.rect)
                self.screen.blit(self.fight.image,self.fight.rect)
                self.screen.blit(self.bagOutline.image,self.bagOutline.rect)
                self.screen.blit(self.bag.image,self.bag.rect)
                self.screen.blit(self.PokemonOutline.image,self.PokemonOutline.rect)
                self.screen.blit(self.Pokemon.image,self.Pokemon.rect)
                self.screen.blit(self.runOutline.image,self.runOutline.rect)
                self.screen.blit(self.run.image,self.run.rect)
            
            if self.intro_anim == False:
                self.screen.blit(self.mainTextOutline.image,(self.mainTextOutline.rect))
                self.screen.blit(self.mainText.image,(self.mainText.rect))

            if self.intro_anim == True:
                self.trainer_intro_group.draw(self.screen)



            self.clock.tick(self.fps)
            self.battle_sprite_group.draw(self.screen)
        pygame.display.update()
   



    def start_screen(self):
        intro = True

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
        trainer_name_rect = trainer_name.get_rect(x=175,y=600)

        color = (255,255,255)

        text_box = Button(self,90,580,700,200,(0,0,0),(225,225,225),"So you want to battle? Fine!","pokemon_pixel_font.ttf",60,True,1,self.text_box)

        options_y = Button(self,800,615,100,45,(0,0,0),color,"Yes","pokemon_pixel_font.ttf",60,False,1)
        options_outline_y = Button(self,795,610,110,55,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",60,False,1)

        options_n = Button(self,800,680,100,45,(0,0,0),color,"No","pokemon_pixel_font.ttf",60,False,1)
        options_outline_n = Button(self,795,675,110,55,(0,0,0),(0,0,0),"","pokemon_pixel_font.ttf",60,False,1)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

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
                        pass
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