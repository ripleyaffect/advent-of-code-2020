def get_input_seat_map():
    return [
        [seat for seat in line.strip()]
        for line in open('input.txt').readlines()
    ]

class Layout():
    SEAT_INDEX_DIFFS = [
        (-1, -1), (-1, +0), (-1, +1),
        (+0, -1),           (+0, +1),
        (+1, -1), (+1, +0), (+1, +1),
    ]
    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'

    def __init__(self, seat_map):
        self.seat_map = seat_map
        self.col_size = len(seat_map)
        self.row_size = len(seat_map[0] if seat_map else 0)

        self.seats_changed = -1
        self.steps_run = 0

    def print_seat_map(self, seat_map=None):
        seat_map = seat_map or self.seat_map

        for row in seat_map:
            print(''.join(row))

    def get_seat_symbol(self, seat_index):
        return self.seat_map[seat_index[0]][seat_index[1]]

    def get_new_seat_index(self, seat_index, seat_index_diff):
        return (
            seat_index[0] + seat_index_diff[0],
            seat_index[1] + seat_index_diff[1],
        )

    def get_surrounding_seat_indexes(self, seat_index):
        seat_indexes = [
            self.get_new_seat_index(seat_index, seat_index_diff)
            for seat_index_diff in self.SEAT_INDEX_DIFFS
        ]

        # Filter out any seats off the edge of the map
        return [
            seat_index for seat_index in seat_indexes
            if (
                -1 < seat_index[0] < self.col_size and
                -1 < seat_index[1] < self.row_size
            )
        ]

    def get_surrounding_seat_symbols(self, seat_index):
        surrounding_seat_indexes = self.get_surrounding_seat_indexes(seat_index)
        return [
            self.get_seat_symbol(surrounding_seat_index)
            for surrounding_seat_index in surrounding_seat_indexes
        ]

    def get_seen_seat_symbol(self, seat_index, direction):
        symbol = None
        while symbol is None:
            seat_index = self.get_new_seat_index(seat_index, direction)
            if not (
                -1 < seat_index[0] < self.col_size and
                -1 < seat_index[1] < self.row_size
            ):
                break
            seat_symbol = self.get_seat_symbol(seat_index)
            if seat_symbol != self.FLOOR:
                symbol = seat_symbol
        return symbol

    def get_seen_seat_symbols(self, seat_index):
        seen_seat_symbols = []
        for direction in self.SEAT_INDEX_DIFFS:
            seat_symbol = self.get_seen_seat_symbol(seat_index, direction)
            if seat_symbol:
                seen_seat_symbols.append(seat_symbol)
        return seen_seat_symbols

    def get_next_seat_symbol(self, seat_index):
        seat_symbol = self.get_seat_symbol(seat_index)

        if seat_symbol == '.':
            return '.'

        # For Part 1
        # surrounding_seat_symbols = self.get_surrounding_seat_symbols(seat_index)
        surrounding_seat_symbols = self.get_seen_seat_symbols(seat_index)

        if seat_symbol == self.EMPTY:
            if surrounding_seat_symbols.count(self.OCCUPIED) == 0:
                self.seats_changed += 1
                return self.OCCUPIED
            return seat_symbol

        if surrounding_seat_symbols.count(self.OCCUPIED) >= 5:
            self.seats_changed += 1
            return self.EMPTY
        return seat_symbol

    def get_next_seat_map(self):
        new_map = []

        for row, _ in enumerate(self.seat_map):
            new_row = []
            for col, _ in enumerate(self.seat_map[row]):
                new_row.append(self.get_next_seat_symbol((row, col)))
            new_map.append(new_row)

        return new_map

    def get_seats_of_type(self, seat_symbol):
        return sum(
            row.count(seat_symbol) for row in self.seat_map
        )

    def run_step(self):
        self.seats_changed = 0
        self.seat_map = self.get_next_seat_map()
        self.steps_run += 1

if __name__ == "__main__":
    layout = Layout(get_input_seat_map())

    while layout.seats_changed != 0:
        layout.run_step()

    print(f'Part 2: {layout.get_seats_of_type(layout.OCCUPIED)}')
