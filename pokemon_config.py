import ctypes

class Config:
    def __init__(self):

        self.screen_width = 1248  
        self.screen_height = 736

        self.TRAINER_POKEMON_LAYER = 6
        self.POKEMON_LAYER = 5
        self.TRAINER_INTRO_LAYER = 4
        self.PLAYER_LAYER = 4
        self.GRASS_LAYER = 3
        self.ENEMY_LAYER = 3
        self.BLOCK_LAYER = 2
        self.GROUND_LAYER = 1

        self.TILESIZE = 32

        self.map = ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                    "B..........................................................B",
                    "B..........GGG.............................................B",
                    "B........GGGGGGG...........................................B",
                    "B.......GGGGGGGGG............T.......T.....................B",
                    "B.......GGGGGGGGG..................................T.......B",
                    "B......GGGGGGGGGGG.........................................B",
                    "B......GGGGGGGGGGG...............T.........................B",
                    "B......GGGGGGGGGGG.........................................B",
                    "B.......GGGGGGGGG..........................................B",
                    "B.......GGGGGGGGG..........................................B",
                    "B........GGGGGGG...P.......................................B",
                    "B..........GGG...............GGGGGGGGGGGGGGGGGG...T...T....B",
                    "B............................GGGGGGGGGGGGGGGGGG............B",
                    "B............................GGGGGGGGGGGGGGGGGG............B",
                    "B.....T..T..T..T..T..........GGGGGGGGGGGGGGGGGG...T...T....B",
                    "B............................GGGGGGGGGGGGGGGGGG............B",
                    "B.............G..............GGGGGGGGGGGGGGGGGG............B",
                    "B............GGG.............GGGGGGGGGGGGGGGGGG...T...T....B",
                    "B............GGG.............GGGGGGGGGGGGGGGGGG............B",
                    "B............GGG...........................................B",
                    "B............GGG...........................................B",
                    "B............GGG...........................................B",
                    "B............GGG.........T...T...T...T...T...T...T.........B",
                    "B............GGG...........................................B",
                    "B............GGG...........................................B",
                    "B............GGG...........................................B",
                    "B.........GGGGGGGGG........................................B",
                    "B........GGGGGGGGGGG.......................................B",
                    "B.......GGGGGG.GGGGGG......................................B",
                    "B.......GGGGGG.GGGGGG......................................B",
                    "B........GGGG...GGGG.......................................B",
                    "B.........GG.....GG........................................B",
                    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]