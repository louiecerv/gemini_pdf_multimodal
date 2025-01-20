import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def create_pdf(text):
    """
    Creates a PDF file with the given text.

    Args:
        text: The text to be written in the PDF.

    Returns:
        The path to the created PDF file.
    """
    pdf_path = "generated_text.pdf" 
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 700, text)
    c.save()
    return pdf_path

def multimodal_prompt(pdf_path, text_prompt):
    """
    Sends a multimodal prompt to the Gemini model with a PDF and a text prompt.

    Args:
        pdf_path: The path to the PDF file.
        text_prompt: The text prompt for the model.

    Returns:
        The model's response as a string.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        # Read PDF data as bytes
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        # Create the PDF input for the model
        pdf_part = {
            "mime_type": "application/pdf",
            "data": pdf_bytes
        }

        # Construct the multimodal prompt
        prompt = [
            f"Analyze the following PDF document and provide insights based on the given prompt: {text_prompt}",
            pdf_part
        ]

        # Send the request to the model
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    # Streamlit UI
    st.title("Multimodal Gemini PDF Analysis App")
    st.write("Upload a PDF file and provide a text prompt.")

    # File uploader for PDF
    uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

    # Text area for user input
    text_prompt = st.text_area("Enter your text prompt:", height=200)

    if uploaded_pdf is not None:
        # Create a temporary PDF file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_pdf.getvalue())

        if st.button("Analyze PDF"):
            with st.spinner("Processing..."):
                response = multimodal_prompt("temp.pdf", text_prompt)
                st.subheader("Response:")
                st.write(response)

if __name__ == "__main__":
    main()