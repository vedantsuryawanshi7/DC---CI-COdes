import Pyro5.api

def main():
    with open("server_uri.txt", "r") as f:
        uri = f.read().strip()

    server = Pyro5.api.Proxy(uri)
    str1 = input("Enter the first string: ")
    str2 = input("Enter the second string: ")

    result = server.concatenate_string(str1, str2)
    print("Concatenated Result:", result)

if __name__ == "__main__":
    main()
