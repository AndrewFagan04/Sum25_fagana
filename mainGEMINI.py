import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pypdf import PdfReader


with st.sidebar:
    st.image("AnswerNestLOGO.png", width=1000)
st.title("SUNY Poly Academic Calendar Ai-Answerer (Fall 2025)")

user_input = st.text_area("Ask something:")
submit = st.button("Generate")

load_dotenv()

def read_file():
    # creating a pdf reader object
    reader = PdfReader("SUNY Web/Fall2025.pdf")

    context = ""
    for p in range(len(reader.pages)):
        #creating a page object
        page = reader.pages[p]

        # extracting text from page
        context += "\n" + page.extract_text()
    return context



def generate(context):
    if submit and user_input:
        api_key=os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        contents = [types.Content(role="user", parts=[types.Part.from_text(text=user_input), types.Part.from_text(text=context)])]

        config = types.GenerateContentConfig(temperature=0, safety_settings=[types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"), types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"), types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_MEDIUM_AND_ABOVE"), types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE")], response_mime_type="text/plain")

        with st.spinner("Generating..."):
            result = ""
            for chunk in client.models.generate_content_stream(
                model="gemma-3-27b-it",
                contents=contents,
                config=config):
                result += chunk.text or ""
            st.write(result)


if __name__ == "__main__":
    c = read_file()                            
    generate(c)