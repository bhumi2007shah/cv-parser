import io
import PyPDF2

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def extract_from_pdf(file):
    text = ""
    #pdfFileObj = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file)
    pagesCount = pdfReader.numPages
    for i in range(0, pagesCount):
        pageObj = pdfReader.getPage(i)
        text += pageObj.extractText()
    return text


# calling above function and extracting text
def extract_text_from_pdf(file_path):
    text = extract_from_pdf(file_path)

    if text != "":
        return text
    else:
        print("nothing extrated from pdf file")
