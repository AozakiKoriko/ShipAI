class Cargo:
    def __init__(self, position, weight, name):
        self.position = position
        self.weight = weight
        self.name = name

def parse_cargo_info(file_path):
    cargos = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            position = tuple(map(int, parts[0][1:-1].split(',')))
            weight = int(parts[1][1:-1])
            name = parts[2]

            if name not in ["NAN", "UNUSED"]:
                cargos.append(Cargo(position, weight, name))

    return cargos

def find_cargo_by_position(cargos, position):
    for cargo in cargos:
        if cargo.position == position:
            return cargo
    return None

# read
cargo_list = parse_cargo_info("/Users/hanlinzha/Library/CloudStorage/OneDrive-Personal/CS 179M/ShipAI/ShipCase1.txt")

# test
while 1:
    # input
    user_input = input("Enter a position (x,y): ")
    if user_input.lower() == 'q':
        break
    
    try:
        x, y = map(int, user_input.split(','))

        # output
        cargo = find_cargo_by_position(cargo_list, (x, y))
        if cargo:
            print(f"Cargo at position {cargo.position}: Name - {cargo.name}, Weight - {cargo.weight}")
        else:
            print("No cargo found at the given position.")
    except ValueError:
        print("Invalid input. Please enter a position in the format 'x,y'.")
