import random
import string
__author__ = 'ohaz'

random.seed()
charset = string.ascii_letters + string.digits


def generate_stats(level):
    random.random()
    random.random()

    stats = [random_stat(level), random_stat(level), random_stat(level), random_stat(level), random_stat(level),
             random_stat(level)]
    while sum(stats) not in range(10, 20):
        stats = [random_stat(level), random_stat(level), random_stat(level), random_stat(level), random_stat(level),
                 random_stat(level)]
    return stats


def random_stat(level):
    stat = random.randint(-1, 3)
    i = 0
    for i in range (1, level):
        stat += random.randint(0, 1)

    return stat


def generate_password():
    random.random()
    random.random()
    pw = ''
    for _ in range(15):
        pw += charset[random.randint(0, len(charset) - 1)]
    return pw
