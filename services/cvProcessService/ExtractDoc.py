#!/usr/bin/env python
import textract


def extract_text_from_doc(file):
    temp = None
    try:
        temp = textract.process(file)
    except Exception as e:
        return str(e)
    temp = temp.decode("UTF-8")
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ''.join(text)
