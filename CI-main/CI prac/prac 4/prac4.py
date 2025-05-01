import numpy as np
import random
import matplotlib.pyplot as plt

# Define the number of cities and the distance matrix
NUM_CITIES = 10  # Number of cities to visit
ITERATIONS = 100  # Number of iterations
ANT_COUNT = 50  # Number of ants
ALPHA = 1  # Influence of pheromone
BETA = 5  # Influence of heuristic (distance)
RHO = 0.1  # Rate of pheromone evaporation
Q = 100  # Total pheromone deposited by each ant

# Randomly generate coordinates for cities (for simplicity)
np.random.seed(42)
cities = np.random.rand(NUM_CITIES, 2)  # Cities as 2D coordinates

# Calculate the Euclidean distance matrix
def calculate_distance(cities):
    dist_matrix = np.zeros((NUM_CITIES, NUM_CITIES))
    for i in range(NUM_CITIES):
        for j in range(i + 1, NUM_CITIES):
            dist = np.linalg.norm(cities[i] - cities[j])
            dist_matrix[i][j] = dist_matrix[j][i] = dist
    return dist_matrix

# Initialize pheromone matrix
def initialize_pheromones():
    pheromones = np.ones((NUM_CITIES, NUM_CITIES))  # Initial pheromone is constant for all edges
    np.fill_diagonal(pheromones, 0)  # No pheromone on the diagonal (city to itself)
    return pheromones

# Probabilistic decision rule for path selection
def select_next_city(current_city, visited, pheromones, distances):
    pheromone_levels = pheromones[current_city]
    pheromone_levels[visited] = 0  # No pheromone for already visited cities

    # Calculate desirability based on distance (heuristic) and pheromone levels
    desirability = pheromone_levels ** ALPHA * (1.0 / (distances[current_city] + 1e-10)) ** BETA

    # Choose the next city based on probabilities
    total = np.sum(desirability)
    if total == 0:
        probabilities = np.ones_like(desirability) / len(desirability)  # If all cities are equally likely
    else:
        probabilities = desirability / total

    next_city = np.random.choice(len(probabilities), p=probabilities)
    return next_city

# Ant Colony Optimization main loop
def ant_colony_optimization():
    # Distance matrix and pheromone initialization
    distances = calculate_distance(cities)
    pheromones = initialize_pheromones()

    best_path = None
    best_length = float('inf')

    for iteration in range(ITERATIONS):
        all_paths = []
        all_lengths = []

        # Each ant constructs a solution
        for ant in range(ANT_COUNT):
            visited = [False] * NUM_CITIES
            path = []
            current_city = random.randint(0, NUM_CITIES - 1)
            path.append(current_city)
            visited[current_city] = True

            for _ in range(NUM_CITIES - 1):
                next_city = select_next_city(current_city, visited, pheromones, distances)
                path.append(next_city)
                visited[next_city] = True
                current_city = next_city

            path_length = sum(distances[path[i], path[i + 1]] for i in range(NUM_CITIES - 1)) + distances[path[-1], path[0]]

            all_paths.append(path)
            all_lengths.append(path_length)

            # Update best path found
            if path_length < best_length:
                best_path = path
                best_length = path_length

        # Pheromone evaporation
        pheromones *= (1 - RHO)

        # Pheromone deposition
        for ant in range(ANT_COUNT):
            path = all_paths[ant]
            path_length = all_lengths[ant]
            pheromone_deposit = Q / path_length
            for i in range(NUM_CITIES - 1):
                pheromones[path[i], path[i + 1]] += pheromone_deposit
            pheromones[path[-1], path[0]] += pheromone_deposit

        print(f"Iteration {iteration + 1}: Best Path Length = {best_length}")

    return best_path, best_length

# Visualize the best path found by the ants
def plot_best_path(best_path):
    best_path_coords = cities[best_path]
    best_path_coords = np.vstack((best_path_coords, best_path_coords[0]))  # Return to start

    plt.figure(figsize=(8, 6))
    plt.plot(best_path_coords[:, 0], best_path_coords[:, 1], 'r-o', markersize=6)
    plt.scatter(cities[:, 0], cities[:, 1], color='blue', label='Cities', zorder=5)
    plt.title('Best Path Found by Ant Colony Optimization')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# Run the ACO algorithm and visualize the result
best_path, best_length = ant_colony_optimization()
print(f"\nBest Path: {best_path}")
print(f"Best Path Length: {best_length}")
plot_best_path(best_path)
