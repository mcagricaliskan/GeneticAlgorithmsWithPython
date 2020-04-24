import random

class Genetic:
    def __init__(self, Target, Population_number):
        self.Gene_Pool = '''abcçdefgğhıijklmnoöpqrsştuüvwxyzABCÇDEFGĞHİIJKLMNOÖPQRŞSTUÜVWXYZ 1234567890,.-;:_!"#%&/()=?@${[]}'''
        self.Target = Target
        self.Target_text_lenght = len(Target)
        self.Population_number = Population_number
        self.Population = []
        self.Next_Generation = []
        self.Found = False
        self.Generation_Timer = 0

    class Member:
        def __init__(self,Gene):
            self.Fitness = 0
            self.Gene = Gene

    def random_gene(self):
        Gene = random.choice(self.Gene_Pool)
        return Gene

    def create_genom(self):
        Genom = [self.random_gene() for i in range(self.Target_text_lenght)]
        return Genom

    def Calculate_Fitness(self):
        for Member in self.Population:
            Member.Fitness = 0
            for x in range(self.Target_text_lenght):
                if Member.Gene[x] == self.Target[x]:
                    Member.Fitness += 1
            if Member.Fitness == self.Target_text_lenght:
                self.Found = True


    def Crossover(self):
        last_best = int((90 * self.Population_number) / 100)
        self.Next_Generation = []
        self.Next_Generation.extend(self.Population[last_best:])
        while True:
            if len(self.Next_Generation) < self.Population_number:
                member_1 = random.choice(self.Population[last_best:]).Gene
                member_2 = random.choice(self.Population[last_best:]).Gene
                child = []
                for gene1,gene2 in zip(member_1,member_2):
                    prob = random.random()
                    if prob < 0.47:
                        child.append(gene1)
                    elif prob < 0.94:
                        child.append(gene2)
                    else:
                        child.append(random.choice(self.Gene_Pool))
                self.Next_Generation.append(self.Member(child))
            else:
                break
        self.Population = self.Next_Generation

    def main(self):
        for number in range(self.Population_number):
            self.Population.append(self.Member(self.create_genom()))

        while not self.Found:
            self.Calculate_Fitness()
            self.Population = sorted(self.Population, key=lambda Member: Member.Fitness)
            self.Crossover()
            self.Generation_Timer += 1

        print(f"Did it {self.Generation_Timer} Generation")

Target = "Mustafa Kemal Atatürk"
Population_Number = 200
for i in range(10):
    Go = Genetic(Target, Population_Number)
    Go.main()