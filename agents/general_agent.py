from services.ollama_client import ask

def run(question: str) -> str:
  return ask(
    model = "qwen2.5:3b",
    system_prompt="You are a helpful AI assistant.",
    user_prompt=question
  )