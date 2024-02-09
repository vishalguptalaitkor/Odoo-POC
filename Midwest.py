import pdfplumber
import pytesseract
from PIL import Image
import io
import pandas as pd
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
    Invoice_total=list(filter(lambda x:'Invoice Total' in x,lines))
    in_index=None
    In_date=None
    product_index=None
    price_index=None
    print(lines)
    for i,line in enumerate(lines):
        if 'Invoice Number' in line:
            in_index=i
        if 'Invoice Date Order Number' in line:
            In_date=i
        if 'Quantity Product' in line:
            product_index=i 
        if 'Price Total T' in line:
            price_index=i
    I,O=lines[In_date+1].split(" ")
    print("kkk",lines[in_index+1])
    products=lines[product_index+2].split(' ')
    quantity=products[0]
    products=[x for x in products[1:]]
    product_name=" ".join(products)
    prices=lines[price_index+2].split(' ')
    print("Prices",product_name)

    #print(Invoice_total)
    data = {'Invoice_total':Invoice_total,'Date':I,'Order Number':O,'Invoice_Number':lines[in_index+1],'Product':product_name,'Quantity':quantity,'Price':prices[0],'Total':prices[2]}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
        

pdf_path = 'Midwest.pdf'
data=extract_invoice_data(pdf_path)
csv_path = 'Midwest.csv'
save_text_to_csv(data, csv_path)

# Extract invoice data