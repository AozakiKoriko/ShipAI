import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Get the path to the desktop directory
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
log_file_path = os.path.join(desktop_path, 'log.txt')


# Function to save message to log file
def save_to_log(action):
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    log_message = f"{timestamp} - {action}\n"
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)


def back_to_main(current_window):
    current_window.destroy()
    root.deiconify()
    save_to_log("Finished a Cycle.")


username = None


def update_username():
    global username

    # Function to handle updating the username
    def set_new_username():
        new_username = username_entry.get()

        if new_username:
            username = new_username
            popup_window.destroy()
            save_to_log(f"{username} signs in")

    # Create a pop-up window for entering a new username
    popup_window = tk.Toplevel()
    popup_window.title("Hand Over")
    popup_window.geometry("300x150")
    popup_window.resizable(False, False)

    username_label = tk.Label(popup_window, text="Enter username:")
    username_label.pack(pady=10)

    username_entry = tk.Entry(popup_window)
    username_entry.pack(pady=5)

    update_button = tk.Button(popup_window, text="signs in", command=set_new_username)
    update_button.pack(pady=10)


# Read load manifest
def load_window():
    save_to_log("Need to Load/Offload")
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                display_load(lines)
                file_name = os.path.basename(file_path)  # Extracting only the file name
                save_to_log(f"Opened Manifest: {file_name}")  # Logging only the file name
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("An error occurred:", e)


# Display load manifest
def display_load(lines):
    the_load_window = tk.Toplevel(root)
    the_load_window.title("Load/Offload")
    main_frame = tk.Frame(the_load_window)
    main_frame.pack(side=tk.RIGHT, padx=50, pady=50)
    root.withdraw()  # close main window

    # Create a frame for the 1x1 grid trunk
    truck_grid_frame = tk.Frame(main_frame)
    truck_grid_frame.pack(side=tk.LEFT)

    # Create a button for the 1x1 grid cell
    truck_btn = tk.Button(truck_grid_frame, text="", borderwidth=2, relief="solid", width=8, height=2,
                          state=tk.DISABLED)
    truck_btn.pack()

    # Frame for the content display area on the left
    left_frame = tk.Frame(the_load_window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Button to update the username
    update_username_button = tk.Button(left_frame, text="Hand Over", command=update_username)
    update_username_button.pack(pady=5)

    # Button to go back to the main window
    back_button = tk.Button(left_frame, text="Load Done", width=12, height=3,
                            command=lambda: back_to_main(the_load_window))
    back_button.pack(side=tk.TOP, pady=5)

    cell_info_label = tk.Label(left_frame, text="", font=("Arial", 16))
    cell_info_label.pack()  # Adjust the positioning as needed within your layout

    # Function to update content display
    def update_content_display(content):
        # Update the label with the clicked cell content
        cell_info_label.config(text=f"Container Name is: {content}")

    # Buttons for content display manipulation
    clear_button = tk.Button(left_frame, text="Clear", command=lambda: update_content_display(""))
    clear_button.pack(pady=5)

    def confirm_description():
        description = description_entry.get().strip()  # Strip leading/trailing whitespace
        disallowed_exact_words = ["?nan?", "?unused?", "nan"]

        if description.lower() in disallowed_exact_words or not description:
            messagebox.showerror("Description Check",
                                 "Invalid description.")
        else:
            messagebox.showinfo("Description Check", "Valid description.")

    def confirm_weight():
        weight = weight_entry.get()
        if weight.isdigit():
            weight_value = int(weight)
            if 1 <= weight_value <= 99999:
                messagebox.showinfo("Weight Check", "Valid weight.")
            else:
                messagebox.showerror("Weight Check", "Invalid weight. Enter a positive integer between 20 and 99999.")
        else:
            messagebox.showerror("Weight Check", "Invalid weight. Please enter an integer.")

    # Label and Entry for Description
    description_label = tk.Label(the_load_window, text="Description:")
    description_label.pack(pady=5)
    description_entry = tk.Entry(the_load_window)
    description_entry.pack(pady=5)

    # Button for confirming Description
    confirm_description_button = tk.Button(the_load_window, text="Confirm Description", command=confirm_description)
    confirm_description_button.pack(pady=5)

    # Label and Entry for Weight
    weight_label = tk.Label(the_load_window, text="Weight:")
    weight_label.pack(pady=5)
    weight_entry = tk.Entry(the_load_window)
    weight_entry.pack(pady=5)

    # Button for confirming Weight
    confirm_weight_button = tk.Button(the_load_window, text="Confirm Weight", command=confirm_weight)
    confirm_weight_button.pack(pady=5)

    # disable copy and paste
    def disable_event(event):
        return "break"

    description_entry.bind("<Control-c>", disable_event)
    description_entry.bind("<Control-x>", disable_event)
    description_entry.bind("<Control-v>", disable_event)

    weight_entry.bind("<Control-c>", disable_event)
    weight_entry.bind("<Control-x>", disable_event)
    weight_entry.bind("<Control-v>", disable_event)

    description_entry.bind("<Button-3>", disable_event)
    weight_entry.bind("<Button-3>", disable_event)

    # 8x12 grid display
    frame = tk.Frame(main_frame)
    frame.pack()

    buttons_dict = {}  # Dictionary to keep track of buttons

    # function to toggle cell color between light green and light blue
    def change_cell_color(btn):
        current_color = btn.cget('bg')
        if current_color == 'light green':
            btn.config(bg='light blue')
        elif current_color == 'light blue':
            btn.config(bg='light green')

    # Function to turn all light blue cells to red
    def turn_blue_to_red():
        for btn in buttons_dict.values():
            if btn.cget('bg') == 'light blue':
                btn.config(bg='red')

    # Function to reset all red cells to green
    def reset_red_to_green():
        for btn in buttons_dict.values():
            if btn.cget('bg') == 'red':
                btn.config(bg='light green')

    # Button to turn all light blue cells to red
    blue_to_red_button = tk.Button(left_frame, text="Blue to Red", command=turn_blue_to_red)
    blue_to_red_button.pack(pady=5)

    # Button to reset all red cells to green
    red_to_green_button = tk.Button(left_frame, text="Reset Red to Green", command=reset_red_to_green)
    red_to_green_button.pack(pady=5)

    # Textbox for entering messages
    message_textbox = tk.Text(left_frame, height=3, width=40)
    message_textbox.pack()

    # Function to clear the message textbox
    def clear_textbox():
        message_textbox.delete("1.0", tk.END)

    # Function to handle submission of the message
    def submit_message():
        message = message_textbox.get("1.0", tk.END).strip()
        if message:
            save_to_log(message)
            messagebox.showinfo("Message Saved", "Message saved to log file")
            clear_textbox()  # Clear the textbox after submitting the message
        else:
            messagebox.showwarning("Empty Message", "Please enter a message to submit")

    # Button to submit the message
    submit_button = tk.Button(left_frame, text="Submit", command=submit_message)
    submit_button.pack(pady=5)

    for i in range(7, -1, -1):
        for j in range(12):
            data = lines[(7 - i) * 12 + j].strip().split(', ')
            label_text = data[2]

            # Create buttons for each cell and attach a function to their click event
            if label_text == "NAN":
                btn = tk.Button(frame, text="", borderwidth=1, relief="solid", width=8, height=2,
                                bg="grey", state=tk.DISABLED)
            elif label_text == "UNUSED":
                btn = tk.Button(frame, text="", borderwidth=1, relief="solid", width=8, height=2,
                                state=tk.DISABLED)
            else:
                btn = tk.Button(frame, text=label_text, borderwidth=1, relief="solid", width=8, height=2,
                                bg="light green", command=lambda b=label_text: update_content_display(b))
                btn.bind('<Button-1>', lambda event, button=btn: change_cell_color(button))  # Bind left click event
            btn.grid(row=i, column=j)
            buttons_dict[(i, j)] = btn  # Store buttons in dictionary

    # Create the 4x24 grid for buffer
    buffer_grid_frame = tk.Frame(main_frame)
    buffer_grid_frame.pack()

    for i in range(4):
        for j in range(24):
            # Create buttons or widgets for the new grid and place them in buffer_grid_frame
            btn = tk.Button(buffer_grid_frame, borderwidth=2, text="", width=6, height=2, state=tk.DISABLED)
            btn.grid(row=i, column=j)

    buffer_grid_frame.pack()

    def on_closing():
        the_load_window.destroy()
        root.deiconify()

    the_load_window.protocol("WM_DELETE_WINDOW", on_closing)


# Read balance manifest
def balance_window():
    save_to_log("Need to balance")
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                display_balance(lines)
                file_name = os.path.basename(file_path)  # Extracting only the file name
                save_to_log(f"Opened Manifest: {file_name}")  # Logging only the file name
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("An error occurred:", e)


# Display balance manifest
def display_balance(lines):
    the_balance_window = tk.Toplevel(root)
    the_balance_window.title("Balance")
    main_frame = tk.Frame(the_balance_window)
    main_frame.pack(side=tk.RIGHT, padx=50, pady=50)
    root.withdraw()  # close balance window

    # Frame for the content display area on the left
    left_frame = tk.Frame(the_balance_window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Button to update the username
    update_username_button = tk.Button(left_frame, text="Hand over", command=update_username)
    update_username_button.pack(pady=5)

    # Button to go back to the main window
    back_button = tk.Button(left_frame, text="Balance Done", width=12, height=3,
                            command=lambda: back_to_main(the_balance_window))
    back_button.pack(side=tk.TOP, pady=5)

    cell_info_label = tk.Label(left_frame, text="", font=("Arial", 16))
    cell_info_label.pack()  # Adjust the positioning as needed within your layout

    # Function to update content display
    def update_content_display(content):
        # Update the label with the clicked cell content
        cell_info_label.config(text=f"Container Name is: {content}")

    # Buttons for content display manipulation
    clear_button = tk.Button(left_frame, text="Clear", command=lambda: update_content_display(""))
    clear_button.pack(pady=5)

    # 8x12 grid display
    frame = tk.Frame(main_frame)
    frame.pack()

    buttons_dict = {}  # Dictionary to keep track of buttons

    def is_symmetrical(grid_data):
        rows = len(grid_data)
        cols = len(grid_data[0]) if rows > 0 else 0
        mid_col = cols // 2

        for i in range(rows):
            for j in range(mid_col):
                if grid_data[i][j] != grid_data[i][cols - 1 - j]:
                    return False
        return True

    def check_symmetry():
        grid_data = [[buttons_dict[(i, j)].cget('text') for j in range(12)] for i in range(8)]
        if not is_symmetrical(grid_data):
            print("These cells aren't symmetrical")
            messagebox.showwarning("Symmetry Check", "These cells aren't symmetrical")
        else:
            print("The grid is symmetrical")
            messagebox.showinfo("Symmetry Check", "The grid is symmetrical")

    # Add a button to trigger the symmetry check
    symmetry_check_button = tk.Button(left_frame, text="Check Symmetry", command=check_symmetry)
    symmetry_check_button.pack(pady=5)

    # Textbox for entering messages
    message_textbox = tk.Text(left_frame, height=3, width=40)
    message_textbox.pack(pady=10)

    # Function to clear the message textbox
    def clear_textbox():
        message_textbox.delete("1.0", tk.END)

    # Function to handle submission of the message
    def submit_message():
        message = message_textbox.get("1.0", tk.END).strip()
        if message:
            save_to_log(message)
            messagebox.showinfo("Message Saved", "Message saved to log file")
            clear_textbox()  # Clear the textbox after submitting the message
        else:
            messagebox.showwarning("Empty Message", "Please enter a message to submit")

    # Button to submit the message
    submit_button = tk.Button(left_frame, text="Submit", command=submit_message)
    submit_button.pack(pady=5)

    for i in range(7, -1, -1):
        for j in range(12):
            data = lines[(7 - i) * 12 + j].strip().split(', ')
            label_text = data[2]
            # Create buttons for each cell and attach a function to their click event
            if label_text == "NAN":
                btn = tk.Button(frame, text="", borderwidth=1, relief="solid", width=8, height=2,
                                bg="grey", state=tk.DISABLED)
            elif label_text == "UNUSED":
                btn = tk.Button(frame, text="", borderwidth=1, relief="solid", width=8, height=2,
                                state=tk.DISABLED)
            else:
                btn = tk.Button(frame, text=label_text, borderwidth=1, relief="solid", width=8, height=2,
                                bg="light green", state=tk.DISABLED)
            btn.grid(row=i, column=j)
            buttons_dict[(i, j)] = btn  # Store buttons in dictionary

    # Create the 4x24 grid for buffer
    buffer_grid_frame = tk.Frame(main_frame)
    buffer_grid_frame.pack()

    for i in range(4):
        for j in range(24):
            # Create buttons or widgets for the new grid and place them in buffer_grid_frame
            btn = tk.Button(buffer_grid_frame, borderwidth=2, text="", width=6, height=2, state=tk.DISABLED)
            btn.grid(row=i, column=j)

    buffer_grid_frame.pack()

    def on_closing():
        the_balance_window.destroy()
        root.deiconify()

    the_balance_window.protocol("WM_DELETE_WINDOW", on_closing)


# Login function
def login():
    global username, login_window, root
    login_window = tk.Toplevel()
    login_window.title("Sign in")
    login_frame = tk.Frame(login_window)
    login_frame.pack(padx=100, pady=80)

    # Username label and entry
    username_label = tk.Label(login_frame, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    # Login button
    login_button = tk.Button(login_frame, text="Sign in", command=lambda: check_login(username_entry.get()))
    login_button.pack()


# Check login credentials
def check_login(user):
    global username
    if user:  # Check if the username is not empty
        username = user  # Set the global username variable
        login_window.destroy()  # Close the login window
        root.deiconify()  # Show the main window without the greeting
        save_to_log(f"{username} signs in")
    else:
        tk.messagebox.showerror("Error", "Please enter a username.")


# Main window
root = tk.Tk()
root.title("ShipsAI")
root.geometry("650x450")

# show main window first
root.deiconify()

# Add a new button to open the login window
main_login_button = tk.Button(root, text="Sign in", command=login, width=9, height=1)
main_login_button.pack(padx=30, pady=5)

# Greeting label
greeting_label = tk.Label(root, text="Welcome to ShipsAI", font=("Arial", 24))
greeting_label.pack(pady=10)

# Load/offload button
load_button = tk.Button(root, text="Load/Offload", command=load_window, width=18, height=2)
load_button.pack(padx=30, pady=90)

# Balance button
balance_button = tk.Button(root, text="Balance", command=balance_window, width=18, height=2)
balance_button.pack(padx=30, pady=5)

# Run the tkinter main loop
root.mainloop()
