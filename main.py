from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import datetime

d = datetime.datetime.now()

while True:
    i = input("Choose which model to use; QwQ (q), DeepSeek (d), Qwen (w) or Gemma3 (g): ")
    if(i == "q"):
        model_name = "QwQ"
        name = "QwQ"
        break
    elif(i == "g"):
        model_name = "gemma3:12b"
        name = "Gemma3"
        break
    elif(i == "d"):
        model_name = "deepseek-r1"
        name = "DeepSeek"
        break
    elif(i == "w"):
        model_name = "qwen2.5vl:latest"
        name = "Qwen"
        break
    else:
        print("Try Again")


template = """
Answer the question below.

Today's date is {year}, {month}, {day}, {hour}, {minute}

Here is the conversation history: {context}

Question: {question}

"""#Dig into this website for useful information based on the question: {website}
"""

Answer:
"""

#
#

model = OllamaLLM(model=model_name)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome to the AI Model ", name,"! Type 'exit' to quit.")
    w = input("Type the website you'll like to use as your source: ")
    






    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = chain.invoke({"year": d.year, "month": d.month, "day": d.day, "hour": d.hour, "minute": d.minute, "context": context, "question": user_input, "website": w})
        print(name,": ", result)
        context += f"\nUser: {user_input}\nAI: {result}\nWeb: {w}"

if __name__ == "__main__":
    handle_conversation()

#
#
#