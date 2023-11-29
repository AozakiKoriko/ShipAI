from read import parse_cargo_info

class Cargo:
    def __init__(self, position, weight, name):
        self.position = position
        self.weight = weight
        self.name = name
        self.isUsed = 0 if name == "UNUSED" else 1
        self.isNan = 1 if name == "NAN" else 0

def fill_grid_with_cargos(cargos):
    grid = [[None for _ in range(12)] for _ in range(8)]

    for cargo in cargos:
        row, col = cargo.position
        
        if row < 0 or row >= 8 or col < 0 or col >= 12:
            print(f"Error: Position out of range for cargo {cargo.name} at ({row}, {col})")
            continue

        if cargo.isNan:
            grid[row][col] = -1
        elif not cargo.isUsed:
            grid[row][col] = 0
        else:
            grid[row][col] = cargo.name

    return grid

# write cargo information to grid
cargos = parse_cargo_info("/Users/hanlinzha/Library/CloudStorage/OneDrive-Personal/CS 179M/ShipAI/ship_cases/ShipCase5.txt")
grid = fill_grid_with_cargos(cargos)

# print grid
grid.reverse()
for row in grid:
    print(" ".join(str(item) if item is not None else "0" for item in row))

