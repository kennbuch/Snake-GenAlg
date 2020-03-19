from tqdm import tqdm
from genetic_algorithm import GeneticAlgorithm
from snake import Snake, Cube
from window import visual
import numpy as np 
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # retrive user input 
    population_size = int(input('population size (integer > 0): '))
    training_iterations = int(input('training iterations (integer >= 0/enter 0 to not train): '))
    test_iterations = int(input('testing iterations (integer >= 0/enter 0 to not test): '))
    randomize_weights_input = bool(input('would you like to randomize the initial weights (Y/N): '))
    randomize_weights = None
    if randomize_weights_input == 'Y' or randomize_weights_input == 'y':
        randomize_weights = True
    elif randomize_weights_input == 'N' or randomize_weights_input == 'n':
        randomize_weights = False

    if not randomize_weights:
        input_file = input('choose the csv file you want to imort the weights from (eg: "data.csv"): ')

    save_weights = input('would you like to save the final weights of the best snake? (Y/N): ')
    save_weights = None
    if save_weights == 'Y' or save_weights == 'y':
        save_weights = True
    elif save_weights == 'N' or save_weights == 'n':
        save_weights = False

    if save_weights:
        output_file = input('choose the csv file you want to save the weights to (eg: "data.csv"): ')

    input('press enter to begin: ')

    ga = GeneticAlgorithm(population_size, 20, randomize_weights=randomize_weights, input_file=input_file)
    
    if training_iterations > 0:
        print("Training...")
        for i in tqdm(range(training_iterations)):
            fitness_scores, avg_length = ga.test_population(population_size)
            fitness_scores = np.array(fitness_scores)

            sort_scores = fitness_scores.argsort()
            fitness_scores = fitness_scores[sort_scores[::-1]]
            ga.population = ga.population[sort_scores[::-1]]

            breeders = ga.get_breeders(fitness_scores, 0.02)
            if breeders.size < 2:
                ga = GeneticAlgorithm(population_size, 20)
            else:
                ga.breed(breeders)
    
    if test_iterations > 0:
        print("Testing...")

        testing_lengths = []

        for _ in tqdm(range(test_iterations)):
            ga.test_individual(ga.population[0], testing_lengths)

        print(f"average length {np.mean(testing_lengths)}, max length: {np.amax(testing_lengths)}")

    if save_weights:
        np.savetxt(output_file, ga.population[0].get_weights(), delimiter=',')

    visual(brain=ga.population[0], human_player=False)
