from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
import json

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Message(BaseModel):
    user: str
    message: str

@app.post("/ask")
def ask_openai(msg: Message):
    user = msg.user
    prompt = msg.message
    memory = load_memory(user)
    messages = memory + [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    answer = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": answer})
    save_memory(user, messages[-10:])  # Save last 10 messages
    return {"response": answer}

def load_memory(user):
    try:
        with open("memory.json", "r") as f:
            data = json.load(f)
        return data.get(user, [])
    except:
        return []

def save_memory(user, messages):
    try:
        with open("memory.json", "r") as f:
            data = json.load(f)
    except:
        data = {}
    data[user] = messages
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=4)
