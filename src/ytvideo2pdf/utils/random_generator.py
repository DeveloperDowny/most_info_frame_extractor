import random
import string


class RandomGenerator:
    @staticmethod
    def generate_random_word(length: int) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
