import pdfplumber
import re

def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


def basic_field_extraction(text):
    data = {}

    policy_no = re.search(r'Policy Number[:\s]+(\w+)', text)
    premium = re.search(r'Premium[:\s]+\$?([\d,]+)', text)
    date = re.search(r'Date[:\s]+([\d/-]+)', text)

    data['policy_number'] = policy_no.group(1) if policy_no else "Not found"
    data['premium'] = premium.group(1) if premium else "Not found"
    data['date'] = date.group(1) if date else "Not found"

    return data