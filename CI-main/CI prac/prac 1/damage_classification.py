import numpy as np
import random
from deap import base, creator, tools, algorithms
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split

# Step 1: Define the Neural Network Model in PyTorch
class SimpleNN(nn.Module):
    def __init__(self, num_neurons, activation_function):
        super(SimpleNN, self).__init__()
        self.hidden = nn.Linear(5, num_neurons)  # 5 input features
        self.output = nn.Linear(num_neurons, 1)  # Binary classification output

        # Assign activation function
        self.activation = {
            'relu': nn.ReLU(),
            'tanh': nn.Tanh(),
            'sigmoid': nn.Sigmoid()
        }[activation_function]

    def forward(self, x):
        x = self.activation(self.hidden(x))
        x = torch.sigmoid(self.output(x))  # Sigmoid for binary classification
        return x

# Step 2: Objective Function for GA (Fitness Function)
def objective_function(individual, X_train, y_train, X_test, y_test):
    num_neurons, learning_rate, activation_function = individual

    model = SimpleNN(num_neurons, activation_function)
    criterion = nn.BCELoss()  # Binary Cross-Entropy for classification
    optimizer = optim.Adam(model.parameters(), lr=max(0.0001, learning_rate))  # Ensure positive lr

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

    # Training loop
    for epoch in range(150):  # Increased epochs for better learning
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train_tensor)
        loss = criterion(predictions, y_train_tensor)
        loss.backward()
        optimizer.step()

    # Evaluation
    model.eval()
    with torch.no_grad():
        predictions = model(X_test_tensor)
        accuracy = ((predictions.round() == y_test_tensor).float().mean()).item()

    return (1 - accuracy,)  # Minimizing error

# Step 3: Load and Preprocess Data
def load_data():
    X = np.random.rand(500, 5)  # Increased samples & features
    y = np.random.randint(0, 2, 500)  # Balanced binary labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    return X_train, X_test, y_train, y_test

# Step 4: Define GA Components
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def create_individual():
    return [
        random.randint(10, 150),  # Neurons (10-150)
        random.uniform(0.0001, 0.01),  # Learning rate (0.0001 - 0.01)
        random.choice(['relu', 'tanh', 'sigmoid'])  # Activation function
    ]

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)

# **Fixed Mutation Function**
def custom_mutate(individual):
    """ Mutates only numerical values and keeps activation function unchanged. """
    if random.random() < 0.2:  # 20% chance to mutate neurons
        individual[0] = max(10, min(150, individual[0] + int(random.gauss(0, 10))))  # Ensure valid range

    if random.random() < 0.2:  # 20% chance to mutate learning rate
        individual[1] = max(0.0001, min(0.01, individual[1] + random.gauss(0, 0.001)))  # Ensure valid range

    if random.random() < 0.2:  # 20% chance to change activation function
        individual[2] = random.choice(['relu', 'tanh', 'sigmoid'])

    return individual,

toolbox.register("mutate", custom_mutate)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", objective_function, X_train=None, y_train=None, X_test=None, y_test=None)

# Step 5: Run the Genetic Algorithm
def run_ga():
    X_train, X_test, y_train, y_test = load_data()
    toolbox.unregister("evaluate")
    toolbox.register("evaluate", objective_function, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)

    population = toolbox.population(n=25)  # Increased population size
    algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.3, ngen=20, verbose=True)  # More generations

    best_individual = tools.selBest(population, 1)[0]
    print(f"Best individual: {best_individual}")
    return best_individual

# Step 6: Execute the GA-NN Optimization
best_individual = run_ga()
