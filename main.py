import tkinter as tk
import datetime
import os
from tkinter import filedialog, messagebox
import json
import balance
from onload_offload_main import onload_offload_algorithm

username = None
json_data = None
step_info_label = None
step_details_label = None
target_list = []
onload_list = []
cargos_weight = []
file_path = ""


def save_progress(current_step, json_data, progress_file_path='progress.json'):
    progress = {
        'last_step': current_step,
        'data': json_data
    }
    with open(progress_file_path, 'w') as file:
        json.dump(progress, file)


def load_progress(progress_file_path='progress.json'):
    try:
        with open(progress_file_path, 'r') as file:
            progress = json.load(file)
            return progress['last_step'], progress['data']
    except FileNotFoundError:
        messagebox.showinfo("Error reading", "Progress file not found")
        return None, None


def on_load_progress_click(update_step_display):
    global current_step, json_data

    last_step, saved_data = load_progress()
    if last_step is not None and saved_data is not None:
        current_step = last_step - 1
        json_data = saved_data
        update_step_display()
    else:
        messagebox.showinfo("Load Progress", "No saved progress found or unable to read the file.")


# Function to read and parse JSON data
def read_json_data():
    try:
        with open('output.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("JSON Error", "JSON File Not Found")


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
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                display_load(lines)
                file_name = os.path.basename(file_path)  # Extracting only the file name
                save_to_log(f"Opened Manifest: {file_name}")  # Logging only the file name
        except FileNotFoundError:
            messagebox.showerror("File error", "File Not Found")


# Display load manifest
def display_load(lines):
    the_load_window = tk.Toplevel(root)
    the_load_window.title("Load/Offload")
    main_frame = tk.Frame(the_load_window)
    main_frame.pack(side=tk.RIGHT, padx=50, pady=50)
    root.withdraw()  # close main window

    # Frame for the content display area on the left
    left_frame = tk.Frame(the_load_window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Button to update the username
    update_username_button = tk.Button(left_frame, text="Hand Over", command=update_username)
    update_username_button.pack(side=tk.TOP, pady=5)

    # Button to go back to the main window
    back_button = tk.Button(left_frame, text="Load Done", width=12, height=3,
                            command=lambda: back_to_main(the_load_window))
    back_button.pack_forget()  # Hide the button initially

    cell_info_label = tk.Label(left_frame, text="", font=("Arial", 16))
    cell_info_label.pack()  # Adjust the positioning as needed within your layout

    # Function to update content display
    def update_content_display(content):
        # Update the label with the clicked cell content
        cell_info_label.config(text=f"Container Name is: {content}")
        log_offload = f"Container of {content} offload"
        save_to_log(log_offload)

    # Buttons for content display manipulation
    clear_button = tk.Button(left_frame, text="Clear", command=lambda: update_content_display(""))
    clear_button.pack(pady=5)

    buttons_dict = {}  # Dictionary to keep track of buttons

    # function to toggle cell color between light green and light blue
    def change_cell_color(event, btn, coords):
        current_color = btn.cget('bg')
        if current_color == 'light green':
            btn.config(bg='light blue')

            target_list.append(coords)


        elif current_color == 'light blue':
            btn.config(bg='light green')

    # Function to add a description and weight
    def add_description_and_weight():
        description = description_entry.get().strip()
        weight = weight_entry.get().strip()

        if validate_description(description) and validate_weight(weight):
            # Append the description and weight to their respective lists
            onload_list.append(description)
            cargos_weight.append(weight)

            # Clear the description and weight Entry fields
            description_entry.delete(0, tk.END)
            weight_entry.delete(0, tk.END)

            log_message = f"Container of description: {description}, weight: {weight} onload"
            save_to_log(log_message)

    def send_info_to_onload_offload_algorithm():
        global file_path
        if len(target_list) >= 1 or len(onload_list) >= 1 and len(cargos_weight) >= 1:
            onload_offload_algorithm(file_path, target_list, onload_list, cargos_weight)

            json_data = read_json_data()
            if json_data is None:
                messagebox.showerror("Error", "Failed to load JSON data.")
                return

            # Initialize step-related variables and labels
            current_step = 0
            step_info_label = tk.Label(left_frame, font=("Arial", 16))
            step_info_label.pack(pady=5)
            step_details_label = tk.Label(left_frame, font=("Arial", 18))
            step_details_label.pack(pady=5)

            def update_grid(target, dest):
                for coords, btn in buttons_dict.items():
                    if btn.cget('bg') in ['red', 'purple']:
                        btn.config(bg='SystemButtonFace' if btn.cget('state') != tk.DISABLED else 'SystemButtonFace',
                                   text="")

                if target:
                    target_coords = (target[0], target[1])
                    if target_coords in buttons_dict:
                        buttons_dict[target_coords].config(bg='red')

                if dest:
                    dest_coords = (dest[0], dest[1])
                    if dest_coords in buttons_dict:
                        buttons_dict[dest_coords].config(bg='purple')

            # Function to update the step display
            def update_step_display():
                nonlocal current_step
                total_steps = len(json_data["steps"])

                if current_step < total_steps:
                    step_data = json_data['steps'][current_step]
                    target = step_data.get('target')
                    dest = step_data.get('dest')

                    update_grid(target, dest)

                    target = "Truck" if target is None else str(target)
                    dest = "Truck" if dest is None else str(dest)
                    cost = step_data['cost']

                    step_info_label.config(text=f"Step {current_step + 1} of {total_steps}")
                    step_details_label.config(text=f"Start: {target} -> Dest: {dest} \n Current Time: {cost}")

                    current_step += 1
                else:
                    step_info_label.pack_forget()
                    step_details_label.pack_forget()
                    total_time_label.pack_forget()
                    next_button.pack_forget()
                    send_manifest = tk.Label(left_frame,
                                             text=f"Updated manifest \n has been generated", font=("Arial", 16))
                    send_manifest.pack(pady=5)
                    back_button.pack(side=tk.TOP, pady=5)
                    os.remove('output.json')

            update_step_display()

            # Displaying total time
            total_time = json_data["totalTime"]
            total_time_label = tk.Label(left_frame, text=f"Total Time: {total_time}", font=("Arial", 14))
            total_time_label.pack(pady=5)

            # Next button to update the step display
            next_button = tk.Button(left_frame, text="Next", command=update_step_display)
            next_button.pack(pady=5)
            return True


        else:
            messagebox.showerror("Validation Check",
                                 "Please input at least 1 container or 1 description with weight.")
            return False

    # Define a function to validate the description
    def validate_description(description):
        disallowed_exact_words = ["NAN", "UNUSED"]
        if description in disallowed_exact_words or not description:
            messagebox.showerror("Validation Check", "Invalid description.")
            return False
        return True

    # Define a function to validate the weight
    def validate_weight(weight):
        if weight.isdigit():
            weight_value = int(weight)
            if 0 <= weight_value <= 99999:
                return True
        messagebox.showerror("Validation Check", "Invalid weight. Enter a non-negative number")
        return False

    def on_button_click():
        # Disable the button
        send_info_button.config(state=tk.DISABLED)
        success = send_info_to_onload_offload_algorithm()
        if not success:
            send_info_button.config(state=tk.NORMAL)

    # Create Entry fields for Description and Weight
    description_label = tk.Label(the_load_window, text="Description:")
    description_label.pack(pady=5)
    description_entry = tk.Entry(the_load_window)
    description_entry.pack(pady=5)

    weight_label = tk.Label(the_load_window, text="Weight:")
    weight_label.pack(pady=5)
    weight_entry = tk.Entry(the_load_window)
    weight_entry.pack(pady=5)

    # Create buttons for adding Description and Weight, and sending all information
    add_info_button = tk.Button(the_load_window, text="Add Description & Weight", command=add_description_and_weight)
    add_info_button.pack(pady=5)

    send_info_button = tk.Button(the_load_window, text="Start", height=2, width=10,
                                 command=on_button_click)
    send_info_button.pack(pady=5)

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

    # Textbox for entering messages
    message_textbox = tk.Text(left_frame, height=4, width=40)
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

    # 8x12 grid display
    frame = tk.Frame(main_frame)
    frame.pack()

    grid_data = {}
    for line in lines:
        coords, _, label = line.strip().split(', ')
        x, y = map(int, coords.strip('[]').split(','))
        grid_data[(x, y)] = label  # Extract the label

    for i in range(8):  # 8 rows
        for j in range(12):  # 12 columns
            # Adjust coordinates to match the .txt file format
            adjusted_i = 8 - i
            adjusted_j = j + 1

            label_text = grid_data.get((adjusted_i, adjusted_j), "")
            coords = (adjusted_i, adjusted_j)

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
                btn.bind('<Button-1>', lambda event, button=btn, c=coords: change_cell_color(event, button, c))
            btn.grid(row=i, column=j)
            buttons_dict[(adjusted_i, adjusted_j)] = btn  # Store buttons in dictionary

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
    global file_path
    save_to_log("Need to balance")
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        if balance.run(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                display_balance(lines)
                file_name = os.path.basename(file_path)  # Extracting only the file name
                save_to_log(f"Opened Manifest: {file_name}")  # Logging only the file name


        else:
            messagebox.showwarning("Balance", "Already Balanced")


# Display balance manifest
def display_balance(lines):
    global json_data, current_step, step_info_label, step_details_label
    the_balance_window = tk.Toplevel(root)
    the_balance_window.title("Balance")
    main_frame = tk.Frame(the_balance_window)
    main_frame.pack(side=tk.RIGHT, padx=50, pady=50)
    root.withdraw()  # close balance window

    load_progress_button = tk.Button(the_balance_window, text="Load Progress",
                                     command=lambda: on_load_progress_click(update_step_display))
    load_progress_button.pack(pady=5)

    # Frame for the content display area on the left
    left_frame = tk.Frame(the_balance_window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Button to update the username
    update_username_button = tk.Button(left_frame, text="Hand over", command=update_username)
    update_username_button.pack(pady=5)

    # Button to go back to the main window
    back_button = tk.Button(left_frame, text="Balance Done", width=12, height=3,
                            command=lambda: back_to_main(the_balance_window))
    back_button.pack_forget()  # Hide the button initially

    current_step = 1
    json_data = read_json_data()

    # Initialize labels for displaying current step and details
    step_info_label = tk.Label(left_frame, font=("Arial", 16))
    step_info_label.pack(pady=5)
    step_details_label = tk.Label(left_frame, font=("Arial", 18))
    step_details_label.pack(pady=5)

    # Set the labels with the first step's data
    first_step_data = json_data['steps'][0]
    first_start_coords = tuple(map(int, first_step_data['start']))
    first_dest_coords = tuple(map(int, first_step_data['dest']))
    first_step_time = first_step_data['time']

    step_info_label.config(text=f"Step 1 of {len(json_data['steps'])}")
    step_details_label.config(
        text=f"Start: {first_start_coords} -> Dest: {first_dest_coords} \n Current time: {first_step_time}")

    def update_step_display():
        global current_step
        total_steps = len(json_data["steps"])
        save_progress(current_step, json_data)

        if current_step < total_steps:
            current_step += 1
        else:
            step_info_label.pack_forget()
            step_details_label.pack_forget()
            total_time_label.pack_forget()
            next_button.pack_forget()
            send_manifest = tk.Label(left_frame,
                                     text=f"Updated manifest \n has been generated", font=("Arial", 16))
            send_manifest.pack(pady=5)
            back_button.pack(side=tk.TOP, pady=5)
            os.remove('output.json')

        step_data = json_data['steps'][current_step - 1]
        start_coords = tuple(map(int, step_data['start']))
        dest_coords = tuple(map(int, step_data['dest']))
        step_time = step_data['time']  # Extract time for the current step

        update_grid(start_coords, dest_coords)

        step_info_label.config(text=f"Step {current_step} of {total_steps}")
        step_details_label.config(text=f"Start: {start_coords} -> Dest: {dest_coords} \n Current time: {step_time}")

    # Displaying total time
    total_time = json_data["totalTime"]
    total_time_label = tk.Label(left_frame, text=f"Total Time: {total_time}", font=("Arial", 14))
    total_time_label.pack(pady=5)

    # Next button to update the step display
    next_button = tk.Button(left_frame, text="Next", command=update_step_display)
    next_button.pack(pady=5)

    buttons_dict = {}  # Dictionary to keep track of buttons

    # Textbox for entering messages
    message_textbox = tk.Text(left_frame, height=4, width=55)
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

    # 8x12 grid display
    frame = tk.Frame(main_frame)
    frame.pack()

    # Parsing the .txt file data
    grid_data = {}
    for line in lines:
        coords, _, label = line.strip().split(', ')
        x, y = map(int, coords.strip('[]').split(','))
        grid_data[(x, y)] = label

    # Generating the grid
    for i in range(8):  # 8 rows
        for j in range(12):  # 12 columns
            # Adjust coordinates to match the .txt file format
            adjusted_i = 8 - i
            adjusted_j = j + 1

            label_text = grid_data.get((adjusted_i, adjusted_j), "")

            # Creating buttons with labels from .txt file
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
            buttons_dict[(adjusted_i, adjusted_j)] = btn

    def update_grid(start_coords, dest_coords):
        for coords, btn in buttons_dict.items():
            if btn.cget('bg') in ['red', 'purple']:
                btn.config(bg='light green' if btn.cget('state') != tk.DISABLED else 'SystemButtonFace', text="")

        # Highlight only the Start and Dest in the grid
        if start_coords in buttons_dict:
            buttons_dict[start_coords].config(bg='red')
        if dest_coords in buttons_dict:
            buttons_dict[dest_coords].config(bg='purple')

    start_coords = tuple(map(int, json_data['steps'][0]['start']))
    dest_coords = tuple(map(int, json_data['steps'][0]['dest']))
    update_grid(start_coords, dest_coords)

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
        save_progress(current_step, json_data)
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
        username = user
        login_window.destroy()  # Close the login window
        root.deiconify()  # Show the main window
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
main_login_button = tk.Button(root, text="Sign in", command=login, width=10, height=2)
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
