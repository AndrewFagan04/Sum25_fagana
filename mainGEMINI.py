import datetime
from pypdf import PdfReader
import os
import streamlit as st
import pandas as pd
import time
import keyboard
import psutil
from google import genai
from google.genai import types
import dotenv

d = datetime.datetime.now()



############################################
#chatGEMINI

dotenv.load_dotenv()

def generate():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    model = "gemma-3-27b-it"
    contents = [types.Content(role="user", parts=[types.Part.from_text(text="can you read this?")])]
    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",  # Block some
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_MEDIUM_AND_ABOVE",  # Block some
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",  # Block some
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",  # Block some
            ),
        ],
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

############################################

def read_file():
    # creating a pdf reader object
    reader = PdfReader("SUNY Web/Fall2025.pdf")

    content = ""
    for p in range(len(reader.pages)):
        #creating a page object
        page = reader.pages[p]

        # extracting text from page
        content += "\n" + page.extract_text()
        
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
    generate()

       