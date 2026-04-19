def classify_document(text):
    if text.count("?") > 5:
        return "Questionnaire/Form"
    elif "invoice" in text.lower():
        return "Invoice"
    else:
        return "General Document"