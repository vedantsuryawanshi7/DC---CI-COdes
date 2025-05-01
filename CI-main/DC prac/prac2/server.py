import Pyro5.api

@Pyro5.api.expose
class StringConcatenationServer:
    def concatenate_string(self, str1, str2):  # Changed to match client call
        result = str1 + str2
        return result

def main():
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(StringConcatenationServer(), "example.string_concatenation")
    
    print("Server is running. URI:", uri)

    with open("server_uri.txt", "w") as f:
        f.write(str(uri))
    
    daemon.requestLoop()

if __name__ == "__main__":
    main()
