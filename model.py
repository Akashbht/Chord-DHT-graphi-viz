from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Get HF token from environment
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="openai/gpt-oss-20b",
    token=HF_TOKEN
)

def chat(message, history=""):
    system_prompt = """You are a specialized technical assistant for the Chord DHT (Distributed Hash Table) project.

SCOPE - Only answer questions about:
1. **Chord DHT Theory**: Ring-based distributed hash tables, consistent hashing, finger tables, successor/predecessor relationships, key lookup algorithms, node join/leave operations
2. **This Project's Implementation**: 
   - Main.py: ChordInterface class managing the network UI and operations
   - Network.py: Network class handling node coordination, metrics, security, backup/restore, health checks, load balancing
   - Node.py: Individual node implementation with data storage, finger tables, key management, encryption
   - Features: Network visualization, backup/restore, load balancing, authentication tokens, data encryption, health monitoring

CONSTRAINTS:
- REFUSE to answer questions outside Chord DHT theory and this project
- If asked about unrelated topics, respond: "I can only answer questions about Chord DHT theory and this specific project implementation."
- Provide code references from Main.py, Network.py, or Node.py when relevant
- Explain how project features implement Chord DHT concepts
- Do not provide information about other DHT implementations or unrelated technologies

Keep responses focused, technical, and grounded in Chord DHT principles and project code."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    response = client.chat_completion(
        messages=messages,
        max_tokens=1500,
        temperature=0.3,
        top_p=0.9
    )
    return response.choices[0].message.content

# ---- Chat Loop ----
history = ""
print("GPT-OSS Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    reply = chat(user_input, history)
    print("Bot:", reply)

    history += f"\nUser: {user_input}\nAssistant: {reply}"

