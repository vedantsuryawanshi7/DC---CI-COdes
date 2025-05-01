import numpy as np
import random

# Fitness Function: Maximizing the sum of 1s in the binary string
def fitness(antibody):
    return sum(antibody)  # Higher sum means better solution

# Generate a Random Antibody (Binary String)
def generate_antibody(size):
    return [random.randint(0, 1) for _ in range(size)]

# Generate Initial Population
def initialize_population(pop_size, size):
    return [generate_antibody(size) for _ in range(pop_size)]

# Select the Best Antibodies (Based on Fitness)
def select_best(population, num_selected):
    population.sort(key=fitness, reverse=True)
    return population[:num_selected]

# Clone the Selected Antibodies
def clone_antibodies(selected, clone_factor):
    clones = []
    for antibody in selected:
        num_clones = int(clone_factor * len(selected))  # More clones for better antibodies
        clones.extend([antibody.copy() for _ in range(num_clones)])
    return clones

# Hypermutation: Apply Small Mutations to Clones
def hypermutation(clones, mutation_rate):
    mutated_clones = []
    for clone in clones:
        new_clone = clone[:]
        for i in range(len(clone)):
            if random.random() < mutation_rate:
                new_clone[i] = 1 - new_clone[i]  # Flip bit
        mutated_clones.append(new_clone)
    return mutated_clones

# Replace Worst Antibodies with Random New Ones
def replace_worst(population, new_size):
    return population[:new_size] + [generate_antibody(len(population[0])) for _ in range(len(population) - new_size)]

# Clonal Selection Algorithm
def clonal_selection(pop_size=10, size=8, generations=10, clone_factor=2, mutation_rate=0.2):
    population = initialize_population(pop_size, size)

    for gen in range(generations):
        selected = select_best(population, num_selected=int(pop_size * 0.5))  # Select Top 50%
        clones = clone_antibodies(selected, clone_factor)
        mutated_clones = hypermutation(clones, mutation_rate)
        
        # Merge and select best from both population and clones
        population.extend(mutated_clones)
        population = select_best(population, pop_size)
        
        # Replace worst individuals
        population = replace_worst(population, new_size=int(pop_size * 0.8))
        
        best = max(population, key=fitness)
        print(f"Generation {gen+1}: Best Fitness = {fitness(best)}, Best Antibody = {best}")

    return max(population, key=fitness)

# Run Clonal Selection
best_solution = clonal_selection()
print("\nBest Solution Found:", best_solution)
