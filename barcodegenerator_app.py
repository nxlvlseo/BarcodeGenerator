import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import base64
from io import BytesIO

# Function to generate barcode image
def generate_barcode(upc_code):
    UPC = barcode.get_barcode_class('upc')
    upc = UPC(upc_code, writer=ImageWriter())
    buffer = BytesIO()
    upc.write(buffer)
    return buffer

# Function to convert image to base64
def image_to_base64(image):
    image.seek(0)
    img_str = base64.b64encode(image.read()).decode()
    return img_str

st.title('Generate UPC-A Barcodes')

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Product Name' in df.columns and 'UPC' in df.columns:
        for index, row in df.iterrows():
            product_name = row['Product Name']
            upc_code = str(row['UPC']).zfill(12)
            barcode_image = generate_barcode(upc_code)
            barcode_base64 = image_to_base64(barcode_image)
            st.markdown(f"### {product_name}")
            st.image(f"data:image/png;base64,{barcode_base64}")
            href = f'<a href="data:image/png;base64,{barcode_base64}" download="{upc_code}.png">Download Barcode</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("CSV must contain 'Product Name' and 'UPC' columns.")
