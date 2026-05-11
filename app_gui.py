import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

from huggingface_hub import InferenceClient
from config import HF_TOKEN

client = InferenceClient(api_key=HF_TOKEN)
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

SYSTEM_PROMPT = """
You are Ausaf AI, a helpful, friendly, and intelligent assistant.

If anyone asks:
- Who created you?
- Who developed you?
- Who is your owner?
- Who made you?
- Who built you?

Always reply exactly:
I was created and developed by Ausaf Ahmad.

Be accurate, helpful, and polite in all other answers.
"""

root = tk.Tk()
root.title("Ausaf AI Chatbot")
root.geometry("800x600")
root.minsize(600, 450)
root.configure(bg="#f5f7fa")

header = tk.Label(
    root,
    text="🤖 Ausaf AI Chatbot",
    font=("Segoe UI", 22, "bold"),
    bg="#1f2937",
    fg="white",
    pady=15,
)
header.pack(fill=tk.X)

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg="white",
    fg="#111827",
    padx=12,
    pady=12,
    relief=tk.FLAT,
)
chat_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
chat_area.config(state=tk.DISABLED)

bottom_frame = tk.Frame(root, bg="#f5f7fa")
bottom_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

user_entry = tk.Entry(
    bottom_frame,
    font=("Segoe UI", 12),
    relief=tk.FLAT,
    bd=0,
)
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))


def add_message(sender, message):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"{sender}: {message}\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)


def ask_ai(user_text):
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            max_tokens=400,
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Error: {e}"

    root.after(0, lambda: add_message("Ausaf AI", reply))
    root.after(0, lambda: send_button.config(state=tk.NORMAL, text="Send"))


def send_message(event=None):
    user_text = user_entry.get().strip()
    if not user_text:
        return

    add_message("You", user_text)
    user_entry.delete(0, tk.END)

    send_button.config(state=tk.DISABLED, text="Thinking...")

    Thread(target=ask_ai, args=(user_text,), daemon=True).start()


send_button = tk.Button(
    bottom_frame,
    text="Send",
    command=send_message,
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief=tk.FLAT,
    padx=22,
    pady=10,
    cursor="hand2",
)
send_button.pack(side=tk.RIGHT)

user_entry.bind("<Return>", send_message)

add_message("Ausaf AI", "Hello! I am your personal AI assistant. Ask me anything.")

user_entry.focus()

root.mainloop()