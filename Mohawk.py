

import PyPDF2
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Example usage
pdf_path = 'Mohawk.pdf'

# Extract text from PDF
text = extract_text_from_pdf(pdf_path)


import re

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def save_text_to_csv(text, csv_path):
    lines = text.split('\n')
    
    #print("Lines",lines)
    invoice_number_pattern = r'INVOICE\s+NO:\s*(\w+)'
    

    invoice_number_match = re.search(invoice_number_pattern, text)
    

    invoice_number = invoice_number_match.group(1) if invoice_number_match else None
   
    print(invoice_number)
    s_index=None
    e_index=None 
    for i,line in enumerate(lines):
        if ' *** SUBTOTAL ' in line:
            e_index=i
        if 'PER ORDER #' in line:
            s_index=i
    #print(lines[s_index+1:e_index])
    products=[]
    for i in lines[s_index+1:e_index]:
        t=i.split(" ")
        if(is_float(t[-1])):
            t=[item for item in t if item.strip()] 
            products.append(t)
            #print(t)

   

    data = {'Products':products,'Invoice Number':invoice_number}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

# Example usage
pdf_path = 'Mohawk.pdf'
text = extract_text_from_pdf(pdf_path)
csv_path = 'Mohawk.csv'
save_text_to_csv(text, csv_path)
