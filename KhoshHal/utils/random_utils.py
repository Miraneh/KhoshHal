import random
import string


class RandomStringGen:
    def __init__(self, length):
        self.length = length
        self.charset = string.ascii_uppercase
        self.charset += string.ascii_lowercase
        self.charset += string.digits

    def gen(self):
        return ''.join(random.choices(
            self.charset,
            k=self.length,
        ))


def random64():
    return RandomStringGen(64).gen()


def random32():
    return RandomStringGen(32).gen()