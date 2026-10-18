from services.ollama_client import ask

def review(question: str, implementation: str) -> str:
  system_prompt = """
  You are a software engineer responsible
  for reviewing AI-generated code.

  Review the implementation for:
   1. Logical errors
   2. Security vulnerabilies
   3. Incorrect algorithms
   4. Missing requirements
   5. Data leakage in machine learning pipelines
   6. Code quality and maintainability

   Do not automatically approve the implementation.

   If the implementation has significant problems,
   explain what must be corrected.

   If the implementation appears correct,
   explain why.

   Do not claim the code was executed or tested.

  
    Review rules:

    - Review ONLY the implementation provided.
    - Do not assume that a feature exists.
    - Do not invent functions, variables, or operations.
    - For every issue, identify the exact code
      statement responsible.
    - Explain why the statement is problematic.
    - Suggest a specific correction.
    - Distinguish confirmed bugs from potential risks.
    - If no significant issues are found, say so.
    - Never claim code was executed unless actual
      execution results were provided.

    Structure your response as:

    FINDINGS:
    1. Issue
    2. Evidence from code
    3. Suggested correction

    
   Choose exactly ONE final assessment based on your review:

    - If no significant problems are found, output:
      FINAL ASSESSMENT: PASS

    - If significant problems are found, output:
      FINAL ASSESSMENT: NEEDS_REVISION

  The final assessment must be the LAST line of your response.
  Never output both assessments.
  """

  user_prompt = f"""
  ORIGINAL REQUEST:
  {question}

  GENERATED IMPLEMENTATION:
  {implementation}

  Review this implementation.
  """

  return ask(
    model= "qwen2.5-coder:3b",
    system_prompt=system_prompt,
    user_prompt=user_prompt
  )

  