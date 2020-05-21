from game.password import encrypt
from game.password import decrypt

encrypted = encrypt("bacon", "r25KjzgbsKiOUdD7")

print(encrypted)
print(decrypt(encrypted, "r25KjzgbsKiOUdD7"))
