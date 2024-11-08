import streamlit as st
import fitz  # PyMuPDF
import os
import re
import pandas as pd
from PIL import Image
import time

# Function to extract invoice details
def extract_invoice_data(text):
    """
    This function uses regular expressions to extract relevant invoice details 
    from the provided text. It returns the data as a list of dictionaries.
    """
    # Regex pattern for extracting invoice rows
    invoice_pattern = r"([^\d]+)\s+(\d+)\s+([\d,]+(?:\.\d{2})?)\s+([\d,]+(?:\.\d{2})?)\s+([\d,]+(?:\.\d{2})?)\s+([\d,]+(?:\.\d{2})?)"
    invoice_data = []

    # Search for all matches of the pattern in the text
    matches = re.findall(invoice_pattern, text)
    
    for match in matches:
        product_name = match[0].strip()
        quantity = int(match[1])
        price = float(match[2].replace(',', ''))
        taxable_amount = float(match[3].replace(',', ''))
        vat_amount = float(match[4].replace(',', ''))
        total = float(match[5].replace(',', ''))
        
        invoice_data.append({
            "Product/Description": product_name,
            "Quantity": quantity,
            "Price": price,
            "Taxable Amount": taxable_amount,
            "VAT": vat_amount,
            "Total": total
        })

    return invoice_data


# Function to detect text from an image (using OCR or other text recognition method)
def detect_text_from_image(image_content):
    # Placeholder for OCR or text detection logic
    # You can integrate Google Vision API or any other OCR method here
    return "Extracted text from image"  # Replace with actual OCR result


# PDF processing function
def process_page_sequentially(doc_path, num_pages):
    """Process pages sequentially."""
    doc = fitz.open(doc_path)
    return_dict = {}

    for page_num in range(num_pages):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()

        # Convert the image to PIL format
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(f"temp_image_{page_num}.jpg")

        # Read image and analyze text (using OCR or another technique)
        with open(f"temp_image_{page_num}.jpg", "rb") as img_file:
            image_content = img_file.read()
            page_text = detect_text_from_image(image_content)

        # Extract invoice data from the text
        invoice_data = extract_invoice_data(page_text)
        
        # Store the extracted data in the dictionary
        return_dict[page_num] = invoice_data
        
        # Remove temporary image
        os.remove(f"temp_image_{page_num}.jpg")

    doc.close()
    return return_dict


# Streamlit UI for file upload and displaying results
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
                <h2>Bayyen</h2>
                <p>A smart AI-based application to automate invoice and inventory management, 
                   improving operational efficiency and reducing errors for small and medium businesses.</p>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # Streamlit file uploader
    st.write("### Upload a PDF to Analyze")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_pdf is not None:
        # Save and process the PDF file
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

        # Process PDF pages
        return_dict = process_page_sequentially(temp_pdf_path, num_pages)
        progress_bar.progress(1.0)

        # Display invoice details in a table format
        st.subheader("Invoice Details:")

        for page_num, invoice_data in return_dict.items():
            with st.expander(f"Page {page_num + 1}"):
                if invoice_data:
                    # Convert invoice data to a pandas DataFrame and display it
                    df = pd.DataFrame(invoice_data)
                    st.table(df)
                else:
                    st.write("No invoice data found on this page.")
    else:
        st.write("Please upload a PDF file to analyze.")