import xmlrpc.server
import factorial  # Import the factorial module

if __name__ == '__main__':
    server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000))
    print("Listening on port 8000...")
    server.register_function(factorial.calculate_factorial, 'factorial') #use imported function
    server.serve_forever()