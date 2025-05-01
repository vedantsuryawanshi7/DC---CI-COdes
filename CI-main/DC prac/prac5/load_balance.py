#Write code to simulate requests coming from clients and distribute them among the servers using the load balancing algorithms. (Load Balancing, Simulation)




import random

# Step 1: Define the Server class
class Server:
    def __init__(self, server_id):
        self.server_id = server_id  # Unique server ID
        self.load = 0  # Number of requests currently being processed
    
    def process_request(self):
        """Simulate processing a request by incrementing the load."""
        self.load += 1
    
    def finish_request(self):
        """Simulate finishing a request by decrementing the load."""
        self.load -= 1

    def __str__(self):
        return f"Server {self.server_id} - Load: {self.load}"

# Step 2: Define the Request class
class Request:
    def __init__(self, request_id):
        self.request_id = request_id  # Unique request ID
    
    def __str__(self):
        return f"Request {self.request_id}"

# Step 3: Define the LoadBalancer class
class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.round_robin_index = 0  # For Round Robin algorithm
    
    def round_robin(self, request):
        """Distribute requests using Round Robin algorithm."""
        server = self.servers[self.round_robin_index]
        print(f"Routing {request} to {server}")
        server.process_request()
        
        # Move to the next server in the round-robin cycle
        self.round_robin_index = (self.round_robin_index + 1) % len(self.servers)
    
    def least_connections(self, request):
        """Distribute requests to the server with the least number of active requests."""
        server = min(self.servers, key=lambda s: s.load)
        print(f"Routing {request} to {server}")
        server.process_request()
    
    def random(self, request):
        """Distribute requests randomly to any server."""
        server = random.choice(self.servers)
        print(f"Routing {request} to {server}")
        server.process_request()
    
    def finish_request(self, server_id):
        """Finish a request on a given server and reduce its load."""
        server = next((s for s in self.servers if s.server_id == server_id), None)
        if server:
            server.finish_request()

# Step 4: Simulate client requests and load balancing
def simulate_load_balancing():
    # Create servers
    servers = [Server(server_id=i) for i in range(1, 4)]  # 3 servers
    
    # Create a load balancer
    load_balancer = LoadBalancer(servers)
    
    # Simulate incoming client requests
    requests = [Request(request_id=i) for i in range(1, 11)]  # 10 client requests
    
    # Simulate requests being routed using different load balancing algorithms
    print("\n-- Round Robin Load Balancing --")
    for req in requests:
        load_balancer.round_robin(req)
    
    print("\n-- Least Connections Load Balancing --")
    for req in requests:
        load_balancer.least_connections(req)
    
    print("\n-- Random Load Balancing --")
    for req in requests:
        load_balancer.random(req)

# Step 5: Run the simulation
simulate_load_balancing()
