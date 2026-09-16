from ollama import Client

client = Client(host="http://localhost:11434")


def ask(model: str, system_prompt: str, user_prompt:str) -> str:
  response = client.chat(
    model=model,
    messages=[
      {
        "role":"system",
        "content": system_prompt,
      },{
        "role": "user",
        "content": user_prompt
      }
    ]
  )

  return response["message"]["content"]