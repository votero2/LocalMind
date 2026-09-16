from agents.coordinator import process


def main():
  print("==== LocalMind AI ====")

  while True: 
    question = input("Ask: ")

    if question.lower() == "exit":
      break

    answer = process(question)

    print("\n")
    print(answer)
    print()


if __name__ == "__main__":
  main()