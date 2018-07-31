from string import ascii_lowercase, ascii_uppercase

ALPHABET_SIZE = len(ascii_lowercase)

def rotating_cipher(alphabet, key):
    def rotation(i):
        return (i+key)%ALPHABET_SIZE
    return { alphabet[i]:alphabet[rotation(i)] for i in range(ALPHABET_SIZE) }

def ascii_rotating_cipher(key):
    lower = rotating_cipher(ascii_lowercase, key)
    upper = rotating_cipher(ascii_uppercase, key)
    return {**lower, **upper}

def rotate(text, key):
    cipher = ascii_rotating_cipher(key)
    return ''.join( cipher[c] if c in cipher else c for c in text )
