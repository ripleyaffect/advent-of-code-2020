MAGIC_NUMBER = 20201227

def get_input_raw(filename):
    return [int(line.strip()) for line in open(filename).readlines()]


def perform_loop(val, subject_number):
    return (val * subject_number) % MAGIC_NUMBER


def get_loop_size(public_key):
    loop_size = 0
    val = 1
    while val != public_key:
        val = perform_loop(val, 7)
        loop_size += 1
    return loop_size


def transform(key, loop_size):
    val = 1
    for _ in range(loop_size):
        val = perform_loop(val, key)
    return val


def run(filename):
    card_pub_key, door_pub_key = get_input_raw(filename)

    door_loop_size = get_loop_size(door_pub_key)

    result = transform(card_pub_key, door_loop_size)

    print(f'Part 1: {result}')


if __name__ == '__main__':
    run('input.txt')
