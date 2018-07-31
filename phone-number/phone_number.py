import re

class Phone(object):

    PUNCTUATION = re.compile(r"[.\s\-\+\(\)]")
    VALID_CODES = [str(i) for i in range(2,10)]
    VALID_COUNTRY_CODES = [str(i) for i in range(1,2)]

    def __init__(self, phone_number):
        number = Phone.PUNCTUATION.sub("", phone_number)
        Phone.raise_for_invalid_length(number)

        self.country_code, self.number = extract_country_code
        self.area_code = self.number[:3]

        Phone.raise_for_invalid_area_code(self.area_code)
        Phone.raise_for_invalid_exchange_code(self.number)
        Phone.raise_for_invalid_country_code(self.country_code)

    def extract_country_code(number):
        if len(number) > 10:
            return number[0], number[1:]
        else:
            return "1", number

    def pretty(self):
        return "({}) {}-{}".format(self.number[:3], self.number[3:6], self.number[6:])

    def raise_for_invalid_length(number):
        if len(number) > 11 or len(number) < 10:
            raise ValueError("Incorrect phone number {}".format(phone_number))
    def raise_for_invalid_area_code(area_code):
        if area_code[0] not in Phone.VALID_CODES:
            raise ValueError("Area code ({}) shouldn't start with a {}.".format(area_code, area_code[0]))
    def raise_for_invalid_exchange_code(number):
        if number[3] not in Phone.VALID_CODES:
            raise ValueError("Number ({}) is not valid exchange code shouldn't be a {}.".format(number, number[3]))
    def raise_for_invalid_country_code(country_code):
        if country_code not in Phone.VALID_COUNTRY_CODES:
            raise ValueError("Country code should be one of {} and not {}.".format(Phone.VALID_COUNTRY_CODES, country_code))
