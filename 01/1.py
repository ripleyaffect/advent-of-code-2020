import itertools
from functools import reduce


def get_input_values():
    f = open('input.txt')
    return [int(line.strip()) for line in f.readlines()]


def get_unique_sets(values, set_size):
    return [list(combo) for combo in itertools.combinations(values, set_size)]


def get_set_summing_to_target(values, set_size, target):
    for _set in get_unique_sets(values, set_size):
        if sum(_set) == target:
            return _set


def get_product(values):
    return reduce(lambda a, b: a * b, values)


def get_part_1(values):
    return get_product(get_set_summing_to_target(values, 2, 2020))


def get_part_2(values):
    return get_product(get_set_summing_to_target(values, 3, 2020))


def main():
    values = get_input_values()

    print(f'Part 1: {get_part_1(values)}')
    print(f'Part 2: {get_part_2(values)}')


if __name__ == "__main__":
    main()
