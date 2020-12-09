from collections import defaultdict


def get_input_lines():
    return [line.strip() for line in open('input.txt').readlines()]


def get_contained_dict(contained):
    parts = contained.split(' ')
    return {
        'num': int(parts[0]),
        'type': ' '.join(parts[1:3]),
    }


def parse_contained_str(contained_str):
    if 'no other bags' in contained_str:
        return []

    contained_list = contained_str.split(', ')
    return [
        get_contained_dict(contained)
        for contained in contained_list
    ]


def parse_line(line):
    container, contained_str = line.split(' bags contain ')
    return {
        'container': container,
        'contained': parse_contained_str(contained_str)
    }


def get_container_bag_map(parsed_input_lines):
    return {
        parsed_line.get('container'): parsed_line.get('contained')
        for parsed_line in parsed_input_lines
    }


def get_contained_bag_map(parsed_input_lines):
    contained_map = defaultdict(list)

    for line in parsed_input_lines:
        for contained in line.get('contained'):
            contained_map[contained['type']].append(line['container'])

    return contained_map


def get_top_level_containers(bag_type, contained_bag_map, checked_bags=None):
    checked_bags = checked_bags or set()

    top_level_containers = set()
    search_set = { bag_type }

    while search_set:
        current_set = { old_set_val for old_set_val in search_set }
        for current_bag_type in search_set:
            containers = set(contained_bag_map.get(current_bag_type, []))
            new_containers = containers.difference(top_level_containers)
            top_level_containers = top_level_containers.union(new_containers)
            search_set = search_set.union(new_containers)

        search_set = search_set.difference(current_set)

    if bag_type in top_level_containers:
        top_level_containers.remove(bag_type)

    return top_level_containers

def get_contained_bags_count(bag_type, container_bag_map):
    contained_bags = container_bag_map.get(bag_type)

    if not contained_bags:
        return 0

    return (
        sum([
            contained_bag['num'] +
            (get_contained_bags_count(
                contained_bag['type'],
                container_bag_map
            ) * contained_bag['num'])
            for contained_bag in contained_bags
        ])
    )


if __name__ == '__main__':
    input_lines = get_input_lines()
    parsed_input_lines = [parse_line(line) for line in input_lines]

    contained_bag_map = get_contained_bag_map(parsed_input_lines)
    print('Part 1:')
    print(len(get_top_level_containers('shiny gold', contained_bag_map)))

    container_bag_map = get_container_bag_map(parsed_input_lines)
    print('Part 2:')
    print(get_contained_bags_count('shiny gold', container_bag_map))
