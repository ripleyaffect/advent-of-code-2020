def get_input_lines():
    return [line.strip() for line in open('input.txt').readlines()]


def get_pieces_raw():
    input_lines = get_input_lines()

    pieces_raw = []

    code = None
    rows = []

    for line in input_lines:
        if 'Tile' in line:
            code = line[5:-1]
        elif line == '':
            pieces_raw.append((code, rows))
            code = None
            rows = []
        else:
            rows.append([v for v in line])

    pieces_raw.append((code, rows))

    return pieces_raw


class Piece():
    def __init__(self, code, rows):
        self.code = int(code)
        self.rows = rows
        self.sides = self.get_sides_set(rows)
        self.neighbors = []
        self.matched_neighbor_codes = []

    @property
    def top(self):
        return ''.join(self.rows[0])

    @property
    def right(self):
        return ''.join(row[-1] for row in self.rows)

    @property
    def bottom(self):
        return ''.join(self.rows[-1])

    @property
    def left(self):
        return ''.join(row[0] for row in self.rows)

    @property
    def is_corner(self):
        return len(self.neighbors) == 2

    @property
    def sliced_rows(self):
        return [
            row[1:-1]
            for row in self.rows[1:-1]
        ]

    def print(self):
        for row in self.rows:
            print(''.join(row))

    def get_sides_set(self, rows):
        """Return `set` of possible sides

        :param rows: `list` of `list`s of icons

        """
        return {
            self.top,
            self.top[::-1],
            self.right,
            self.right[::-1],
            self.bottom,
            self.bottom[::-1],
            self.left,
            self.left[::-1],
        }

    def get_opposite_side(self, side):
        if side == self.top: return self.bottom
        elif side == self.bottom: return self.top
        elif side == self.left: return self.right
        elif side == self.right: return self.left

    def get_matching_sides(self, other_piece):
        return self.sides.intersection(other_piece.sides)

    def get_neighbors(self, pieces):
        neighbors = []
        for piece in pieces:
            if piece.code != self.code:
                matching_sides = self.get_matching_sides(piece)
                if self.get_matching_sides(piece):
                    neighbors.append(piece)
        return neighbors


    def add_neighbors(self, neighbors):
        self.neighbors += neighbors

    def get_neighbor_on_side(self, side):
        for neighbor in self.neighbors:
            if side in self.get_matching_sides(neighbor):
                return neighbor
        return None

    def rotate_right(self):
        new_rows = [[] for r in self.rows]
        for row in self.rows[::-1]:
            for j, val in enumerate(row):
                new_rows[j].append(val)
        self.rows = new_rows

    def flip(self):
        self.rows = self.rows[::-1]

    def flip_y(self):
        self.flip()
        self.rotate_right()
        self.rotate_right()

    def __str__(self):
        return f'<Piece {self.code}>'

    def __repr__(self):
        return f'<Piece {self.code}>'


class Puzzle():
    def __init__(self, pieces):
        self.pieces = pieces

    @property
    def corner_pieces(self):
        return [piece for piece in self.pieces if piece.is_corner]

    @property
    def corner_codes(self):
        return [piece.code for piece in self.corner_pieces]

    def set_neighbors(self):
        for piece in self.pieces:
            piece.add_neighbors(piece.get_neighbors(self.pieces))

    def slice_piece(self, pieces, piece_code):
        return [p for p in pieces if p.code != piece_code]

    def solve(self):
        """Lol this is trash, but it's _functioning_ trash"""
        rows = []

        # Pull a corner piece
        current_piece = self.corner_pieces[0]

        # Track the remaining pieces
        remaining_corner_codes = set(self.corner_codes)
        remaining_corner_codes.remove(current_piece.code)

        # Get the remaining pieces?
        remaining_pieces = self.slice_piece(self.pieces, current_piece.code)

        current_row = []
        next_piece = current_piece.neighbors[0]

        placed_piece_codes = set()

        while True:
            # Find the piece in the currently moving direction
            # Get the matching side
            matching_sides = current_piece.get_matching_sides(next_piece)

            # Rotate current piece to correct orientation
            while current_piece.right not in matching_sides:
                current_piece.rotate_right()

            # Rotate next piece to correct orientation
            while next_piece.left not in matching_sides:
                next_piece.rotate_right()

            if current_piece.right != next_piece.left:
                next_piece.flip()

            # Add the piece to the row
            current_row.append(current_piece)
            placed_piece_codes.add(current_piece.code)

            # Get the next neighbor
            current_piece = next_piece
            next_piece = current_piece.get_neighbor_on_side(current_piece.right)

            if next_piece is None:
                current_row.append(current_piece)
                placed_piece_codes.add(current_piece.code)

                # Start next row
                # Get the remaining neighbor of the first piece in the row
                remaining_neighbors = [
                    piece for piece in current_row[0].neighbors
                    if piece.code not in placed_piece_codes
                ]

                # Break out if all pieces are in place
                if not remaining_neighbors:
                    rows.append(current_row)
                    break

                current_piece = remaining_neighbors[0]
                matching_sides = current_piece.get_matching_sides(current_row[0])

                # Position the first piece in next row correctly
                while current_piece.top not in matching_sides:
                    current_piece.rotate_right()

                # Flip the current row if needed (only first row)
                if current_row[0].bottom not in matching_sides:
                    for piece in current_row:
                        piece.flip()

                # Flip the first piece on the next row on y if needed
                if current_row[0].bottom != current_piece.top:
                    current_piece.flip_y()

                next_piece = current_piece.get_neighbor_on_side(current_piece.right)

                rows.append(current_row)
                current_row = []

        return rows


class PuzzleSearcher():
    def __init__(self, piece_rows):
        self.piece_rows = piece_rows
        self.rows = self.get_rows(piece_rows)

    def get_rows(self, piece_rows):
        size = len(piece_rows[0][0].sliced_rows[0])
        rows = [[] for _ in range(size * len(piece_rows))]

        for i, piece_row in enumerate(piece_rows):
            for j, piece in enumerate(piece_row):
                for k, row in enumerate(piece.sliced_rows):
                    rows[size*i+k] += row

        return rows

    def get_pattern_coords(self, pattern_rows):
        pattern_coords = []
        for y, row in enumerate(pattern_rows):
            for x, val in enumerate(row):
                if val == '#':
                    pattern_coords.append((x, y))
        return pattern_coords

    def check_coord_for_pattern(self, point, pattern_coords):
        for coord in pattern_coords:
            check_point = (point[0] + coord[0], point[1] + coord[1])
            if self.rows[check_point[1]][check_point[0]] != '#':
                return False
        return True

    def rotate_right(self):
        new_rows = [[] for r in self.rows]
        for row in self.rows[::-1]:
            for j, val in enumerate(row):
                new_rows[j].append(val)
        self.rows = new_rows

    def flip(self):
        self.rows = self.rows[::-1]

    def search_current_orientation_for(self, x_range, y_range, pattern_coords):
        matches = []
        for x in range(x_range):
            for y in range(y_range):
                if self.check_coord_for_pattern((x, y), pattern_coords):
                    matches.append((x, y))
        return matches


    def search_for(self, pattern_rows):
        pattern_coords = self.get_pattern_coords(pattern_rows)

        x_buff = len(pattern_rows[0])
        y_buff = len(pattern_rows)

        x_range = len(self.rows[0]) - x_buff
        y_range = len(self.rows) - y_buff

        # Try all orientations

        for _ in range(2):
            for _ in range(4):
                matches = self.search_current_orientation_for(
                    x_range,
                    y_range,
                    pattern_coords
                )
                if matches:
                    return matches
                self.rotate_right()

            self.flip()

        return matches

    def print(self):
        for row in self.rows:
            print(''.join(row))


def get_pieces():
    return [Piece(piece_raw[0], piece_raw[1]) for piece_raw in get_pieces_raw()]


def product(vals):
    product = 1
    for val in vals:
        product *= val
    return product


def get_hash_count(rows):
    return sum(sum([val == '#' for val in row]) for row in rows)


if __name__ == '__main__':
    puzzle = Puzzle(get_pieces())

    # Add the neighbors to the peices
    puzzle.set_neighbors()

    corner_codes_product = product([p.code for p in puzzle.corner_pieces])
    print(f'Part 1: {corner_codes_product}')

    solved_piece_rows = puzzle.solve()
    searcher = PuzzleSearcher(solved_piece_rows)

    search_pattern_rows = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ',
    ]

    # We did the match! The montster match!
    matches = searcher.search_for(search_pattern_rows)

    total_hashes = get_hash_count(searcher.rows)
    monster_hashes = get_hash_count(search_pattern_rows)
    water_roughness = total_hashes - monster_hashes * len(matches)

    print(f'Part 2: {water_roughness}')
