import string


def get_input_lines():
    return open('input.txt').readlines()


def separate_input_lines(input_lines):
    return [
        line.strip() for line in
        ''.join(input_lines).replace('\n', ' ').split('  ')
    ]


def get_answer_sets(groups):
    return [
        set(group.replace(' ', '')) for group in groups
    ]


def get_all_yes_quesions_for_group(group):
    answer_sets = [set(answers) for answers in group.split(' ')]
    common_answers = set(string.ascii_lowercase)
    for answer_set in answer_sets:
        common_answers = common_answers.intersection(answer_set)
    return common_answers


def get_all_yes_quesions_for_groups(groups):
    return [
        get_all_yes_quesions_for_group(group) for group in groups
    ]


if __name__ == '__main__':
    lines = get_input_lines()
    groups = separate_input_lines(lines)
    answer_sets = get_all_yes_quesions_for_groups(groups)
    result = sum(len(answer_set) for answer_set in answer_sets)
    print(result)
