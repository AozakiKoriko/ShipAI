from manifest_import import parse_cargo_info
from manifest_import import Cargo

def fill_grid_with_cargos(cargos):
    grid = [[None for _ in range(12)] for _ in range(9)]

    for cargo in cargos:
        row, col = cargo.position
        """
        format of location: 
        location (x,y) which x means hight, y means column
        """
        if row < 0 or row >= 9 or col < 0 or col >= 12:
            print(f"Error: Position out of range for cargo {cargo.name} at ({row}, {col})")
            continue

        if cargo.isNan:
            grid[row][col] = -1
        elif not cargo.isUsed:
            grid[row][col] = 0
        else:
            grid[row][col] = cargo.name

    return grid



#print grid
#grid.reverse()
#for row in grid:
#    print(" ".join(str(item) if item is not None else "0" for item in row))


