import PyPDF2
import pdfplumber
import pytesseract
from PIL import Image
import io
import pandas as pd

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text
def extract_invoice_data(pdf_path):
    #invoice_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract images from PDF page
            images = page.images
            full_text=''
            for img in images:
                # Get the image bytes
                img_bytes = io.BytesIO(img["stream"].get_data())
                # Open the image using PIL
                img_pil = Image.open(img_bytes)
                # Perform OCR on the image to extract text
                text = pytesseract.image_to_string(img_pil)
                full_text+=text
                # Example: Extract invoice number
                invoice_number = 123
                # Extract other data fields similarly
                
    #print(full_text)
    return full_text

def save_text_to_csv(text, csv_path):
    lines = text.split('\n')
    
    #print("Lines",lines)
    s_index=None
    e_index=None
    i_index=None
    for i,line in enumerate(lines):
        if 'Line Style Size Order Qty Price Roll Number Amount' in line:
            s_index=i
        if 'TOTAL SQUARE YARDS' in line:
            e_index=i
        if 'INVOICE TOTAL' in line:
            i_index=i
    #print(lines[s_index+1:e_index])
    print(lines[i_index+1])
    filtered_list = [item for item in lines[s_index+1:e_index] if item.strip()] 
    items_list=[]
   
    for i in filtered_list:
        t=i.split(" ")
        if(is_float(t[-1])):
            items_list.append(t)
  
    
   

    data = {'Products':items_list,'Invoice Total':lines[i_index+1]}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

# Example usage
pdf_path = 'Engineer.pdf'

# Extract text from PDF
text = extract_invoice_data(pdf_path)

csv_path = 'Engineer.csv'
save_text_to_csv(text, csv_path)