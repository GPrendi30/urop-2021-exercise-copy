from ga.DNA import DNA
from config import CHROMOSOME_LENGTH
from track_generator.command import Command
from track_generator.generator import *
import random
import math

class Population:

    # constructor
    def __init__(self, maxPop, mutation_rate, chromosome_length):
        self.maxPop = maxPop
        self.mutation_rate = mutation_rate
        self.population = []
        self.chromosome_length = chromosome_length

    # populate function which generates the starting population
    def populate(self):
        for i in range(self.maxPop):
            # pe -> DNA object
            pe = DNA(chromosome_length=self.chromosome_length)
            # generating genes and genomes
            pe.generate_genes()
            pe.generate_genome()

            # add pe to population
            self.population.append(pe)

    # returns the greates fitness, and the index of the fittest
    def getFittest(self):
        pop = self.population
        max = pop[0].fitness
        max_i = 0

        for i in range(self.maxPop):
            current_fitness = pop[i].fitness

            if current_fitness > max:
                max = current_fitness
                max_i = i

        return [max, max_i]


    # return the average fitness
    def getAvgFitness(self):
        pop = self.population
        avg = 0
        # adds all fitnesses and / by population number
        for i in range(self.maxPop):
            current_fitness = pop[i].fitness
            avg += current_fitness

        return avg / self.maxPop

    # performs natural selection and returns an array with 2 elements(parents)
    def selection(self):
        pop = self.population
        parents = []

        for i in range(0,2):
            parent_found = False

            while not parent_found:
                # randomly generate an index and a probability
                index = random.randint(0, self.maxPop - 1)
                prob = random.randint(0, 100) / 100

                # if prob is lower than fitness, then choose the parent
                if prob < pop[index].fitness:
                    parents.append(pop[index])
                    parent_found = True

        return parents


    # calculates the fitness, for every element in the population
    def calc_fitness(self):
        pop = self.population
        for pe in pop:
            pe.calc_fitness()

    # performs genetic crossover
    # randomly selects the parents
    # randomly finds a midpoint, and copies the genome from parentA start -> midpoint, from parentB midpoint -> end
    def crossover(self, parents):
        p_index = random.randint(0, 1)
        if p_index:
            a_i = 1
            b_i = 0
        else:
            a_i = 0
            b_i = 1

        parentA = parents[a_i]
        parentB = parents[b_i]

        #randomly select a midpoint
        midpoint = random.randint(0, math.floor(minimum(len(parentA.genome), len(parentB.genome)) * 2/3))

        #create the child
        child = DNA(chromosome_length=self.chromosome_length)
        # if parentA.genome[midpoint].command == Command.DY or parentB.genome[midpoint].command == Command.DY:
        #    midpoint -= 1

        #copy genome
        child.genome += parentA.genome[:midpoint]
        child.genome += parentB.genome[midpoint:]

        # randomly find an index to be replaced by the child
        index = random.randint(0, self.maxPop - 1)
        child.genome_to_gene()  # convert the genome to gene
        self.population[index] = child  # put the child in the population


    def mutate(self):

        population = self.population
        mutated = self.maxPop * self.mutation_rate

        for i in range(int(mutated)):
            index = random.randint(0, self.maxPop - 1)
            genome = population[index].genome
            genome_index = random.randint(0, len(genome) - 1)

            command = Command(random.randint(0, 3))
            if command == Command.DY:
                value = random.randint(0, 30)
            else:
                value = 1

            modified_gene = ChromosomeElem(command=command, value=value)
            genome[genome_index] = modified_gene


def minimum(a, b):
    if a <= b:
        return a
    else:
        return b
