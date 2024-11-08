import streamlit as st
import random
from PIL import Image
import time

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
                <p>A smart AI-based application to automate invoice and inventory management, improving operational efficiency and reducing errors for small and medium businesses.</p>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # File uploader for PDF processing
    st.write("### Upload a PDF to Analyze")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

    # Mock data simulating the PDF processing output
    return_dict = {
        1: {
            "products": [
                {"description": "Product A", "quantity": "2", "price": 10.00, "sell_price": 0, "qrcode_number": 0, "taxable_amount": 20.00, "vat": 2.00, "total": 22.00},
                {"description": "Product B", "quantity": "1", "price": 15.00, "sell_price": 0, "qrcode_number": 0, "taxable_amount": 15.00, "vat": 1.50, "total": 16.50}
            ],
            "additional_info": "This is some additional invoice info for page 1."
        },
        2: {
            "products": [
                {"description": "Product C", "quantity": "3", "price": 7.00, "sell_price": 0, "qrcode_number": 0, "taxable_amount": 21.00, "vat": 2.10, "total": 23.10}
            ],
            "additional_info": "This is some additional invoice info for page 2."
        }
    }

    # Step 1: Display the upload screen
    if uploaded_pdf:
        st.write("Uploading and processing your PDF...")
        progress_bar = st.progress(0)  # Initial progress bar

        # Simulate the upload and waiting process (e.g., 10 seconds)
        for i in range(10):
            time.sleep(1)  # Simulate time taken to process
            progress_bar.progress((i + 1) * 10)  # Update progress

        # After 10 seconds, show the result page with table
        st.write("Upload successful! Processing your invoice...")

        # Store the data for the next page
        st.session_state['table_data'] = []
        for page_num, content in return_dict.items():
            for item in content.get("products", []):
                st.session_state['table_data'].append(item)

        # Add a small delay before showing the result
        time.sleep(2)

    # Step 2: Display the invoice table after processing (this is the same page)
    if 'table_data' in st.session_state:
        st.title("Invoice Details")

        # Define headers for the invoice table
        table_data = []
        table_data.append(["Description/Product", "Quantity", "Cost Price", "Sell Price", "Qr Number", "Taxable Amount", "VAT", "Total", "Actions"])

        # Append rows of invoice details
        for i, item in enumerate(st.session_state.table_data):
            row = [
                item["description"],
                item["quantity"],
                item["price"],
                item["sell_price"],
                item["qrcode_number"],
                item["taxable_amount"],
                item["vat"],
                item["total"]
            ]
            table_data.append(row)

        # Display the table with the data
        st.dataframe(table_data, use_container_width=True)

        # Inputs for discount percentage
        discount_input = st.text_input("Enter Percentage", value="0")

        try:
            discount_percentage = float(discount_input)
            if 0 <= discount_percentage <= 100:
                if st.button("Generate Sell Price for All Products"):
                    # Calculate sell price for all products based on the discount percentage
                    for item in st.session_state.table_data:
                        cost_price = item["price"]
                        discount_price = cost_price * (discount_percentage / 100)
                        sell_price = cost_price + discount_price
                        item["sell_price"] = sell_price
                    #st.success(f"Sell Price updated for all products with {discount_percentage}% discount.")
            else:
                st.error("Please enter a valid discount percentage between 0 and 100.")
        except ValueError:
            st.error("Please enter a valid number.")

        # Button for generating QR codes for all products
        if st.button("Generate Bar Code Number for All Products"):
            for item in st.session_state.table_data:
                # Generate a random 14-digit number as a string for QR code
                barcode_number = ''.join([str(random.randint(0, 9)) for _ in range(14)])
                item["qrcode_number"] = barcode_number
            #st.success("Barcode number  generated for all products.")

        # Bottom section with additional information extracted by the AI
        st.write("---")  # Divider line

        with st.expander("Additional Details"):
            for page_num, content in return_dict.items():
                additional_info = content.get("additional_info", "")
                st.write(f"Page {page_num + 1}: {additional_info}")

if __name__ == "__main__":
    run_app()