class Node():
    def __init__(self, value, prev=None):
        self.value = value
        self.prev = prev
        self.next = None

        # Connect the previous node to self
        if self.prev:
            self.prev.next = self

    def __repr__(self):
        return f'<Node {self.value}>'


class LinkedList():
    def __init__(self, values):
        self.current = Node(values[0])
        self.value_map = {
            self.current.value: self.current,
        }

        self.min_val = values[0]
        self.max_val = values[0]

        prev = self.current

        # Generate the list
        for value in values[1:]:
            prev = Node(value, prev)
            if self.min_val > value:
                self.min_val = value
            if self.max_val < value:
                self.max_val = value
            self.value_map[value] = prev

        # Connect the last node to the first
        self.current.prev = prev
        prev.next = self.current

    @property
    def values(self):
        stop_value = self.current.value

        values = [self.current.value]
        self.increment()

        while self.current.value != stop_value:
            values.append(self.current.value)
            self.increment()

        return values

    def increment(self):
        self.current = self.current.next

    def find_node(self, value):
        return self.value_map[value]


def get_input(input_file):
    return [int(n) for n in open(input_file).readline().strip()]


class CupGame():
    def __init__(self, cups):
        self.cups = LinkedList(cups)
        self.cups_len = len(cups)

        self.pickup_first = None
        self.pickup_last = None

        self.destination_cup = None

    @property
    def min_val(self):
        return self.cups.min_val

    @property
    def max_val(self):
        return self.cups.max_val

    def print_state(self):
        print(f'cups: {self.cups.values}')
        print(f'pickups: {self.pickup_first}-{self.pickup_last}')
        print(f'destination: {self.destination_cup}')
        print()

    def move_cups(self):
        current_cup = self.cups.current

        self.pickup_first = current_cup.next
        self.pickup_last = self.pickup_first.next.next

        # Close the loop
        self.pickup_first.prev.next = self.pickup_last.next
        self.pickup_last.next.prev = self.pickup_first.prev

        # Get the vals for later
        pointer = self.pickup_first
        picked_up_cups = set([pointer.value])
        while pointer.value != self.pickup_last.value:
            pointer = pointer.next
            picked_up_cups.add(pointer.value)

        # Get the Destination value/node
        destination_val = current_cup.value - 1

        if destination_val < self.min_val:
            destination_val = self.max_val

        while destination_val in picked_up_cups:
            destination_val -= 1
            if destination_val < self.min_val:
                destination_val = self.max_val

        self.destination_cup = self.cups.find_node(destination_val)

        # Insert the cups in the correct location
        self.pickup_first.prev = self.destination_cup
        self.pickup_last.next = self.destination_cup.next

        self.destination_cup.next = self.pickup_first
        self.pickup_last.next.prev = self.pickup_last

        # Prep for the next loop
        self.cups.increment()

        self.pickup_first = None
        self.pickup_last = None
        self.destination_cup = None

    def play(self, rounds):
        for _ in range(rounds):
            self.move_cups()

def run(input_file):
    cups = get_input(input_file)

    # Part 1

    cup_game = CupGame(cups)
    cup_game.play(100)

    while cup_game.cups.current.value != 1:
        cup_game.cups.increment()

    result = ''.join([str(v) for v in cup_game.cups.values[1:]])
    print(f'Part 1: {result}')

    # Part 2

    cup_game = CupGame(cups + list(range(10, 1_000_001)))
    cup_game.play(10_000_000)

    cup_1 = cup_game.cups.find_node(1)
    result = cup_1.next.value * cup_1.next.next.value
    print(f'Part 2: {result}')


if __name__ == "__main__":
    run('input.txt')
