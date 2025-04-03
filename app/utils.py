import random
import string

def generate_short_code(r, length=6):  # r을 인자로 받음
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not r.exists(f"short:{code}"):
            return code