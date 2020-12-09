import re

ALLOWED_ECL_VALUES = {
    'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth',
}


def get_input_lines():
    return open('input.txt').readlines()


def separate_input_lines(input_lines):
    return [
        line.strip() for line in
        ''.join(input_lines).replace('\n', ' ').split('  ')
    ]


def get_passport_dict(input_group):
    kv_raw_pairs = [kv_raw.split(':') for kv_raw in input_group.split(' ')]
    passport_dict = {
        k.strip(): v for [k, v] in kv_raw_pairs
    }
    if 'cid' in passport_dict:
        del passport_dict['cid']
    return passport_dict


def get_passport_list():
    input_lines = get_input_lines()
    input_groups = separate_input_lines(input_lines)
    return [get_passport_dict(input_group) for input_group in input_groups]


class ValueException(Exception):
    pass


class ValueMissingException(ValueException):
    pass


class ValueNotNumberException(ValueException):
    pass


class ValueOutOfRangeException(ValueException):
    pass


class ValueInValuesException(ValueException):
    pass


class ValueRegexException(ValueException):
    pass


def validate_presence(value, tags=''):
    if not value:
        raise ValueMissingException(f'[{tags}] Missing value')
    return True


def validate_number(value, tags=''):
    try:
        return int(value)
    except:
        raise ValueNotNumberException(f'[{tags}] Value "{value}" not a number')
    return True


def validate_range(value, min_value, max_value, tags=''):
    value = validate_number(value)
    if not min_value <= value <= max_value:
        raise ValueOutOfRangeException(
            f'[{tags}] Value "{value}" not in range [{min_value}, {max_value}]'
        )
    return True


def validate_in_values(value, allowed_values, tags=''):
    if value not in allowed_values:
        raise ValueInValuesException(
            f'[{tags}] Value "{value}" not in values {allowed_values}'
        )
    return True


def validate_regex(value, regex, tags=''):
    if not re.match(regex, value):
        raise ValueRegexException(
            f'[{tags}] Value "{value}" did not match regex "{regex}"'
        )


def get_byr_is_valid(value):
    try:
        validate_presence(value, tags='byr')
        validate_range(value, 1920, 2002, tags='byr')
    except ValueException as exc:
        print(exc)
        return False
    return True


def get_iyr_is_valid(value):
    try:
        validate_presence(value, tags='iyr')
        validate_range(value, 2010, 2020, tags='iyr')
    except ValueException as exc:
        print(exc)
        return False
    return True


def get_eyr_is_valid(value):
    try:
        validate_presence(value, tags='eyr')
        validate_range(value, 2020, 2030, tags='eyr')
    except ValueException as exc:
        print(exc)
        return False
    return True

# a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
def get_hgt_is_valid(value):
    try:
        validate_presence(value, tags='hgt')
        validate_regex(value, '^[0-9]{2,3}(cm|in)')
        if 'cm' in value:
            validate_range(value[:-2], 150, 193, tags='hgt][cm')
        if 'in' in value:
            validate_range(value[:-2], 59, 76, tags='hgt][in')
    except ValueException as exc:
        print(exc)
        return False
    return True


def get_hcl_is_valid(value):
    try:
        validate_presence(value, tags='hcl')
        validate_regex(value, r'^#[0-9a-f]{6}$', tags='hcl')
    except ValueException as exc:
        print(exc)
        return False
    return True


def get_ecl_is_valid(value):
    try:
        validate_presence(value, tags='ecl')
        validate_in_values(value, ALLOWED_ECL_VALUES, tags='ecl')
    except ValueException as exc:
        print(exc)
        return False
    return True


def get_pid_is_valid(value):
    try:
        validate_presence(value, tags='pid')
        validate_regex(value, r'^[0-9]{9}$', tags='pid')
    except ValueException as exc:
        print(exc)
        return False
    return True


def get_cid_is_valid(value):
    return True


VALIDATORS = {
    'byr': get_byr_is_valid,
    'iyr': get_iyr_is_valid,
    'eyr': get_eyr_is_valid,
    'hgt': get_hgt_is_valid,
    'hcl': get_hcl_is_valid,
    'ecl': get_ecl_is_valid,
    'pid': get_pid_is_valid,
    'cid': get_cid_is_valid,
}

def get_passport_is_valid(passport):
    return all(
        VALIDATORS[key](passport.get(key)) for key in VALIDATORS.keys()
    )

if __name__ == '__main__':
    passport_list = get_passport_list()
    count = 0
    for passport in passport_list:
        valid = get_passport_is_valid(passport)
        if valid:
            count += 1

    print(count)
