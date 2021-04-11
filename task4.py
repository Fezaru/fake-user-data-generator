import sys
import csv
import time
from mimesis import Generic


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(time.time() - start)

    return wrapper


def handle_language(lang: str):
    if lang == 'en_US':
        return Generic('en')
    elif lang == 'ru_RU':
        return Generic('ru')
    elif lang == 'uk_UA':
        return Generic('uk')
    print('incorrect language string')
    sys.exit(1)


def generate_row(g: Generic):
    return {'fullname': g.person.full_name(),
            'address': g.address.city() + ', ' + g.address.address() + ', ' + g.person.full_name(),
            'telephone': g.person.telephone()}


@calculate_time
def generate_data(g: Generic, n: int, filename: str):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['fullname', 'address', 'telephone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(n):
            writer.writerow(generate_row(g))


if len(sys.argv) != 3:
    print('incorrect arguments quantity')
    sys.exit(1)

try:
    int(sys.argv[1])
except Exception:
    print('first argument must be quantity of lines')
    sys.exit(1)

g = handle_language(sys.argv[2])
generate_data(g, int(sys.argv[1]), 'output.csv')
