#!/usr/bin/env python
import docx2txt


def extract_text_from_doc(file):
    temp = docx2txt.process(file)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)
