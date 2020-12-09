SLOPES = [
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1),
]


def get_input():
    f = open('input.txt')
    return [[symbol for symbol in line if symbol != '\n'] for line in f.readlines()]


def get_next_position(position, max_len, slope):
    return (
        position[0] + slope[0],
        (position[1] + slope[1]) % max_len
    )


def get_tree_count(tree_map, position, slope):
    value = 0
    max_len = len(tree_map[0])
    try:
        symbol = tree_map[position[0]][position[1]]
        value = 1 if symbol == '#' else 0
    except Exception as e:
        print(e)
        return 0
    return (
        value +
        get_tree_count(
            tree_map,
            get_next_position(position, max_len, slope),
            slope
        )
    )


def main():
    tree_map = get_input()
    result = 1

    for slope in SLOPES:
        slope_tree_count = get_tree_count(tree_map, (0, 0), slope)
        print(f'Slope {slope}: {val}')
        result *= slope_tree_count

    print(result)


if __name__ == '__main__':
    main()
