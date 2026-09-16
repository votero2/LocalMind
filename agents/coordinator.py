from agents.general_agent import run as general_run
from agents.coding_agent import run as coding_run

PROGRAMMING_WORDS = [
  "python",
  "c#",
  "java",
  "code",
  "program",
  "function",
  "class",
  "sql",
  "api",
  "bug",
  "error"
]

def process(question: str):
  lower = question.lower()

  if any(word in lower for word in PROGRAMMING_WORDS):
    print("\nCoding Agent selected.\n")
    return coding_run(question)
  
  print("\nGeneral Agent selected.\n")
  return general_run(question)