import os
from together import Together

# Ensure the API key is set
api_key = os.getenv("TOGETHER_API_KEY")
if not api_key:
    raise ValueError("TOGETHER_API_KEY environment variable not set.")

# Initialize the Together client
client = Together(api_key=api_key)

# Maintain conversation history
conversation_history = []

def get_response(user_input):
    global conversation_history

    # Append user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Get AI-generated response
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=conversation_history,
        max_tokens=500,
        temperature=0.5
    )

    bot_reply = response.choices[0].message.content.strip()

    # Format response for better readability
    formatted_reply = format_response(bot_reply)

    # Append bot reply to history
    conversation_history.append({"role": "assistant", "content": formatted_reply})

    return formatted_reply

def format_response(response_text):
    """Properly formats AI responses by ensuring correct numbering and spacing."""
    lines = response_text.split("\n")
    formatted_lines = []
    num = 1  # Start numbering

    for line in lines:
        line = line.strip()

        # Skip empty lines to prevent index errors
        if not line:
            continue  

        # Ensure proper headings stay bold and separate
        if "**" in line:
            formatted_lines.append(f"\n{line}\n")  # Ensure bold headings are always on a new line
            num = 1  # Reset numbering after a heading

        # Fix numbered points and ensure they appear correctly
        elif line.startswith("-") or line.startswith("•") or (line[0].isdigit() if line else False):
            formatted_lines.append(f"{num}. {line.lstrip('-•1234567890.').strip()}")  
            num += 1

        # Ensure normal sentences are well-spaced and don't merge
        else:
            formatted_lines.append(line)  

    # Rejoin with proper line breaks
    formatted_text = "\n\n".join(formatted_lines)

    return formatted_text.strip()  # Ensure no extra blank spaces

if __name__ == "__main__":
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            break
        print("\nUser Input:", user_message)
        try:
            bot_reply = get_response(user_message)
            print("\nBot:\n", bot_reply, "\n")
        except Exception as e:
            print(f"ERROR: {e}")
            print("\nBot: An error occurred.\n")
