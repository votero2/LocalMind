from agents.general_agent import run as general_run
from agents.coding_agent import run as coding_run
from agents.supervisor import select_agent
from agents.reviewer_agent import review


def collaborate(question: str) -> str:
  print("\nCollaboration mode selected.\n")

  analysis_prompt = f"""
  Analyze the following request.
  Emplain the relevant concepts and requirements.
  Do not write implementation code.

  Request:
  {question}
  """

  analysis = general_run(analysis_prompt)

  #Step 2: Coding Agent receives the analysis
  print("Step 2: Coding Agent implementing...\n")

  implementation_prompt = f"""
  Original user request:
  {question}

  General Agent analysis:
  {analysis}

  Using this analysis, provide the software implementation
  requested by user.
  Explain important design choices.
  """

  implementation = coding_run(implementation_prompt)

  #Step #: Reviewer Agent examines the implementation
  print("Step 3: Reviewer Agent checking implementation...\n")

  review_result = review(question, implementation)

  return(
    f"GENERAL AGENT ANALYSIS:\n{analysis}\n\n"
    f"CODING AGENT IMPLEMENTATION:\n{implementation}\n\n"
    f"REVIEWER AGENT FEEDBACK:\n{review_result}"
  )


def process(question: str) -> str:
  selected_agent = select_agent(question)

  if selected_agent == "collaborate":
    return collaborate(question)

  if selected_agent == "coding":
    print("\nCoding Agent selected.\n")
    return coding_run(question)
  
  print("\nGeneral Agent selected.\n")
  return general_run(question)