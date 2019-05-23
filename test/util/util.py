import random

def get_name(name):
    random_postfix = random.randint(1000, 999999)
    name = '%s_%s' % (name, random_postfix)
    return name