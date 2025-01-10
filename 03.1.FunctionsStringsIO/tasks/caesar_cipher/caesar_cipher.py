def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """

    def newChar(c: str) -> str:
        b = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - b + n) % 26 + b)

    return ''.join(newChar(char) if char.isalpha() else char for char in message)
