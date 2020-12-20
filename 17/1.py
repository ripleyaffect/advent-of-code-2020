from collections import defaultdict
import itertools


def get_diffs():
    diffs = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if i or j or k or l:
                        diffs.append([i, j, k, l])
    return diffs


DIFFS = get_diffs()


def get_input_raw():
    return [[v for v in line.strip()] for line in open('input.txt').readlines()]


def get_initial_coords():
    input_raw = get_input_raw()

    initial_coords = set()

    for (y, col) in enumerate(input_raw):
        for (x, icon) in enumerate(col):
            if icon == '#':
                initial_coords.add(f'[{x}, {-y}, 0, 0]')

    return initial_coords


def parse_coord(coord):
    return [int(i) for i in coord[1:-1].split(',')]


def apply_diff(coord, diff):
    return [
        v + diff[i] for i, v in enumerate(coord)
    ]


def get_coord_neighbors(str_coord):
    coord = parse_coord(str_coord)
    neighbors = [str(apply_diff(coord, diff)) for diff in DIFFS]
    return neighbors


def get_neighbors_map(coords):
    neighbors_map = defaultdict(int)

    for coord in coords:
        for neighbor in get_coord_neighbors(coord):
            neighbors_map[neighbor] += 1

    return neighbors_map


def get_next_state(current_state, neighbor_count):
    # If a cube is active and exactly 2 or 3 of its neighbors are also active,
    # the cube remains active. Otherwise, the cube becomes inactive.
    if current_state == '#':
        return '#' if neighbor_count in {2, 3} else '.'
    # If a cube is inactive but exactly 3 of its neighbors are active,
    # the cube becomes active. Otherwise, the cube remains inactive.
    else:
        return '#' if neighbor_count == 3 else '.'


def get_next_coords(str_coords):
    neighbors_map = get_neighbors_map(str_coords)
    next_coords = set()

    all_str_coords = str_coords.union(set(neighbors_map.keys()))

    for str_coord in all_str_coords:
        next_state = get_next_state(
            '#' if str_coord in str_coords else '.',
            neighbors_map.get(str_coord, 0)
        )
        if next_state == '#':
            next_coords.add(str_coord)

    return next_coords


if __name__ == "__main__":
    next_coords = get_initial_coords()

    for x in range(6):
        next_coords = get_next_coords(next_coords)
        print(len(next_coords))
