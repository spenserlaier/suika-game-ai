
#structure: neural network with input layer, one hidden layer, and output layer where output is the
#horizontal coordinate to drop the ball
import game_loop
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

def create_neural_network(input_size, output_size=1):
    model = Sequential()
    model.add(Dense(units=64, activation='relu', input_dim=input_size))
    model.add(Dense(units=64, activation='relu', input_dim=input_size))
    #model.add(Dense(units=output_size, activation='sigmoid'))
    model.add(Dense(units=output_size, activation='tanh'))
    model.compile(optimizer=Adam(), loss='mean_squared_error')  
    return model

def initialize_population(population_size, input_size, output_size):
    return [create_neural_network(input_size, output_size) for _ in range(population_size)]

def crossover(parent1, parent2):
    child = create_neural_network(parent1.input_shape[1], parent1.output_shape[1])
    for layer in range(len(child.layers)):
        if np.random.rand() > 0.5:
            child.layers[layer].set_weights(parent1.layers[layer].get_weights())
        else:
            child.layers[layer].set_weights(parent2.layers[layer].get_weights())
    return child

def mutate(network, mutation_rate=0.1):
    for layer in network.layers:
        if np.random.rand() < mutation_rate:
            weights = layer.get_weights()
            for i in range(len(weights)):
                weights[i] += np.random.normal(0, 0.1, size=weights[i].shape)
            layer.set_weights(weights)
    return network

def calculate_fitness(network):
    # TODO: run the game loop with the given network, and continue feeding it inputs 
    # until the game over condition is reached. when that happens, return the score as the
    # general measurement of fitness
    fitness = game_loop.main(network)
    return fitness

# Genetic Algorithm
def genetic_algorithm(population_size, input_size, output_size, generations):
    population = initialize_population(population_size, input_size, output_size)
    for generation in range(generations):
        # Evaluate fitness for each individual in the population
        fitness_scores = [calculate_fitness(network) for network in population]

        # Select parents based on fitness
        parents = [population[i] for i in np.argsort(fitness_scores)[-2:]][::-1]

        # Generate offspring through crossover and mutation
        offspring = [crossover(parents[0], parents[1]) for _ in range(population_size - 2)]
        offspring = [mutate(child) for child in offspring]

        # Replace old population with offspring
        population = parents + offspring

        # Display or store information about the best individual in each generation
        best_network = population[np.argmax(fitness_scores)]
        best_fitness = max(fitness_scores)
        print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

    return best_network

input_size = 21 - 6 - 2
output_size = 1  
#TODO: adjust output so that it's a value within the expected x boundaries
population_size = 10
generations = 50

best_network = genetic_algorithm(population_size, input_size, output_size, generations)

