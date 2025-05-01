import numpy as np
import random
from deap import base, creator, tools, algorithms
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split


class SimpleNN(nn.Module):
    def __init__(self, num_neurons, activation_function):
        super(SimpleNN, self).__init__()
        self.hidden = nn.Linear(3, num_neurons)
        self.output = nn.Linear(num_neurons, 1)

        if activation_function == 'relu':
            self.activation = nn.ReLU()
        elif activation_function == 'tanh':
            self.activation = nn.Tanh()
        elif activation_function == 'sigmoid':
            self.activation = nn.Sigmoid()

    def forward(self, x):
        x = self.activation(self.hidden(x))
        x = self.output(x)
        return x


def objective_function(individual, X_train, y_train, X_test, y_test):
    num_neurons, learning_rate, activation_function = individual
    
    model = SimpleNN(num_neurons, activation_function)
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

    for epoch in range(50):  # Training Loop
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train_tensor)
        loss = criterion(predictions, y_train_tensor)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        predictions = model(X_test_tensor)
        loss = criterion(predictions, y_test_tensor)

    return (loss.item(),)


def load_data():
    X = np.random.rand(100, 3)
    y = np.random.rand(100)
    return train_test_split(X, y, test_size=0.2)


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def create_individual():
    num_neurons = random.randint(5, 100)
    learning_rate = random.uniform(0.0001, 0.01)
    activation_function = random.choice(['relu', 'tanh', 'sigmoid'])
    return [num_neurons, learning_rate, activation_function]

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def mutate(individual):
    individual[0] += int(random.gauss(0, 10))  # Mutate neurons
    individual[0] = max(5, min(100, individual[0]))  # Keep neurons in range

    individual[1] += random.gauss(0, 0.005)  # Mutate learning rate
    individual[1] = max(0.0001, min(0.01, individual[1]))  # Clamp learning rate

    if random.random() < 0.2:  # 20% chance to change activation function
        individual[2] = random.choice(['relu', 'tanh', 'sigmoid'])

    return individual,

toolbox.register("mutate", mutate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("select", tools.selTournament, tournsize=3)


def run_ga():
    X_train, X_test, y_train, y_test = load_data()
    
    toolbox.register("evaluate", objective_function, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)

    population = toolbox.population(n=10)
    algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=10, verbose=True)

    best_individual = tools.selBest(population, 1)[0]
    print(f"\nBest Individual: {best_individual}")
    return best_individual


best_individual = run_ga()
