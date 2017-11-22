import bleach
import re


def strip_all_tags(value):
    return bleach.clean(value, tags=[], strip=True)


def extract_text(value):
    value = strip_all_tags(value)
    return ' '.join(re.findall(r'(\b\w+)', value))
