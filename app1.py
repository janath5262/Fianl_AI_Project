import streamlit as st
from PIL import Image
import pyttsx3
import os
import pytesseract  
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Google Generative AI with API Key
API_KEY = "ADD_YOUR_API_KEY"  
os.environ["ADD_YOUR_API_KEY"] = API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()




# Functions for functionality
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Upload Image Section
st.title('''🤖Assisting Visually Impaired Individuals''')
st.markdown("📤 Upload an Image", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Buttons Section
col1, col2, col3 = st.columns(3)

button1 = col1.button("🔍 Describe Scene")
button2 = col2.button("✍️ Extract Text")
button3 = col3.button("🔊 Text-to-Speech")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of objects detected in the image with their purpose.
2. Overall description of the image.
3. Advantages and Disadvantages for the visually impaired.
"""

# Process user interactions
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    # Handle the "Describe Scene" button click
    if button1:
        with st.spinner("Generating scene description..."):
            # Generate scene description
            response = generate_scene_description(input_prompt, image_data)
            st.write(response)

            # Convert the scene description to speech
            with st.spinner("Converting scene description to speech..."):
                if response.strip():
                    text_to_speech(response)
                    st.success(" Text-to-Speech Conversion Completed for Scene Description!")
                else:
                    st.warning("No description available to convert to speech.")

    
    # Handle the "Text-to-Speech" button click
    if button3:
        with st.spinner("Converting extracted text to speech..."):
            text = extract_text_from_image(image)
            if text.strip():
                text_to_speech(text)
                st.success(" Text-to-Speech Conversion Completed for Extracted Text!")
            else:
                st.warning("No text found to convert.")
