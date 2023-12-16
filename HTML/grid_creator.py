from manifest_import import parse_cargo_info
from manifest_import import Cargo

def fill_grid_with_cargos(cargos):
    grid = [[None for _ in range(12)] for _ in range(8)]

    for cargo in cargos:
        row, col = cargo.position
        if row < 0 or row >= 8 or col < 0 or col >= 12:
            print(f"Error: Position out of range for cargo {cargo.name} at ({row}, {col})")
            continue

        adjusted_row = 7 - row

        if cargo.isNan:
            grid[adjusted_row][col] = -1
        elif not cargo.isUsed:
            grid[adjusted_row][col] = 0
        else:
            grid[adjusted_row][col] = cargo.name

    return grid

def create_grid_from_manifest(file_path):
    cargos = parse_cargo_info(file_path)
    return fill_grid_with_cargos(cargos)
