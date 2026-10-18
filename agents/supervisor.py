from services.ollama_client import ask

AVAILABLE_AGENTS = {"coding", "general","collaborate"}

def select_agent(question: str) -> str:
  system_promp = """
    You are the supervisor of a multi-agent AI system.

    Your job is to select the most appropriate agent.

    Available agents:
    - coding: Programming, debugging, software engineering,
      SQL, APIs, and technical coding tasks.
    - general: General knowledge, explanations, and other topics.
    - collaborate: Tasks requiring both software implementation
    and a substantial non-programming explanation or analysis.

    Rules:
    - Return exactly one word: coding, general, or collaborate.
    - Choose collaborate only when both agents provide distinct value.
    - Do not answer the user's question.
    - If the user explicitly asks agents to collaborate,
      analyze, implement, and review a solution,
      choose collaborate.
    - If the user requests both implementation and
     independent review, choose collaborate.

    
    Examples:

    User: Write a Python function to calculate factorials.
    Decision: coding

    User: What caused the fall of the Roman Empire?
    Decision: general

    User: Explain the mathematics of linear regression and
    implement a Python model to predict house prices.
    Decision: collaborate

    User: Explain neural networks and build a neural network
    using TensorFlow.
    Decision: collaborate

    User: Debug my SQL connection.
    Decision: coding

    Important:
    When a request explicitly requires both theoretical analysis
    and software implementation, prefer collaborate.

    Return only the decision word.
    """

  response = ask(
    model = "qwen2.5:3b",
    system_prompt=system_promp,
    user_prompt=question
  )

  decision = response.strip().lower()

  print(f"Supervisor raw decision: {response!r}")

  if decision in AVAILABLE_AGENTS:
    return decision

  #Accept a clearly labeled decision
  if decision.startswith("decision:"):
    parsed = decision.split(":",1)[1].strip()

    if parsed in AVAILABLE_AGENTS:
      return parsed

  print(f"Unrecognized routing decision: {response!r}")

  return "general"