# attacks.py - holds all attacks and attack info 
import random

def sword(health):
    dam = random.randint(2,5)
    return health - dam, dam


def spell(health):
    dam = random.randint(3,6)
    return health - dam, dam
    