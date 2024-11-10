def replace_latin_with_cyrillic(text):
    replacements = {
        'A': 'А', 'B': 'В', 'E': 'Е', 'K': 'К', 'M': 'М',
        'H': 'Н', 'O': 'О', 'P': 'Р', 'C': 'С', 'T': 'Т',
        'X': 'Х',
        'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р',
        'c': 'с', 'y': 'у', 'x': 'х'
    }

    for latin_char, cyrillic_char in replacements.items():
        text = text.replace(latin_char, cyrillic_char)

    return text
