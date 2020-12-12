def get_input_directions():
    return [{
        'command': line[0],
        'value': int(line[1:]),
    } for line in open('input.txt').readlines()]

class Traveler():
    DIRECTIONS_TO_VECTOR = {
        'N': (0, +1),
        'E': (+1, 0),
        'S': (0, -1),
        'W': (-1, 0),
    }
    ANGLE_TO_DIRECTION = {
        0: 'N',
        90: 'E',
        180: 'S',
        270: 'W',
    }
    ANGLE_TO_TRANSPOSITION = {
        0: lambda x, y: (x, y),
        90: lambda x, y: (y, -x),
        180: lambda x, y: (-x, -y),
        270: lambda x, y: (-y, x)
    }

    def __init__(self, waypoint):
        self.position = (0, 0)
        self.angle = 90
        self.direction = self.ANGLE_TO_DIRECTION[self.angle]
        self.waypoint = waypoint

    def get_vector_by_distance(self, vector, distance):
        return (
            vector[0] * distance,
            vector[1] * distance
        )

    def turn(self, direction, angle_diff):
        diff = angle_diff if direction == 'R' else -angle_diff
        self.angle += diff

        if self.angle < 0:
            self.angle += 360

        self.angle = self.angle % 360

        self.direction = self.ANGLE_TO_DIRECTION[self.angle]

        return self.position

    def get_new_position(self, vector):
        return (
            self.position[0] + vector[0],
            self.position[1] + vector[1]
        )

    def get_new_waypoint(self, vector):
        return (
            self.waypoint[0] + vector[0],
            self.waypoint[1] + vector[1]
        )

    def move_by_vector(self, vector):
        self.position = self.get_new_position(vector)

    def move_waypoint(self, direction, value):
        self.waypoint = self.get_new_waypoint(
            self.get_vector_by_distance(
                self.DIRECTIONS_TO_VECTOR[direction],
                value
            )
        )

    def turn_waypoint(self, direction, value):
        # Model as a right rotation
        value = value if direction == 'R' else 360 - value

        # Get the transposition function
        transposition = self.ANGLE_TO_TRANSPOSITION[value]

        # Apply the transposition
        self.waypoint = transposition(self.waypoint[0], self.waypoint[1])

    def move(self, direction, value):
        self.position = self.get_new_position(
            self.get_vector_by_distance(
                self.DIRECTIONS_TO_VECTOR[direction],
                value
            )
        )

    def run_command(self, command, value):
        if command in ('L', 'R'):
            self.turn_waypoint(command, value)
        elif command == 'F':
            self.move_by_vector(
                self.get_vector_by_distance(self.waypoint, value)
            )
        else:
            self.move_waypoint(command, value)

    def get_manhattan_distance(self):
        return abs(self.position[0]) + abs(self.position[1])

    def print_vals(self):
        print(f'Position: {self.position}')
        print(f'Waypoint: {self.waypoint}')

if __name__ == '__main__':
    directions = get_input_directions()
    traveler = Traveler((10, 1))
    for direction in directions:
        print()
        traveler.run_command(direction['command'], direction['value'])
        traveler.print_vals()

    print(traveler.get_manhattan_distance())
