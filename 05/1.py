def get_boarding_passes():
    return [l.strip() for l in open('input.txt').readlines()]

def find_val(code, lower, upper, vals):
    if not code:
        return vals[0]

    index = int(len(vals) / 2)

    if code[0] == lower:
        return find_val(code[1:], lower, upper, vals[:index])

    return find_val(code[1:], lower, upper, vals[index:])

def get_bp_row(code):
    return find_val(code, lower='F', upper='B', vals=range(2**(len(code))))

def get_bp_col(code):
    return find_val(code, lower='L', upper='R', vals=range(2**(len(code))))

def get_seat_id(boarding_pass):
    row = get_bp_row(boarding_pass[:7])
    col = get_bp_col(boarding_pass[7:])
    return row * 8 + col

def get_seat_ids(boarding_passes):
    return [get_seat_id(boarding_pass) for boarding_pass in boarding_passes]

if __name__ == '__main__':
    boarding_passes = get_boarding_passes()
    seat_ids = get_seat_ids(boarding_passes)

    print(f'Part 1: {max(seat_ids)}')

    all_seat_ids = range(min(seat_ids), max(seat_ids))
    print(f'Part 2: {set(all_seat_ids).difference(seat_ids)}')
