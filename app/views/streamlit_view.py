import streamlit as st
from app.controllers import pdf_controller
import time
import fitz
import os

def run_app():
    # Page configuration
    st.set_page_config(page_title="Bayyen - Smart Invoice Management", page_icon="📄")

    # Custom CSS to mimic hero section styling
    st.markdown("""
        <style>
            /* Hero Section Styling */
            .hero {
                color: #ffffff;
                padding: 40px 0;
                text-align: center;
            }
            .hero h2 {
                font-size: 2.5em;
                margin-bottom: 0.2em;
            }
            .hero p {
                font-size: 1.2em;
                margin-bottom: 1.5em;
            }
            .hero .btn {
                background-color: #ffffff;
                color: #2fa1ff;
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: bold;
            }
            .hero .btn:hover {
                background-color: #e6e6e6;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <section class="hero">
            <div class="container">
                <img src="https://cdn.discordapp.com/attachments/1304510211129741323/1304535075555381258/SPOILER_logo.png?ex=672fbe77&is=672e6cf7&hm=108c32da08e5baa4a698ef32f278f91819d32982a01ba8cfefa076723fb64a2b&" style="width: 150px; height: 150px" />
                <h2>Baen</h2>
                <p>A smart AI-based application to automate invoice and inventory management, 
                   improving operational efficiency and reducing errors for small and medium businesses.</p>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # File uploader for PDF processing
    st.write("### Upload a PDF to Analyze")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

    # PDF processing logic
    if uploaded_pdf is not None:
        # Save the uploaded PDF to a temporary file
        temp_pdf_path = "temp_uploaded.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        # Count pages in the PDF
        doc = fitz.open(temp_pdf_path)
        num_pages = len(doc)
        doc.close()

        st.info(f"The file has {num_pages} pages. Please wait while we process.")
        progress_bar = st.progress(0)

        # Simulated progress
        for i in range(100):
            progress_bar.progress(i / 100)
            time.sleep(0.20)

        # Process PDF pages after progress
        return_dict = pdf_controller.process_page_sequentially(temp_pdf_path, num_pages)
        progress_bar.progress(1.0)

        # Optional: Remove the temporary PDF file after processing
        # os.remove(temp_pdf_path)

        # Display analysis results
        st.subheader("Analysis Results:")
        for page_num, content in return_dict.items():
            with st.expander(f"Page {page_num + 1}"):
                print(content)
                st.write(content)

    else:
        st.write("Please upload a PDF file to analyze.")