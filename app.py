from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import tempfile

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

st.title('Gemini Chatbot')

user_prompt = st.text_area(label="Enter your prompt")
image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if st.button("Submit"):
    if user_prompt:
        if image_file is not None:
            image = None
            with tempfile.NamedTemporaryFile(delete=True, suffix=".jpg") as tmp_file:
                tmp_file.write(image_file.getbuffer())
                temp_image_path = tmp_file.name
                image = genai.upload_file(path=temp_image_path)
            
            response = model.generate_content([user_prompt, image])
            genai.delete_file(image.name)
        else:
            response = model.generate_content([user_prompt])

        st.subheader("Response from Gemini:")
        st.write(response.text)
    else:
        st.error("Please enter a prompt.")
