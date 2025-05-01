import xmlrpc.client

def get_factorial(number):
    """Gets the factorial from the remote server."""
    try:
        with xmlrpc.client.ServerProxy("http://localhost:8000") as proxy:
            result = proxy.factorial(number)
            return result
    except ConnectionRefusedError:
        return "Error: Could not connect to the server. Make sure it is running."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    while True:
        try:
            num = int(input("Enter an integer to calculate its factorial (or type 'exit' to quit): "))
            result = get_factorial(num)
            print(f"Factorial of {num}: {result}")

        except ValueError:
            user_input = input("Invalid input. Type 'exit' to quit, or enter an integer: ")
            if user_input.lower() == 'exit':
                break
            else:
                print("Invalid input")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
