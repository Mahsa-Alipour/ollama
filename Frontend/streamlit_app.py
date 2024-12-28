import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("Lava-Llama3 Multi_Modal")

interaction_type = st.sidebar.radio(
    "Select Interaction Type:",
    ["QA", "Resume Summarizer", "Image Describer"]
)

BACKEND_URLS = {
    "QA": os.getenv("QA_API_URL"),
    "Resume Summarizer": os.getenv("RESUME_SUMMARIZER_API_URL"),
    "Image Describer": os.getenv("IMAGE_DESCRIBER_API_URL"),
}

MAX_FILE_SIZE = 3 * 1024 * 1024  
ALLOWED_FILE_TYPE = "application/pdf"

if interaction_type == "QA":
    st.header("QA")

    prompt = st.text_input("Enter your question:")

    if st.button("Generate QA Response"):
        if prompt:
            try:
                response = requests.get(BACKEND_URLS["QA"], params={"prompt": prompt})

                if response.status_code == 200:
                    result = response.json()
                    st.write("### Model Response:")
                    st.write(result.get("response", "No response found!"))
                else:
                    st.error(f"Failed to fetch response from the FastAPI server. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a question.")

elif interaction_type == "Resume Summarizer":
    st.header("Resume Summarizer")

    prompt = st.text_input("Enter your summary prompt:")

    uploaded_file = st.file_uploader("Upload a resume (PDF):", type=["pdf"])

    if uploaded_file:
        if uploaded_file.type != ALLOWED_FILE_TYPE:
            st.error("Invalid file type. Please upload a PDF file.")
        elif uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"File is too large. Maximum allowed size is {MAX_FILE_SIZE // (1024 * 1024)} MB.")
        else:
            if prompt:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                data = {"prompt": prompt}

                try:
                    response = requests.post(BACKEND_URLS["Resume Summarizer"], files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()
                        st.write("### Model Response:")
                        st.write(result.get("response", "No response found!"))
                    else:
                        st.error(f"Failed to fetch response from the FastAPI server. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")
            else:
                st.warning("Please enter a summary prompt.")



  
# elif interaction_type == "Resume Summarizer":
#         st.header("Resume Summarizer")

#         uploaded_file = st.file_uploader("Upload a resume (PDF):", type=["pdf"])

#         if uploaded_file:
#             if uploaded_file.type != ALLOWED_FILE_TYPE:
#                 st.error("Invalid file type. Please upload a PDF file.")
#             elif uploaded_file.size > MAX_FILE_SIZE:
#                 st.error(f"File is too large. Maximum allowed size is {MAX_FILE_SIZE // (1024 * 1024)} MB.")
#             else:                
#                 try:
#                     files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
#                     data = {}  
#                     response = requests.post(BACKEND_URLS["Resume Summarizer"], files=files, data=data)

#                     if response.status_code == 200:
#                         result = response.json()
#                         st.write("### Model Response:")
#                         st.json(result)  
#                     else:
#                         st.error(f"Failed to fetch response from the FastAPI server. Status code: {response.status_code}\nDetail: {response.text}")
#                 except Exception as e:
#                     st.error(f"Error occurred: {str(e)}")

    



elif interaction_type == "Image Describer":
    st.header("Image Describer")

    prompt = st.text_input("Enter your description prompt:")

    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])

    if st.button("Generate Image Description"):
        if prompt and uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"prompt": prompt}

            try:
                response = requests.post(BACKEND_URLS["Image Describer"], files=files, data=data)

                if response.status_code == 200:
                    result = response.json()
                    st.write("### Model Response:")
                    st.write(result.get("response", "No response found!"))
                else:
                    st.error(f"Failed to fetch response from the FastAPI server. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a description prompt and upload an image.")
