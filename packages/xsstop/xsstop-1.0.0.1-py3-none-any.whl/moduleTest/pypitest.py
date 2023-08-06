import re


def prevent(string):
    string = string.replace('<', '&lt;')
    string = string.replace('>', '&gt;')  # prevent insert tag
    string = string.replace('&', '&amp;')
    string = string.replace('\"', '&quot;')
    string = string.replace('\'', 'ENT_QUOTES;')
    string = re.sub("script|scr|ipt|(|)", "", string, flags=re.IGNORECASE)
    return string
