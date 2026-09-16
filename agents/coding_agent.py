from services.ollama_client import ask

def run(question: str) -> str:
  return ask(
    model="qwen2.5-coder:3b",
    system_prompt="You are an expert software engineer.",
    user_prompt=question
  )