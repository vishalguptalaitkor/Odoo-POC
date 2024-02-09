#print("hello")
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
    Invoice_date=list(filter(lambda x:'Invoice due date is' in x,lines))
    Invoice_total=list(filter(lambda x:'Invoice Total' in x,lines))
    dindex=None
    index1=None
    s_index=None
    e_index=None
    for i,line in enumerate(lines):
        #print(line)
        if 'Date Customer # Branch Rep Page' in line:
            dindex=i

        if 'Invoice # Order # Customer P/O #' in line:
            print("Hiiii")
            index1=i
        if 'Ordered Back Ordered Shipped Unit Price Total Price' in line:
            s_index=i
        if 'Sub Total' in line:
            e_index=i
    #print(index1)
    #print(len(lines))
    print(lines[s_index+1:e_index])
    filtered_list = [item for item in lines[s_index+1:e_index] if item.strip()] 
    items_list=[]
    unit=[]
    price=[]
    total_price=[]
    for i in filtered_list:
        t=i.split(" ")
        #print(str(t[-1]).isnumeric())
        if(is_float(t[-1])):
            item,un,pr,tp=i.split(" ")
            items_list.append(item)
            unit.append(un)
            price.append(pr)
            total_price.append(tp)


    I,O,C=lines[index1+2].split(" ")
    temp=list(lines[dindex+1].split(" "))
    print(I,O,C)
    data = {'date':temp[0],'Invoice_date':Invoice_date,'Invoice_total':Invoice_total,'Invoice Number':I,'Order Number':O,'Customer P/O':C,'items':items_list,'unit':unit,'price':price,'total_price':total_price}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
pdf_path = 'Cartwright.pdf'
csv_path = 'cart.csv'

# Extract invoice data
invoice_data = extract_invoice_data(pdf_path)

# Write data to CSV
save_text_to_csv(invoice_data, csv_path)

print(f"Invoice data has been extracted from '{pdf_path}' and saved to '{csv_path}'.")
