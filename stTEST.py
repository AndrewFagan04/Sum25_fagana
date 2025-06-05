from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import datetime
from pypdf import PdfReader
import os
import streamlit as st
import pandas as pd
import time
import keyboard
import psutil

d = datetime.datetime.now()



user_input = st.text_input("Ask Here", "")
if (user_input != None) and (st.button("-->")):

    # creating a pdf reader object
    reader = PdfReader("SUNY Web/Fall2025.pdf")

    content = ""
    for p in range(len(reader.pages)):
        #creating a page object
        page = reader.pages[p]

        # extracting text from page
        content += "\n" + page.extract_text()
        
    print(content)




    template = """
    Answer the question below.

    Today's date is {year}, {month}, {day}, {hour}, {minute}

    Here is the conversation history: {context}

    Question: {question}

    Use this file to help answer the question {content}

    Answer:
    """

    model = OllamaLLM(model='gemma3:12b')
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model


    context = ""


    result = chain.invoke({"year": d.year, "month": d.month, "day": d.day, "hour": d.hour, "minute": d.minute, "context": context, "question": user_input, "content": content})
    print('gemma3:12b',": ", result)
    context += f"\nUser: {user_input}\nAI: {result}\nFile: {content}"
    
    
    st.write({"gemma3:12b": [result]})


if st.button("STOP"):
    time.sleep(1)
    keyboard.press_and_release('ctrl+w')
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate        




       