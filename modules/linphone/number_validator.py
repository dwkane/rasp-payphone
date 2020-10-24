import phonenumbers


def format_number(number):
    num = phonenumbers.parse(number, "US")
    if not phonenumbers.is_valid_number(num):
        return " ".join(number)
    else:
        print(phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL))
        return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL)


def is_number_valid(number):
    try:
        num = phonenumbers.parse(number, "US")
        return phonenumbers.is_valid_number(num)
    except phonenumbers.NumberParseException:
        return False
