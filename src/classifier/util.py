def get_words(content):
    import re
    r = re.compile(r'[a-zA-Z]+|\.\.\.')
    words = re.findall(r, content)
    return [str(word.lower()) for word in words]
