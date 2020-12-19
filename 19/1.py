import re

MAX_LOOPS = 13


def get_patterns():
    return [line.strip() for line in open('patterns.txt').readlines()]


def parse_value(value):
    return [v.split(' ') for v in value.replace('"', '').split(' | ')]


def parse_line_raw(line_raw):
    code, value = line_raw.split(': ')
    return {
        'code': code,
        'value': parse_value(value)
    }


def get_input_lines():
    return [
        parse_line_raw(line.strip())
        for line
        in open('input.txt').readlines()
    ]


def get_matcher_dict(lines):
    return {line['code']: line['value'] for line in lines}


def get_code_patterns(matcher_dict, depth=0, entry_code='0'):
    values = matcher_dict[entry_code]

    if 'a' in values[0][0] or 'b' in values[0][0]:
        return values[0][0]

    if depth > MAX_LOOPS:
        return ''

    pattern = '|'.join(
        ''.join(get_code_patterns(matcher_dict, depth + 1, v) for v in value)
        for value in values
    ).replace('()', '')

    return f'({pattern})' if depth > 0 else f'^{pattern}$'


def seed_part_2(matcher_dict):
    updates = [
        parse_line_raw(update_line)
        for update_line
        in [
            '8: 42 | 42 8',
            '11: 42 31 | 42 11 31',
        ]
    ]

    matcher_dict.update(get_matcher_dict(updates))

    return matcher_dict


if __name__ == "__main__":
    matcher_dict = get_matcher_dict(get_input_lines())
    patterns = get_patterns()

    # Part 1
    code_patterns = get_code_patterns(matcher_dict, 0)
    part_1 = sum(
        bool(re.match(code_patterns, pattern)) for pattern in patterns
    )
    print(f'Part 1: {part_1}')

    # Part 2
    seed_part_2(matcher_dict)
    code_patterns = get_code_patterns(matcher_dict, 0)
    part_2 = sum(
        bool(re.match(code_patterns, pattern)) for pattern in patterns
    )
    print(f'Part 2: {part_2}')
