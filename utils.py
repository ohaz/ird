import random
import string
__author__ = 'ohaz'

random.seed()
charset = string.ascii_letters + string.digits

#todo generate stats level-based
def generate_stats(level):
    random.random()
    random.random()
    #todo generate hp instead of sending 0
    stats = [0, random_stat(), random_stat(), random_stat(), random_stat(), random_stat(), random_stat()]
    while sum(stats) not in range(10, 20):
        stats = [0, random_stat(), random_stat(), random_stat(), random_stat(), random_stat(), random_stat()]
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
