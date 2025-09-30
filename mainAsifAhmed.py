import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pypdf import PdfReader


with st.sidebar:
    st.image("AnswerNestLOGO.png", width=1000)
st.title("Asif Ahmed's Ai-Answerer")


if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

option = st.selectbox("Options",("Chapter 11 - Deep Foundations",
                                 "Shallow Foundation - Step by Step",
                                 "Types of Foundations Footings in Building Construction Video",
                                 "Shallow Foundations and Their Types Foundations in Building Video",
                                 "Foundation Insulation Effectiveness Frost Protected Shallow Foundations Video",
                                 "cold regions",
                                 "foundations issues",
                                 "dewatering"))



load_dotenv()

def read_file(option):
    if option == "Chapter 11 - Deep Foundations":
        file = "Deep Foundation Cudotu.pdf"
    elif option == "Shallow Foundation - Step by Step":
        file = "shallow foundation step by step.pdf"
    elif option == "Types of Foundations Footings in Building Construction Video":
        file = "Types of Foundations  Footings in Building Construction.pdf"
    elif option == "Shallow Foundations and Their Types Foundations in Building Video":
        file = "Shallow Foundations and Their Types Foundations in Building 2.pdf"
    elif option == "Foundation Insulation Effectiveness Frost Protected Shallow Foundations Video":
        file = "Foundation Insulation Effectiveness Frost Protected Shallow Foundations.pdf"
    elif option == "cold regions":
        file = "cold regionsREADABLE.pdf"
    elif option == "foundations issues":
        file = "foundations issuesREADABLE.pdf"
    elif option == "dewatering":
        file = "dewateringREADABLE.pdf"
    
    # creating a pdf reader object
    reader = PdfReader("AsifAhmed/" + file)

    context = ""
    for p in range(len(reader.pages)):
        #creating a page object
        page = reader.pages[p]

        # extracting text from page
        context += "\n" + page.extract_text()

    return context



def generate(context):
    if user_input := st.chat_input("Ask something:"):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        prompt_text = f"""
        You are a helpful assistant.  Your purpose is to answer questions based ONLY on the information provided in the attached document.

        If the answer to the question cannot be found directly within the document, you MUST respond with the phrase: "Answer not found in document."  Do not attempt to provide an answer based on your general knowledge; stick strictly to the content of the document.

        Document: {context}
        Question: {user_input}
        """

        api_key=os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        contents = [types.Content(role="user", parts=[types.Part.from_text(text=user_input), types.Part.from_text(text=prompt_text)])]

        config = types.GenerateContentConfig(temperature=0, safety_settings=[types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"), types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"), types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_MEDIUM_AND_ABOVE"), types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE")], response_mime_type="text/plain")

        with st.spinner("Generating..."):
            result = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash", #these versions aren't in use anymore: gemma-1.5-flash, gemini-1.5-flash-8b
                contents=contents,
                config=config):
                result += chunk.text or ""


            response = f"Gemini: {result}"
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def delete():
    if st.button("Delete History"):
        for message in st.session_state:
            del st.session_state[message]



if __name__ == "__main__":
    context = read_file(option)                            
    generate(context)
    delete()