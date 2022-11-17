import ctypes

class Config:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.screen_width = self.user32.GetSystemMetrics(0)    
        self.screen_height = self.user32.GetSystemMetrics(1)

        self.map = ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                    "B.....................SSSSSSSSSSSSSSSSSSSSSSSSS............B",
                    "B.....................SRRRRRRRRRRRRRRRRRRRRRRRS............B",
                    "B.....................SR...T.....TT......T....S............B",
                    "B.....................SR.SSSSSSSSSSSSSSSSSSSSSS............B",
                    "B.....................SR...................................B",
                    "B.....................SRRRRRRRRRRRRRRRRRRRRRRRRRRRR........B",
                    "B.................................................R........B",
                    "B......GGGGGGGGGGG................................R........B",
                    "B......GGGGGGGGGGG................................R........B",
                    "B......GGGGGGGGGGG................................R........B",
                    "B......GGGGGGGGGGG................................R........B",
                    "B...........T................GGGGGGGGGGGGGGGGGG.T.R........B",
                    "B............................GGGGGGGGGGGGGGGGGG...R........B",
                    "BRRRRRRRRRRRRRRRRRRRRRRRRR...GGGGGGGGGGGGGGGGGG.T.R........B",
                    "B........................R...GGGGGGGGGGGGGGGGGG...R........B",
                    "B........................R...GGGGGGGGGGGGGGGGGG...R..T.....B",
                    "B........................R...GGGGGGGGGGGGGGGGGG...R........B",
                    "B........................R...GGGGGGGGGGGGGGGGGG.T.R........B",
                    "B........................R...GGGGGGGGGGGGGGGGGG...R..T.....B",
                    "B..WWWWWWWWWWWWWWWWWWWW..R........................R........B",
                    "B..WWWWWWWWWWWWWWWWWWWW..RRRRRRRRRRRRRRRRRRRRRRRRRR........B",
                    "B..WWWWWWWWWWWWWWWWWWWW.......T.....T.........T............B",
                    "B..WWWWWWWWWWWWWWWWWWWW....................................B",
                    "B..WWWWWWWWWWWWWWWWWWWW....................................B",
                    "B..WWWWWWWWWWWWWWWWWWWW....................................B",
                    "B..WWWWWWWWWWWWWWWWWWWW....................................B",
                    "B..WWWWWWWWWWWWWWWWWWWW....................................B",
                    "B..WWWWWWWWWWWWWWWWWWWW....................................B",
                    "B..WWWWWWWWWWWWWWWWWWWW....................................B",
                    "B..........................................................B",
                    "B..........................................................B",
                    "B..........................................................B",
                    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]