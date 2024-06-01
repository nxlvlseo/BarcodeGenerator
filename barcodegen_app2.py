import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont

# Function to generate barcode image with product name
def generate_barcode_with_name(product_name, upc_code):
    # Truncate product name to 30 characters
    truncated_name = product_name[:30]
    
    UPC = barcode.get_barcode_class('upc')
    upc = UPC(upc_code, writer=ImageWriter())
    barcode_buffer = BytesIO()
    upc.write(barcode_buffer)
    
    barcode_image = Image.open(barcode_buffer)
    width, height = barcode_image.size
    
    # Create a new image with additional space for the product name
    new_height = height + 50
    new_image = Image.new("RGB", (width, new_height), "white")
    draw = ImageDraw.Draw(new_image)
    
    # Load a truetype or opentype font file
    font = ImageFont.load_default()
    
    # Draw the truncated product name at the top
    text_bbox = draw.textbbox((0, 0), truncated_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_position = ((width - text_width) / 2, 10)
    draw.text(text_position, truncated_name, fill="black", font=font)
    
    # Paste the barcode image below the product name
    new_image.paste(barcode_image, (0, 50))
    
    return new_image

# Function to convert image to base64
def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

st.title('Generate UPC-A Barcodes')

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Product Name' in df.columns and 'UPC' in df.columns:
        for index, row in df.iterrows():
            product_name = row['Product Name']
            upc_code = str(row['UPC']).zfill(12)
            barcode_image = generate_barcode_with_name(product_name, upc_code)
            barcode_base64 = image_to_base64(barcode_image)
            st.markdown(f"### {product_name}")
            st.image(f"data:image/png;base64,{barcode_base64}")
            href = f'<a href="data:image/png;base64,{barcode_base64}" download="{upc_code}.png">Download Barcode</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("CSV must contain 'Product Name' and 'UPC' columns.")
