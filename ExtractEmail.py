import re


def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            email = email[0].split()[0].strip(';')
            email = email.replace("Email:", "")
            email = email.replace("email:", "")
            return email
        except IndexError:
            return None
