import pygame
import random
import time


pygame.init()

class Bird:
    def __init__(self,Bird_Image, Bird_Mask):
        self.Bird_X = 50
        self.Bird_Y = 50
        self.Gravity = 0.78
        self.acc = 0.075
        self.Bird_Image = Bird_Image
        self.Bird_Mask = Bird_Mask

        self.Score = 0 # Fitness of bird
        self.Pipe_Y = 0
        self.Pipe_distance = 0


    def Draw_Bird(self,window):
        window.blit(self.Bird_Image,(self.Bird_X, self.Bird_Y))

class Pipe:
    def __init__(self, Pipe_X, Pipe_Y, Pipe_id,Upper_Image,Lower_Image, Upper_Mask, Lower_Mask):
        self.Pipe_X = Pipe_X
        self.Pipe_Lower_Y = Pipe_Y
        self.Pipe_Upper_Y = self.Pipe_Lower_Y - 420
        self.Pipe_id = Pipe_id

        self.Upper_Pipe_Image = Upper_Image
        self.Lower_Pipe_Image = Lower_Image

        self.Upper_Pipe_Mask = Upper_Mask
        self.Lower_Pipe_Mask = Lower_Mask

    def Draw_Pipe(self,window):
        window.blit(self.Lower_Pipe_Image,(self.Pipe_X, self.Pipe_Lower_Y))
        window.blit(self.Upper_Pipe_Image,(self.Pipe_X, self.Pipe_Upper_Y))

    def Move_Pipe(self,id, GameSpeed):
        if self.Pipe_X == -52:
            self.Pipe_X = 548
            self.Pipe_id = id
            return id
        else:
            self.Pipe_X -= 1 * GameSpeed



class GameCore:
    def __init__(self, Population_Number = 1):
        self.window_height = 288
        self.window_width = 512
        self.window = pygame.display.set_mode((self.window_height,self.window_width))
        self.Clock = pygame.time.Clock()
        self.GameSpeed = 2

        self.BackGround = pygame.image.load("assets/background.png").convert()

        self.Base = pygame.image.load("assets/base.png").convert()

        self.Pipe_lower_Image = pygame.image.load("assets/pipe.png").convert_alpha()
        self.Pipe_upper_Image = pygame.transform.flip(self.Pipe_lower_Image, False, True)
        self.Pipe_lower_Mask = pygame.mask.from_surface(self.Pipe_lower_Image)
        self.Pipe_upper_Mask =pygame.mask.from_surface(self.Pipe_upper_Image)

        self.Pipe_Number = 0


        self.Bird_Image = pygame.image.load("assets/bird.png").convert_alpha()
        self.Bird_Mask = pygame.mask.from_surface(self.Bird_Image)


        self.Pipe_List = [
            Pipe(300, random.randint(180,320), 1, self.Pipe_upper_Image, self.Pipe_lower_Image,
                 self.Pipe_upper_Mask, self.Pipe_lower_Mask),
            Pipe(450, random.randint(180, 320), 2, self.Pipe_upper_Image, self.Pipe_lower_Image,
                 self.Pipe_upper_Mask, self.Pipe_lower_Mask),
            Pipe(600, random.randint(180, 320), 3, self.Pipe_upper_Image, self.Pipe_lower_Image,
                 self.Pipe_upper_Mask, self.Pipe_lower_Mask),
            Pipe(750, random.randint(180, 320), 3, self.Pipe_upper_Image, self.Pipe_lower_Image,
                 self.Pipe_upper_Mask, self.Pipe_lower_Mask)


        ]


        ### Genetic ####

        self.Population = []
        self.Next_Generation = []
        self.Population_Number = Population_Number

        for i in range(self.Population_Number):
            self.Population.append(Bird(self.Bird_Image,self.Bird_Image))

        self.Deneme = []

    def Draw(self):

        self.window.blit(self.BackGround,(0,0))
        self.window.blit(self.Base,(0, 400))

        for pipe in self.Pipe_List:
            pipe.Draw_Pipe(self.window)

        for i in self.Population:
            i.Draw_Bird(self.window)

        self.Clock.tick(60)
        pygame.display.update()


    def GameLoop(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Close"

        self.Tus = pygame.key.get_pressed()
        if self.Tus[pygame.K_ESCAPE]:
            return "Close"

        self.FPS = str(int(self.Clock.get_fps()))
        pygame.display.set_caption(f"Fps : {self.FPS}")

        for pipe in self.Pipe_List:
            pipe.Move_Pipe(self.Pipe_Number,self.GameSpeed)

            for Member in self.Population:
                if Member.Bird_X + 16 == pipe.Pipe_X:
                    Member.Score += 1

        # self.Deneme = []
        # for x in self.Population:
        #     self.Deneme.append(x.Score)
        # print(self.Deneme)


        self.Draw()



Game = GameCore()
while True:
    GameStatus = Game.GameLoop()
    if GameStatus == "Close":
        break

pygame.quit()