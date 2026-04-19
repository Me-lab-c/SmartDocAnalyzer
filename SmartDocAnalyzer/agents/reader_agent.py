import pandas as pd
import PyPDF2
from docx import Document
import re


def clean_text(text):
    # 🔥 KEEP line breaks (IMPORTANT)
    text = re.sub(r'\r', '', text)

    # Remove extra spaces but NOT newlines
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    return clean_text(text)


def read_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return clean_text(text)


def read_excel(file_path):
    import pandas as pd

    # Read file
    df = pd.read_excel(file_path)

    # 🔥 Remove completely empty rows & columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # 🔥 Fill NaN with empty string
    df = df.fillna("")

    text = ""

    # 🔹 Convert clean data into key:value format
    for _, row in df.iterrows():
        for col in df.columns:
            col_name = str(col).strip()
            value = str(row[col]).strip()

            # ❌ Skip empty or NaN-like values
            if value == "" or value.lower() in ["nan", "none"]:
                continue

            text += f"{col_name}: {value}\n"

        text += "\n"

    return text.strip()

def read_document(file_path):
    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.endswith(".docx"):
        return read_docx(file_path)
    elif file_path.endswith(".xlsx"):
        return read_excel(file_path)
    else:
        return ""