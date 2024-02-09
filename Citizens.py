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
    Invoice_total=list(filter(lambda x:'Invoice Amount' in x,lines))
    t=Invoice_total[0].split(" ")
    print(t[-1])
    print("Lines",lines)
    s_index=None
    e_index=None
    for i,line in enumerate(lines):
        if 'Pisces | Wicth | Length RolNumber | toc | Sidemarke | POF | Weight' in line:
            s_index=i 
        if 'Collect' in line:
            e_index=i 
    print(lines[s_index+1:e_index])
    filtered_list = [item for item in lines[s_index+1:e_index] if item.strip()] 
    items_list=[]
    price=[]
    total_price=[]
    for i in filtered_list:
        t=i.split(" ")
        t=[item for item in t if item.strip()] 
        #print("Hii",t)
       
            #temp=i.split(" ")
            
        print(" ".join(t[:len(t)-3]))
        items_list.append(" ".join(t[:len(t)-3]))
        price.append(t[-1])
    print(items_list)

    data = {'Products':items_list,'Price':price,'Invoice Total':Invoice_total[0]}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

# Example usage
pdf_path = 'Citizens.pdf'

# Extract text from PDF
text = extract_invoice_data(pdf_path)
csv_path = 'Citizens.csv'
save_text_to_csv(text, csv_path)
