def filter_empty(text: str) -> str:
    if text == ' ' or not text:
        return 'None'
    else:
        return text


def parse_description(text: str) -> dict:
    return {
        'cost': float(text.split('$')[1]),
        'street_address': ' '.join(text.split(' ,')[0].split(' ')[-2:]),
        # 'state': '',
        # 'zip': ''
    }
