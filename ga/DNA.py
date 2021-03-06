#importing needed modules
from config import CHROMOSOME_LENGTH
from ga.chromosome_elem import ChromosomeElem
from track_generator.command import Command
from track_generator.generator import *

import matplotlib.pyplot as plt
import random

# DNA class that contains all the information about an individual:
class DNA:

    # constructor
    def __init__(self, chromosome_length):
        # the length of the DNA
        self.chromosome_length = chromosome_length
        self.dna_length = chromosome_length

        # gene of the DNA
        self.gene = []
        # track is the array that stores the points coordinates
        self.track = []
        # fitness of the individual
        self.fitness = 0
        # genome is the string representation of the gene
        self.genome = []

    # generate genes, based on rules specified on the exercise Readme.md
    def generate_genes(self):

        commandS_poss = [0, 1, 2, 3]  # if the command is S the next command can be anything
        commandDY_poss = [1, 2]        # if the command is DY the next command is L or R
        commandR_L_poss = [0, 3]       # if the command is L or R the next command is S or DY

        # start is a S command
        start = ChromosomeElem(Command.S, random.randint(1, self.dna_length))
        self.gene.append(start)
        self.dna_length -= start.value # add



        while self.dna_length > 1:
            prev_command = self.gene[-1].command

            # checks for the previous command and randomly selects the next command
            if prev_command == Command.S:
                command = Command(commandS_poss[random.randint(0, len(commandS_poss) - 1)])
                if command == Command.DY:
                    value = random.randint(1, 4000) / 100  # generate the degree of turn
                else:
                    value = random.randint(1, self.dna_length)

            elif prev_command == Command.L or prev_command == Command.R:
                command = Command(commandR_L_poss[random.randint(0, 1)])
                if command == Command.DY:
                    value = random.randint(1, 4000) / 100  # generate the degree of turn
                else:
                    value = random.randint(1, self.dna_length)

            elif prev_command == Command.DY:
                command = Command(commandDY_poss[random.randint(0, len(commandDY_poss) - 1)])
                value = random.randint(1, self.dna_length) # generate the degree of turn

            # creates the chromosome object with command and value
            ce = ChromosomeElem(command, value)
            self.gene.append(ce)  #adds it to the gene
            if ce.command != command.DY:
                self.dna_length -= ce.value  # decrease the dna_length

        # add the end point of the gene
        end = ChromosomeElem(Command.S, 1)
        self.gene.append(end)
        self.dna_length -= end.value



    def generate_genome(self):
        # generating the array of commands with value 1.0
        for i in self.gene:
            value = i.value
            if i.command != Command.DY:
                for j in range(value):
                    unit = ChromosomeElem(command=i.command, value=1) # unit Chromosome object with value = 1
                    self.genome.append(unit)
            else:
                unit = ChromosomeElem(command=i.command, value= i.value)
                self.genome.append(unit)


    # return genome(list of unit Chomosome) to gene
    def genome_to_gene(self):
        genome = self.genome
        count = 1
        for i in range(len(self.genome)):
            if i == len(self.genome) - 1:
                count += 1
                ce = ChromosomeElem(command=genome[i - 1].command, value=count)
                self.gene.append(ce)

            else:

                if genome[i].command == genome[i + 1].command:
                    count += 1

                else:
                    if genome[i].command == Command.DY:
                        ce = ChromosomeElem(command=genome[i].command, value=genome[i].value)
                        self.gene.append(ce)
                        count = 1
                    else:
                        ce = ChromosomeElem(command=genome[i].command, value=count)
                        self.gene.append(ce)
                        count = 1


    # generates the coordinates of the points, and calculates the fitness
    def calc_fitness(self):
        self.track = generate_track(self.gene)  # generate the track

        track = self.track
        start = track[0]   # start vector
        end = track[-1]    # end vector
        # calculating the distance
        dist = math.sqrt(math.pow(end.x - start.x, 2) + math.pow(end.y - start.y, 2))

        # calculating fitness
        self.fitness = (1 / (dist * dist)) * 10

    def print_track(self):
        for i in self.track:
            print(i)

    def print_genes(self):
        for i in self.gene:
            print(i)

    def print_genome(self):
        for i in self.genome:
            print(i)

    def plot(self):
        track_points = self.track
        
        start = track_points[0]
        end = track_points[-1]
        plot_x = [track_point.x for track_point in track_points]
        plot_y = [track_point.y for track_point in track_points]
        
        plt.scatter(plot_x, plot_y)
        plt.scatter(start.x, start.y, color="red")
        plt.scatter(end.x, end.y, color="black")
        plt.show()
