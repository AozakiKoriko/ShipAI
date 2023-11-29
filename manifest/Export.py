def format_grid_line(line, row_number):
    formatted_lines = []
    columns = line.split()
    
    for col_number, value in enumerate(columns, start=1):
        if value == '0':
            name = 'UNUSED'
 
        elif value == '-1':
            name = 'NAN'

        else:
            name = value
            # Placeholder for weight, update this with logic to determine weight
            # weight = '00000' 

        formatted_lines.append(f"[{row_number:02},{col_number:02}], {name}")

    return formatted_lines

def export_formatted_grid(grid):
    formatted_output = []
    current_row_number = 1
    for line in reversed(grid):  # Process the grid lines in reverse order
        formatted_line = format_grid_line(line, current_row_number)
        formatted_output.extend(formatted_line)
        current_row_number += 1  # Increment the row number after processing each line
    
    return '\n'.join(formatted_output)

# Example usage
grid_data = """
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
-1 Cat Dog Pig Hen Rat 0 0 0 0 0 -1
""".strip().split('\n')

formatted_output = export_formatted_grid(grid_data)
print(formatted_output)

