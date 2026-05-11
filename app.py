from huggingface_hub import InferenceClient
from config import HF_TOKEN

# Create the AI client using your Hugging Face token from config.py
client = InferenceClient(api_key=HF_TOKEN)

print("🤖 Ausaf AI Chatbot Started!")
print("Type 'exit' to quit.\n")

while True:
    # Get user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("Bot: Goodbye! 👋")
        break

    try:
        # Send the conversation to the AI model
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Ausaf AI, a helpful, friendly, and intelligent assistant.

If anyone asks:
- Who created you?
- Who developed you?
- Who is your owner?
- Who made you?
- Who built you?

Always reply exactly:
I was created and developed by Ahiiusaf Ahamad.

Be accurate, helpful, and polite in all other answers.
"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=300,
        )

        # Extract and print the AI's reply
        reply = completion.choices[0].message.content
        print(f"Bot: {reply}\n")

    except Exception as e:
        print("Error:", e)
        print("Please check your Hugging Face token, model access, and internet connection.\n")