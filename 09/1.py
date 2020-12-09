def get_input_values():
    return [int(line.strip()) for line in open('input.txt').readlines()]


def get_is_valid(value, preamble):
    for (i, preamble_1) in enumerate(preamble):
        for preamble_2 in preamble[i:]:
            if preamble_1 + preamble_2 == value:
                return True
    return False


def get_first_invalid_value(values, preamble_size):
    current_index = preamble_size
    preamble = values[:current_index]

    while get_is_valid(values[current_index], preamble):
        current_index += 1
        preamble = values[current_index - preamble_size:current_index]

    return values[current_index]


def get_weakness_slice(values, target):
    current_index = 0
    for index in range(len(values)):
        count = 1
        slice = values[index:index + count]
        slice_sum = sum(slice)

        while slice_sum < target:
            count += 1
            slice = values[index:index + count]
            slice_sum = sum(slice)

        if slice_sum == target:
            return slice


if __name__ == '__main__':
    values = get_input_values()
    preamble_size = 25

    first_invalid_value = get_first_invalid_value(values, preamble_size)
    print(f'Part 1: {first_invalid_value}')

    weakness_slice = get_weakness_slice(values, first_invalid_value)
    weakness = min(weakness_slice) + max(weakness_slice)
    print(f'Part 2: {weakness}')
