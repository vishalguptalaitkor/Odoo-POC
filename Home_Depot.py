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
    print("Lines",lines)
    Order_Number=list(filter(lambda x:'Order #' in x,lines))
    Order_Total=list(filter(lambda x:'Order Total' in x,lines))
    Delivery_Charge=list(filter(lambda x:'Delivery Charge' in x,lines))
    print("Order",Order_Number)
    s_index=None
    e_index=None
    for i,line in enumerate(lines):
        if 'Item Description Qty Unit Price Discount Net Unit Price Pre Tax Amount' in line:
            s_index=i 
        if 'Subtotal' in line:
            e_index=i 
    print(lines[s_index+1:e_index])
    products=[]
    quantity=[]
    price=[]
    total=[]
    discount=[]
    for i in lines[s_index+1:e_index]:
        t=i.split(" ")
        last=t[-1]
        #print(str(t[-1]).isnumeric())
        if(is_float(last[1:])):
            product_name=" ".join(t[0:len(t)-5])
            products.append(product_name)
            quantity.append(t[-5])
            price.append(t[-4])
            discount.append(t[-3])
            total.append(t[-1])

   
    print(products)
    print(discount)
    data = {'Order_Number':Order_Number,'Product':products,'Quantity':quantity,'Price':price,'Discount':discount,'Total':total,'Order_Total':Order_Total,'Delivery_Charge':Delivery_Charge}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

# Example usage
pdf_path = 'Home Depot.pdf'

# Extract text from PDF
text = extract_invoice_data(pdf_path)

csv_path = 'Home_Depot.csv'
save_text_to_csv(text, csv_path)

# # Find the index of the line containing "Invoice due date is"
# lines = text.split('\n')
# print(lines)