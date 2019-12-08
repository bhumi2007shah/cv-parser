import re


def extract_mobile_number(text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    if phone:
        if len(phone) == 1:
            number = ''.join(phone[0])
            return number
        elif len(phone) > 1:
            phone_number = []
            for number in phone:
                temp_number = ''.join(number)
                if(len(temp_number)>10 and not "+" in temp_number):
                    temp_number = "+"+temp_number
                phone_number.append(temp_number)

            phone_number = ','.join(phone_number)
            return phone_number