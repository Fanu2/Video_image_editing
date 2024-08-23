import ollama

def main():
    # Create a client or similar instance based on the library's API
    client = ollama.Client()  # Replace with actual client initialization if needed

    try:
        # Prepare input text
        input_text = "What is the capital of France?"

        # Generate output (using 'generate' method with minimal parameters)
        response = client.generate(
            model='llama2',  # Replace with the actual model name if necessary
            prompt=input_text
        )

        # Print the output
        print("Model output:", response)  # Adjust based on actual response structure
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
