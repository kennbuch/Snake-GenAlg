from model import NN
from sklearn import preprocessing
from tqdm import tqdm
from time import sleep
from window import randomFood
from snake import Snake, Cube
from tqdm import tqdm
from math import floor
import numpy as np
import multiprocessing

class GeneticAlgorithm():

    def __init__(self, pop_size, rows, randomize_weights=True, input_file=None):
        # layer layout of each NN
        layers = [24, 16, 16, 4]

        # calculate the number of genes in a dna strand 
        self.dna_size = 0
        for i in range(1, len(layers)):
            self.dna_size += layers[i-1] * layers[i]

        # initialize the population 
        self.population = np.empty(pop_size, dtype=NN)
        for i in range(pop_size):
            self.population[i] = NN(layers, self.dna_size)
        
        # insert the given weights if the user so chooses
        if not randomize_weights:
            self.population[0].set_weights(np.loadtxt('data.csv', delimiter=','))

        # size of the field
        self.rows = rows

    def test_individual(self, brain, length_arr, fitness_arr=None):
        
        snake = Snake(self.rows, self.rows)               # the snake 
        food = Cube(randomFood(self.rows, snake))         # initial food 
        directions = ['up', 'down', 'left', 'right']      # directions the snake can move
        fitness = 0                                       # fitness score for this snake (+0.7 - finding food, +0.1 - getting closer to food, -0.2 getting farther from food)
        hunger = 0                                        # hunger score, when it reaches 60 the snake dies
        distance_to_food = snake.distance_to_food(food)   # distance the snake's head is to the food

        while hunger < 100:  
            x = np.array([snake.get_NN_input(food)])      # retrieve the input
            y = brain.predict(x, get_index=True)          # pass in input and choose next move
            direction = directions[y]

            if not snake.move(direction):                 # the snake dies
                break
            if snake.head.pos == food.pos:                # the snake finds the food
                fitness += 0.7
                hunger = 0                                
                snake.grow()                              
                food = Cube(randomFood(self.rows, snake)) 
            else:                                         # the snake doesn't find the food nor dies                        
                new_distance_to_food = snake.distance_to_food(food)
                if new_distance_to_food < distance_to_food:
                    fitness += 0.1                        
                else: 
                    fitness -= 0.2                        
                distance_to_food = new_distance_to_food
                hunger += 1
        
        length_arr.append(len(snake.body))
        if fitness_arr:
            fitness_arr.append(fitness)
        


    def test_population(self, pop_size):
        lengths = []
        fitness_scores = []

        for brain in self.population:
            self.test_individual(brain, lengths, fitness_scores)

        return fitness_scores, np.average(lengths)

    def breed(self, scores):
        scores_sum = np.sum(scores)             # sum of the top fitness scores
        breeding_probs = scores / scores_sum    # each specimen has a probability proportional to its fitness score to breed
        breeding_pool_size = self.population.size - scores.size
        parents_pool_size = scores.size


        # randomly sample two different breeding pools of parents
        breeding_pool = np.random.choice(self.population[:parents_pool_size], 
                                         size=breeding_pool_size*2, p=breeding_probs)

        # breed the parents from each breeding pool and add their children to the population
        for i, (parent1, parent2) in enumerate(zip(breeding_pool[:breeding_pool_size], 
                                                   breeding_pool[breeding_pool_size:])):
            offspring_dna = self.crossover(parent1, parent2)                        # build the child DNA by crossing over the parents DNA
            self.mutate(offspring_dna, 0.01)                                        # mutate the offspring DNA with a specified mutation rate
            self.inject_dna(offspring_dna, self.population[parents_pool_size + i])  # recycle the old specimines by injecting the new DNA 
    
    def crossover(self, p1, p2):
        p1_dna = self.extract_dna(p1)       # parent 1 dna strand
        p2_dna = self.extract_dna(p2)       # parent 2 dna strand
        child_dna = np.zeros(p1_dna.size, dtype=np.float32)

        # the child DNA is created by alternating which parent the next gene comes from
        #   ie. child_dna = [p1 gene 1, p2 gene 2, p1 gene 3, p2 gene 4, ...]
        j = 0   
        parents = [p1_dna, p2_dna]          
        for i in range(self.dna_size):
            child_dna[i] = parents[j][i]
            j = 1 if j == 0 else 0

        return child_dna

    def mutate(self, dna, mutation_rate):
        # a list of whether or not a gene will be mutated
        mutation_vals = np.random.choice([True, False], dna.size, p=[mutation_rate, 1-mutation_rate])

        # genes are mutated by flipping its bit
        for i, mutate in enumerate(mutation_vals):
            if mutate: 
                dna[i] = np.random.randint(-127, 128)

    def extract_dna(self, specimen, bit=False):
        return specimen.get_weights()

    def inject_dna(self, dna, specimen):
        specimen.set_weights(dna)

    def get_breeders(self, scores, ratio):
        # find the point where the scores array turns negative
        cut_negs = scores.size
        for i in range(scores.size):
            if scores[i] < 0:
                cut_negs = i
                break
        
        # return the 
        breeders = scores[0:cut_negs] 
        num_breeders = int(scores.size * ratio)
        if breeders.size < num_breeders:
            return breeders
        else: 
            return breeders[0:num_breeders]
