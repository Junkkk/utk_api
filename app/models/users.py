import re
from pydantic import BaseModel, validator, constr
from pydantic.schema import EmailStr
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class User(BaseModel):
    phone: constr(max_length=50, strip_whitespace=True) = None
    email: EmailStr
    comment: str

    @validator('phone')
    def check_phone(cls, v):
        """Проверка правильности введеного номера телефона"""
        if v is None:
            return v
        try:
            n = parse_phone_number(v, 'RU')
        except NumberParseException as e:
            raise ValueError('Please provide a valid mobile phone number') from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        return format_number(n, PhoneNumberFormat.NATIONAL if n.country_code == 44 else PhoneNumberFormat.INTERNATIONAL)

    @validator('comment')
    def check_comment(cls, v):
        """Проверка комментария на наличие ссылок внутри"""
        regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([
                    ^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"""
        url = re.findall(regex, v)
        urls = [x[0] for x in url]
        if urls:
            raise ValueError('Comment must not contain the URL')
        return v
