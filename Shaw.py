
from PIL import Image

import pandas as pd
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def save_text_to_csv(text, csv_path):
    lines = text.split('\n')
    print("Lines",lines)
    t_index=None
    s_index=None
    e_index=None
    o_index=None
    for i,line in enumerate(lines):
        #print(line)
        if 'TAX' in line:
            t_index=i
        if 'ORDER DATE' in line:
            o_index=i

        if 'SHIP DATE' in line:
            print("Hiiii")
            s_index=i
        
        if 'For GCC visit http://productsafety.shawinc.com/' in line:
            e_index=i
    print(lines[t_index].lstrip())
    temp=lines[o_index].lstrip().split(' ')
    date=temp[-1]
    print(lines[s_index+1:e_index])
    
    data = {'Invoice_date':date,'items_details':lines[s_index+1:e_index]}
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
pdf_path = 'Shaw.pdf'
csv_path = 'Shaw.csv'

# Extract invoice data
invoice_data = extract_text_from_pdf(pdf_path)

# Write data to CSV
save_text_to_csv(invoice_data, csv_path)

print(f"Invoice data has been extracted from '{pdf_path}' and saved to '{csv_path}'.")
