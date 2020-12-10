from functools import reduce


def get_input_ratings():
    return [int(line.strip()) for line in open('input.txt').readlines()]


def get_all_ratings():
    ratings = get_input_ratings()
    ratings.sort()

    device_rating = max(ratings) + 3

    return ratings + [device_rating]


def get_rating_differences(ratings):
    diffs = []
    current = 0

    for rating in ratings:
        diffs.append(rating - current)
        current = rating

    return diffs


def get_one_sets(diffs):
    """Return a list of counts of 1 sequences

    The paths diverge on consecutive sets of numbers:

    1, 2, 3 => 2 paths
        [1, 2 ,3]
        [1, 3]
    1, 2, 3, 4 => 4 paths:
        [1, 2, 3, 4]
        [1, 2, 4]
        [1, 3, 4]
        [1, 4]

    After convergence the path can split again. We can get a multipler
    for each of these splits and multiply these together for the total
    number of paths.

    """
    sets = []
    current = 0
    for diff in diffs:
        if diff == 1:
            current += 1
        else:
            sets.append(current)
            current = 0
    return sets


def get_multiplier(value):
    # Easier to just hard code these
    # Each set of n 1s gives a multiplier for the # of branches
    # Kinda like fibonacci but sum of last 3 nums
    return [1, 1, 2, 4, 7, 13, 24][value]


def get_product(values):
    return reduce(lambda a, b: a * b, values, 1)


def main():
    all_ratings = get_all_ratings()

    diffs = get_rating_differences(all_ratings)
    print(f'Part 1: {diffs.count(1) * diffs.count(3)}')

    one_sets = get_one_sets(diffs)
    multipliers = [get_multiplier(one_set) for one_set in one_sets]
    print(f'Part 2: {get_product(multipliers)}')


if __name__ == '__main__':
    main()
