def extract_text_from_pdf(self, pdf_file):
    """
    Extracts text from a PDF file using the PyPDF2 library.

    Args:
        pdf_file: The PDF file to extract text from.

    Returns:
        str: The extracted text from the PDF file.
    """

    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for _, page in enumerate(reader.pages):  
        text += page.extract_text()  
    return text