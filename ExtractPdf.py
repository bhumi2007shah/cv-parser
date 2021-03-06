import PyPDF2
import textract


def extract_from_pdf(file, file_path):
    text = ""
    if file_path is not None:
        text = textract.process(file_path, method='tesseract', language='eng')

    if text != "":
        return text
    else:
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
