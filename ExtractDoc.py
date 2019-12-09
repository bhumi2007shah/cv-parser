#!/usr/bin/env python
import textract


def extract_text_from_doc(file):
    temp = textract.process(file).decode("UTF-8")
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)
