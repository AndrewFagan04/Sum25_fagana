from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import datetime
import os

d = datetime.datetime.now()



def read_file():
    user = input("What file would you like to learn about?: ")

    #opens files
    file = open(user, 'r')

    #reads file
    content = file.read()
    print(content)

    #closes file
    file.close()
    
    return content





def models():
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

    Use this file to help answer the question {content}

    Answer:
    """

    return model_name, name, template





def handle_conversation(model_name, name, template, content):
    model = OllamaLLM(model=model_name)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model


    context = ""
    print("Welcome to the AI Model ", name,"! Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = chain.invoke({"year": d.year, "month": d.month, "day": d.day, "hour": d.hour, "minute": d.minute, "context": context, "question": user_input, "content": content})
        print(name,": ", result)
        context += f"\nUser: {user_input}\nAI: {result}\nFile: {content}"



if __name__ == "__main__":
    c = read_file()
    m, n, t = models()
    handle_conversation(m, n, t, c)

