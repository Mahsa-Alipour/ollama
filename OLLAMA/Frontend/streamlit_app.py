import streamlit as st
import requests

# Streamlit app title
st.title("Lava-Llama3 Multi_Modal")

# Sidebar for selecting interaction type
interaction_type = st.sidebar.radio(
    "Select Interaction Type:",
    ["QA", "Resume Summarizer", "Image Describer"]
)

# Backend URL mappings
BACKEND_URLS = {
    "QA": "http://127.0.0.1:8000/ask_text",
    "Resume Summarizer": "http://127.0.0.1:8000/ask_pdf",
    "Image Describer": "http://127.0.0.1:8000/ask_image",
}

# Handle each interaction type
if interaction_type == "QA":
    st.header("QA")

    # Input box for the prompt
    prompt = st.text_input("Enter your question:")

    # Button to send the prompt
    if st.button("Generate QA Response"):
        if prompt:
            try:
                # Call the FastAPI backend for QA
                response = requests.get(BACKEND_URLS["QA"], params={"prompt": prompt})

                if response.status_code == 200:
                    # Display the response from the FastAPI server
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

    # Input box for the prompt
    prompt = st.text_input("Enter your summary prompt:")

    # File uploader for the PDF
    uploaded_file = st.file_uploader("Upload a resume (PDF):", type=["pdf"])

    # Button to send the request
    if st.button("Generate Resume Summary"):
        if prompt and uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"prompt": prompt}

            try:
                # Call the FastAPI backend for resume summarization
                response = requests.post(BACKEND_URLS["Resume Summarizer"], files=files, data=data)

                if response.status_code == 200:
                    # Display the response from the FastAPI server
                    result = response.json()
                    st.write("### Model Response:")
                    st.write(result.get("response", "No response found!"))
                else:
                    st.error(f"Failed to fetch response from the FastAPI server. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a summary prompt and upload a resume.")

elif interaction_type == "Image Describer":
    st.header("Image Describer")

    # Input box for the prompt
    prompt = st.text_input("Enter your description prompt:")

    # File uploader for the image
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])

    # Button to send the request
    if st.button("Generate Image Description"):
        if prompt and uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"prompt": prompt}

            try:
                # Call the FastAPI backend for image description
                response = requests.post(BACKEND_URLS["Image Describer"], files=files, data=data)

                if response.status_code == 200:
                    # Display the response from the FastAPI server
                    result = response.json()
                    st.write("### Model Response:")
                    st.write(result.get("response", "No response found!"))
                else:
                    st.error(f"Failed to fetch response from the FastAPI server. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
        else:
            st.warning("Please enter a description prompt and upload an image.")
