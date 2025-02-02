import os
import anthropic

# Set up the Anthropic API client
api_key = os.environ["ANTHROPIC_API_KEY"]
client = anthropic.Client(api_key)

def chat_with_assistant(prompt):
    response = client.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",
        max_tokens_to_sample=2000,
    )
    return response.completion

def main():
    print("Welcome to the AI Academy Labs Assistant!")
    print("I'm here to help you automate and grow the project.")

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("Thank you for using the AI Academy Labs Assistant. Goodbye!")
            break

        assistant_response = chat_with_assistant(user_input)
        print(f"Assistant: {assistant_response}")

if __name__ == "__main__":
    main()