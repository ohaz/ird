import random
import string
__author__ = 'ohaz'

random.seed()
charset = string.ascii_letters + string.digits


def generate_stats():
    random.random()
    random.random()
    stats = [random_stat(), random_stat(), random_stat(), random_stat(), random_stat(), random_stat()]
    while sum(stats) not in range(10, 20):
        stats = [random_stat(), random_stat(), random_stat(), random_stat(), random_stat(), random_stat()]
    return stats


def random_stat():
    return random.randint(-1, 3)


def generate_password():
    random.random()
    random.random()
    pw = ''
    for _ in range(15):
        pw += charset[random.randint(0, len(charset) - 1)]
    return pw
