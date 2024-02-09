#print("hello")
import pdfplumber
import pytesseract
from PIL import Image
import io
import pandas as pd

def extract_invoice_data(pdf_path):
    #invoice_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
           
            images = page.images
            full_text=''
            for img in images:
                # Get the image bytes
                img_bytes = io.BytesIO(img["stream"].get_data())
                # Open the image using PIL
                img_pil = Image.open(img_bytes)
                # Perform OCR on the image to extract text
                text = pytesseract.image_to_string(img_pil)
                full_text+=text+','
               
                
    print(full_text)
    return full_text

def save_text_to_csv(text, csv_path):
    lines = text.split('\n')
   
    data = {'text': lines}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
pdf_path = 'example.pdf'
csv_path = 'invoice_data.csv'


invoice_data = extract_invoice_data(pdf_path)


save_text_to_csv(invoice_data, csv_path)

print(f"Invoice data has been extracted from '{pdf_path}' and saved to '{csv_path}'.")
