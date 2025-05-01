import random
import numpy as np
from deap import base, creator, tools, algorithms

# Step 1: Define the Optimization Problem
# We aim to maximize f(x) = sum(x), where x is a binary vector

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # Maximization problem
creator.create("Individual", list, fitness=creator.FitnessMax)

# Step 2: Define the DEAP Toolbox
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)  # Binary genes (0 or 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)  # 10 genes
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Step 3: Define the Fitness Function
def eval_function(individual):
    return (sum(individual),)  # Maximizing the sum of 1s

toolbox.register("evaluate", eval_function)
toolbox.register("mate", tools.cxTwoPoint)  # Two-point crossover
toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)  # 20% chance to flip bits
toolbox.register("select", tools.selTournament, tournsize=3)  # Tournament selection

# Step 4: Run the Evolutionary Algorithm
def run_evolution():
    pop = toolbox.population(n=50)  # Population of 50
    hof = tools.HallOfFame(1)  # Keep track of the best individual

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=20, stats=stats, halloffame=hof, verbose=True)

    print("\nBest Individual:", hof[0], "Fitness:", hof[0].fitness.values[0])

# Step 5: Execute
if __name__ == "__main__":
    run_evolution()
