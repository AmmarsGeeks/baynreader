import streamlit as st
import random
from PIL import Image

# Mock data simulating the PDF processing output
return_dict = {
    1: {
        "products": [
            {
                "description": "Product A",
                "quantity": "2",
                "price": 10.00,
                "sell_price": 0,
                "qrcode_number": 0,
                "taxable_amount": 20.00,
                "vat": 2.00,
                "total": 22.00
            },
            {
                "description": "Product B",
                "quantity": "1",
                "price": 15.00,
                "sell_price": 0,
                "qrcode_number": 0,
                "taxable_amount": 15.00,
                "vat": 1.50,
                "total": 16.50
            }
        ],
        "additional_info": "This is some additional invoice info for page 1."
    },
    2: {
        "products": [
            {
                "description": "Product C",
                "quantity": "3",
                "price": 7.00,
                "sell_price": 0,
                "qrcode_number": 0,
                "taxable_amount": 21.00,
                "vat": 2.10,
                "total": 23.10
            }
        ],
        "additional_info": "This is some additional invoice info for page 2."
    }
}

# Streamlit UI layout
st.set_page_config(page_title="Invoice Text Extraction", page_icon="📄")
st.title("📄 Invoice Text Extraction and Analysis")

# Mock invoice image (Placeholder)
invoice_image = Image.open("temp_invoice.jpg")  # Placeholder for the generated image

# Initialize session state for storing table data if not already initialized
if 'table_data' not in st.session_state:
    st.session_state.table_data = []
    for page_num, content in return_dict.items():
        for item in content.get("products", []):
            st.session_state.table_data.append(item)

# Display results in a layout with two columns
with st.container():
    col1, col2 = st.columns([1, 2])

    # Left column - Display the invoice image
    with col1:
        st.subheader("Uploaded Invoice")
        st.image(invoice_image, caption="Invoice Image", use_container_width=True)

    # Right column - Display the invoice details in a table
    with col2:
        st.subheader("Invoice Details")

        # Define headers for the invoice table
        table_data = []
        table_data.append([
            "Description/Product", "Quantity", "Cost Price", "Sell Price", "Qr Number", "Taxable Amount", "VAT", "Total", "Actions"
        ])

        # Append rows of invoice details with buttons for each row
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

            # Add the row with data
            table_data.append(row)

        # Display the updated data in a table using st.dataframe (for better control)
        st.write("---")
        st.dataframe(table_data, use_container_width=True)

        # Inputs for discount percentage
        discount_input = st.text_input("Enter  Percentage", value="0")

        try:
            discount_percentage = float(discount_input)
            if 0 <= discount_percentage <= 100:
                if st.button("Generate Sell Price for All Products"):
                    # Calculate sell price for all products based on the discount percentage
                    for item in st.session_state.table_data:
                        cost_price = item["price"]
                        discount_price = cost_price * (discount_percentage / 100)
                        sell_price = cost_price - discount_price
                        item["sell_price"] = sell_price
                    st.success(f"Sell Price updated for all products with {discount_percentage}%.")
            else:
                st.error("Please enter a valid discount percentage between 0 and 100.")
        except ValueError:
            st.error("Please enter a valid number.")

        # Button for generating QR codes for all products
        if st.button("Generate QR Code for All Products"):
            for item in st.session_state.table_data:
                # Generate a random 14-digit number as a string for QR code
                barcode_number = ''.join([str(random.randint(0, 9)) for _ in range(14)])
                item["qrcode_number"] = barcode_number
            st.success("QR Codes generated for all products.")

        # Bottom section with additional information extracted by the AI
        st.write("---")  # Divider line

        with st.expander("Additional Details"):
            for page_num, content in return_dict.items():
                additional_info = content.get("additional_info", "")
                st.write(f"Page {page_num + 1}: {additional_info}")