from config import CHROMOSOME_LENGTH
from ga.population import Population
import time

def ga(maxPop, mutation_rate, chromosome_length, maxGen):
    pop = Population(maxPop, mutation_rate, chromosome_length=chromosome_length)

    # populating with maxPop elements
    pop.populate()
    i = 0
    for i in range(maxGen):
        # calculating fitness
        pop.calc_fitness()

        # natural selection
        parents = pop.selection()

        # crossover + mutation
        pop.crossover(parents)

        pop.mutate()
        # printing
        print('Gen ' + str(i) + ": ", pop.getFittest()[0], pop.getAvgFitness())

        pop.population[pop.getFittest()[1]].plot()

    pop.population[pop.getFittest()[1]].plot()

ga(maxPop=300, mutation_rate=0.01, maxGen=1500, chromosome_length=24)
