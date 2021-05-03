#guess XOR key length, adapted from xortool

from operator import itemgetter

def guess_key_length(text):
    """
    Try key lengths from 1 to max_key_length and print local maximums
    Set key_length to the most possible if it's not set by user.
    """
    fitnesses = calculate_fitnesses(text)
    #print(fitnesses)
    return get_max_fitnessed_key_length(fitnesses)

def calculate_fitnesses(text):
    """Calculate fitnesses for each keylen"""
    prev = 0
    pprev = 0
    fitnesses = []
    for key_length in range(1, 10 + 1):
        fitness = count_equals(text, key_length)

        # smaller key-length with nearly the same fitness is preferable
        fitness = (float(fitness) /
                   (10 + key_length ** 1.5))

        if pprev < prev and prev > fitness:  # local maximum
            fitnesses += [(key_length - 1, prev)]

        pprev = prev
        prev = fitness

    if pprev < prev:
        fitnesses += [(key_length - 1, prev)]

    return fitnesses

def calculate_fitness_sum(fitnesses):
    return sum([f[1] for f in fitnesses])

def count_equals(text, key_length):
    """Count equal chars count for each offset and sum them"""
    equals_count = 0
    if key_length >= len(text):
        return 0

    for offset in range(key_length):
        chars_count = chars_count_at_offset(text, key_length, offset)
        equals_count += max(chars_count.values()) - 1  # why -1? don't know
    return equals_count

def get_max_fitnessed_key_length(fitnesses):
    max_fitness = 0
    max_fitnessed_key_length = 0
    for key_length, fitness in fitnesses:
        if fitness > max_fitness:
            max_fitness = fitness
            max_fitnessed_key_length = key_length
    return max_fitnessed_key_length, max_fitness

def chars_count_at_offset(text, key_length, offset):
    chars_count = dict()
    for pos in range(offset, len(text), key_length):
        c = text[pos]
        if c in chars_count:
            chars_count[c] += 1
        else:
            chars_count[c] = 1
    return chars_count
