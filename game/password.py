from itertools import cycle
from base64 import b64encode
from base64 import b64decode
from string import ascii_lowercase
from secrets import choice

from termcolor import cprint

from game.database import target_details


def password(target: dict) -> bool:
    tgt = target_details(target)

    secret = tgt.get("password")
    hidden = [char for char in secret]
    board  = ["_" for x in hidden]

    if secret:
        while True:
            try:
                user_input = input("enter password: ")
                guess      = [char for char in user_input]
                pad        = len(hidden)
                trimmed    = (guess + pad * ['_'])[:pad]  # padding
                likeness   = board

                # Step through each character
                # Output all the correctly positioned characters
                for i in range(len(hidden)):
                    for c in trimmed:
                        if c in hidden[i]:
                            board[i] = c

                print(" ".join(likeness))

                if hidden == guess:
                    return True

            except KeyboardInterrupt:
                return False

    return True


def encrypt(plaintext: str, key: str) -> str:
    """ input a string to encrypt and an encryption key """
    ciphertext = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(plaintext, cycle(key)))
    return b64encode(ciphertext.encode()).decode()


def decrypt(ciphertext: str, key: str) -> str:
    """ input an encrypted string and the encryption key """
    ciphertext = b64decode(ciphertext.encode()).decode()
    decrypted = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(ciphertext, cycle(key)))
    cprint(decrypted, "green")

    return decrypted
