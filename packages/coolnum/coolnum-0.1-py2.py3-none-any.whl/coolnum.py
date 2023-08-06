
def percentToFloat(text):
    ''' percentToFloat('3.5%') -> 0.035 '''
    if type(text) in (float, int):
        return text
    if '%' in text:
        return float(text[:-1]) / 100
    if '‰' in text:
        return float(text[:-1]) / 1000
    return float(text)