import random
import time

class Genetic:
    def __init__(self, population_number,targeted_text):

        self.Population_Number = population_number
        self.Population = []
        self.Next_Generation = []
        self.List_of_letters = "abcçdefgğhıijklmnoöprşstuüvyzqABCÇDEFGĞHIİJKLMNOÖPRŞSTUÜVYZQ "
        self.Targeted_Text = targeted_text
        self.Targeted_Text_Lenght = len(self.Targeted_Text)
        self.Done = True
        self.Winner = ""
        self.Generation_Timer = 0
        self.Weak_Fitness = 0
        self.Mutation_Rate = 1

    class DNA:
        def __init__(self, Gen):
            self.GEN = Gen
            self.Score = 0

    def create_population(self):

        while True:
            random_word = ""
            for i in range(self.Targeted_Text_Lenght):
                random_word += random.choice(self.List_of_letters)
            self.Population.append(self.DNA(random_word))

            if len(self.Population) == self.Population_Number:
                break

    def fitness(self):
        for member in self.Population:
            score_of_gen = 0
            for x in range(len(member.GEN)):
                if member.GEN[x] == self.Targeted_Text[x]:
                    score_of_gen += 1
            member.Score = score_of_gen

    def Selection(self):
        for member in self.Population:
            if member.GEN == self.Targeted_Text:
                self.Winner = str(member.GEN)
                self.Done = False
            elif member.Score <= self.Weak_Fitness:
                self.Population.remove(member)

    def Mutation(self):
        for member in self.Population:
            number_of_text = 0
            if random.randint(0,100) < self.Mutation_Rate:
                number_of_text = random.randint(0,len(self.Targeted_Text)-1)
                text = list(member.GEN)
                text[number_of_text] = random.choice(self.List_of_letters)
                text = "".join(text)
                #print(f" text = {text}")
                member.GEN = text

    def Crossover(self):
        while True:
            if len(self.Population) < self.Population_Number:
                new_chield_text = ""
                new_chield_text_2 = ""
                random_member_parent_1 = random.choice(self.Population)
                random_member_parent_2 = random.choice(self.Population)
                mid_point = random.randint(1, self.Targeted_Text_Lenght - 1)
                new_chield_text += random_member_parent_1.GEN[:mid_point]
                new_chield_text += random_member_parent_2.GEN[mid_point:]
                new_chield_text_2 += random_member_parent_2.GEN[:mid_point]
                new_chield_text_2 += random_member_parent_1.GEN[mid_point:]
                self.Population.append(self.DNA(new_chield_text))
                self.Population.append(self.DNA(new_chield_text_2))
            else:
                break


    def Weakness_level(self):
        list_of_weaks = []
        for member in self.Population:
            list_of_weaks.append(member.Score)
        # if list_of_weaks.count(self.Weak_Fitness) == self.Population_Number:
        #     self.Mutation_Rate += 2
        #     print("we did it")
        # print(list_of_weaks.count(self.Weak_Fitness))
        #print(self.Mutation_Rate)
        if list_of_weaks.count(self.Weak_Fitness) == 0 and self.Weak_Fitness < self.Targeted_Text_Lenght - 1:
            self.Weak_Fitness += 1
        if self.Weak_Fitness == self.Targeted_Text_Lenght - 1 and self.Done == True:
            self.Weak_Fitness = 0

    def main(self):
        self.create_population()
        startTime = time.time()
        while self.Done:
            self.fitness()
            self.Selection()
            self.Crossover()
            self.Mutation()
            self.Weakness_level()
            self.Generation_Timer += 1
        Time = time.time() - startTime
        print(f"Your target = {self.Targeted_Text}, found = {self.Winner}"
              f"\nGeneration Timer = {self.Generation_Timer}"
              f" Take = {Time} seconds")
for i in range(10):
    Program = Genetic(100,"Mustafa Kemal Atatürk")
    Program.main()
