import pygame
import random


pygame.init()

class GameCore():
    def __init__(self, Bird_Population_Number = 1):
        self.screen_width = 512
        self.screen_height = 288
        self.window = pygame.display.set_mode((self.screen_height, self.screen_width))
        pygame.display.set_caption("Flappy Bird")
        self.Clock = pygame.time.Clock()
        self.GameStatus = "Game"


        ####### BackGround ########
        self.BackGroundDay = pygame.image.load("Data/sprites/background-day.png").convert_alpha()
        self.BackGroundNight = pygame.image.load("Data/sprites/background-night.png").convert_alpha()
        self.BackGroundList = [self.BackGroundDay, self.BackGroundNight]
        self.BackGround = self.BackGroundList[random.randint(0, 1)]
        self.BackGround_X = 0
        self.BackGround_Y = 0

        self.Ground = pygame.image.load("Data/sprites/base.png").convert_alpha()
        self.Ground_X = 0
        self.Ground_Y = 400
        self.Ground_X2 = 336
        self.Ground_Y2 = 400

        ####### Bird ########


        self.BirdImage = pygame.image.load("Data/sprites/yellowbird-midflap.png").convert_alpha()

        ###### Genetic Thinks ########

        self.Best_Fitness = 1

        ##### PIPE ######
        self.pipe_list = []
        self.PIPEIMAGE = pygame.image.load("Data/sprites/pipe-green.png").convert_alpha()
        self.PipeAnimationTime = pygame.time.get_ticks()
        self.PipeAnimationDelay = 0
        self.BirdAnimationTime = pygame.time.get_ticks()
        self.BirdAnimation = 0

        ##### GENETİC ######

        self.Next_Generation_List = []
        self.Generation = 0
        self.Bird_Population = []
        self.Bird_Population_Number = Bird_Population_Number

        for x in range(Bird_Population_Number):
            self.Bird_Population.append(self.Bird(self.BirdImage))


    class Bird:
        def __init__(self,Image):
            self.Bird_X = 50
            self.Bird_Y = 50
            self.Gravity = 0.75
            self.acc = 0.075
            self.BirdAnimationTime = pygame.time.get_ticks()
            self.BirdAnimation = 0
            self.BirdFitness = 0
            self.BirdImage = Image
            self.BirdImageMask = pygame.mask.from_surface(self.BirdImage)
            self.Score = 0

        def DNA(self):
            pass

        def DrawBird(self,window):
            window.blit(self.BirdImage, (self.Bird_X, self.Bird_Y))

    class Pipe():
        def __init__(self, pipe_X, pipe_Y, PipeImage):
            self.pipe_X = pipe_X
            self.pipe_Y = pipe_Y
            self.lower_pipe = PipeImage
            self.upper_pipe = pygame.transform.flip(self.lower_pipe, False, True)

            self.lower_pipe_mask = pygame.mask.from_surface(self.lower_pipe)
            self.upper_pipe_mask = pygame.mask.from_surface(self.upper_pipe)

        def DrawPipe(self, window):
            window.blit(self.lower_pipe, (self.pipe_X, self.pipe_Y))
            window.blit(self.upper_pipe, (self.pipe_X, self.pipe_Y - 420))

        def MovePipe(self):
            self.pipe_X -= 2

    def MaskCollision(self, Masked_Image1, Image1_X, Image1_Y, Masked_Image2, Image2_X, Image2_Y):
        offset = (round(Image2_X - Image1_X), round(Image2_Y - Image1_Y))
        result = Masked_Image1.overlap(Masked_Image2, offset)
        return result

    def Kill_The_Bird(self,bird):
        if bird.Score >= self.Best_Fitness:
            self.Next_Generation_List.append(bird)
            self.Bird_Population.remove(bird)
        else:
            self.Bird_Population.remove(bird)

    def NextGeneration(self, Next_Generation_List):
        pass

    def Draw(self):

        self.window.blit(self.BackGround, (self.BackGround_X, self.BackGround_Y))

        if self.GameStatus == "Start":
            self.window.blit(self.GameStartImage, (50, 50))
        if self.GameStatus == "Game":

            for pipe in self.pipe_list:
                pipe.DrawPipe(self.window)
            for bird in self.Bird_Population:
                bird.DrawBird(self.window)
            #self.window.blit(self.ScorFont.render("" + str(self.Score), True, (255, 255, 255)), (120, 50))

        self.window.blit(self.Ground, (self.Ground_X, self.Ground_Y))
        self.window.blit(self.Ground, (self.Ground_X2, self.Ground_Y2))

        self.Clock.tick(60)

        pygame.display.update()

    def GameLoop(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Close"
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         if self.GameStatus == "Start":
            #             self.GameStatus = "Game"
            #         if self.GameStatus == "Game":
            #             self.Gravity = random.random(-2,-3) #-2.8
            #             pygame.mixer.Channel(0).play(pygame.mixer.Sound("Data/audio/wing.ogg"))
            #         if self.GameStatus == "GameOver":
            #             self.GameStatus == "Start"



        print(len(self.Bird_Population))


        self.Tus = pygame.key.get_pressed()
        if self.Tus[pygame.K_ESCAPE]:
            return "Close"

        if self.GameStatus == "Game":




            ######### Gravity ###########
            for Bird in self.Bird_Population:
                Bird.Bird_Y += Bird.Gravity
                Bird.Gravity += Bird.acc

                if Bird.Bird_Y > 380:
                    self.Kill_The_Bird(Bird)


            ######## Ground Control ######

            self.Ground_X -= 2
            self.Ground_X2 -= 2

            if self.Ground_X == -336:
                self.Ground_X = 336

            if self.Ground_X2 == -336:
                self.Ground_X2 = 336

            ######## PIPE ###########
            if pygame.time.get_ticks() - self.PipeAnimationTime > self.PipeAnimationDelay:
                self.pipe_list.append(self.Pipe(300, random.randint(180, 320), self.PIPEIMAGE))
                self.PipeAnimationTime = pygame.time.get_ticks()
                self.PipeAnimationDelay = 1200

            for pipe in self.pipe_list:
                pipe.MovePipe()
                for bird in self.Bird_Population:
                    collision_lower = self.MaskCollision(bird.BirdImageMask, bird.Bird_X, bird.Bird_Y,
                                                         pipe.lower_pipe_mask, pipe.pipe_X, pipe.pipe_Y)
                    collision_upper = self.MaskCollision(bird.BirdImageMask, bird.Bird_X, bird.Bird_Y,
                                                         pipe.upper_pipe_mask, pipe.pipe_X, pipe.pipe_Y - 420)

                    if collision_lower != None or collision_upper != None:
                        self.Kill_The_Bird(bird)



                    if bird.Bird_X + 17 == pipe.pipe_X:
                        bird.Score += 1

                if pipe.pipe_X == -52:
                    self.pipe_list.remove(pipe)


                if len(self.Bird_Population) == 0:
                    self.Generation += 1
                    self.NextGeneration(self.Next_Generation_List)



            #print(self.Score)

        self.Draw()

Bird_Population_Number = 100
Game = GameCore(Bird_Population_Number)

while True:
    GameStatus = Game.GameLoop()
    if GameStatus == "Close":
        break

pygame.quit()
