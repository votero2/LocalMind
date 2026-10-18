from agents.general_agent import run as general_run
from agents.coding_agent import run as coding_run
from agents.supervisor import select_agent
from agents.reviewer_agent import review


def collaborate(question: str, on_event=None) -> str:
  def emit(agent, status , message):
      if on_event:
          on_event({
              "agent": agent,
              "status": status,
              "message": message
          })
  print("\nCollaboration mode selected.\n")

  analysis_prompt = f"""
  Analyze the following request.
  Emplain the relevant concepts and requirements.
  Do not write implementation code.

  Request:
  {question}
  """
  emit("general_agent","running","Analyzing request")
  
  analysis = general_run(analysis_prompt)

  emit("general_agent","completed","Analysis finished")

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

  
    # Step 4: Check the reviewer's assessment
  def get_assessment(feedback: str) -> str:
        for line in reversed(feedback.splitlines()):
            line = line.strip().upper()

            if line.startswith("FINAL ASSESSMENT:"):
                status = line.split(":", 1)[1].strip()

                if status in ("PASS", "NEEDS_REVISION"):
                    return status

        return "UNKNOWN"

  assessment = get_assessment(review_result)
  final_implementation = implementation
  final_review = review_result

  # Step 5: Allow one revision if needed
  if assessment == "NEEDS_REVISION":
        print("\nStep 4: Coding Agent revising implementation...\n")

        revision_prompt = f"""
        ORIGINAL USER REQUEST:
        {question}

        PREVIOUS IMPLEMENTATION:
        {implementation}

        REVIEWER FEEDBACK:
        {review_result}

        Correct the issues identified by the reviewer.

        Return the complete revised implementation.
        Preserve all original user requirements.
        """

        final_implementation = coding_run(revision_prompt)

        # Step 6: Review the corrected implementation
        print("\nStep 5: Reviewer Agent performing final review...\n")

        final_review = review(question, final_implementation)
        assessment = get_assessment(final_review)

  
  return (
        f"GENERAL AGENT ANALYSIS:\n{analysis}\n\n"
        f"CODING AGENT IMPLEMENTATION:\n{final_implementation}\n\n"
        f"REVIEWER AGENT FEEDBACK:\n{final_review}\n\n"
        f"FINAL STATUS: {assessment}"
    )



def process(question: str, on_event=None) -> str:
    selected_agent = select_agent(question)

    if on_event:
        on_event({
            "agent": "supervisor",
            "status": "completed",
            "message": f"Selected route: {selected_agent}"
        })

    if selected_agent == "collaborate":
        return collaborate(question, on_event=on_event)

    if selected_agent == "coding":
        if on_event:
            on_event({
                "agent": "coding_agent",
                "status": "running",
                "message": "Generating code"
            })

        result = coding_run(question)

        if on_event:
            on_event({
                "agent": "coding_agent",
                "status": "completed",
                "message": "Code generated"
            })

        return result

    if on_event:
        on_event({
            "agent": "general_agent",
            "status": "running",
            "message": "Processing request"
        })

    result = general_run(question)

    if on_event:
        on_event({
            "agent": "general_agent",
            "status": "completed",
            "message": "Response generated"
        })

    return result