import random

def random_alpha_string(k=8):
    return ''.join(random.choices('qwertyuiopasdfghjklzxcvbnm', k=k))

def random_number_string(k=8):
    return ''.join(random.choices('0123456789', k=k))

def print_flush(str):
    print(str, flush=True)
