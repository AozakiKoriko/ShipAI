import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

# Get the path to the desktop directory
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
log_file_path = os.path.join(desktop_path, 'log.txt')


# Function to save message to log file
def save_to_log(message):
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")


def back_to_main(current_window):
    current_window.destroy()
    root.deiconify()


username = None


def update_username():
    global greeting_label, username

    # Function to handle updating the username
    def set_new_username():
        new_username = username_entry.get()
        if new_username:
            username = new_username
            greeting_label.config(text=f"On duty: {username}")
            popup_window.destroy()

    # Create a pop-up window for entering a new username
    popup_window = tk.Toplevel()
    popup_window.title("Update Username")
    popup_window.geometry("300x150")
    popup_window.resizable(False, False)

    username_label = tk.Label(popup_window, text="Enter new username:")
    username_label.pack(pady=10)

    username_entry = tk.Entry(popup_window)
    username_entry.pack(pady=5)

    update_button = tk.Button(popup_window, text="Update", command=set_new_username)
    update_button.pack(pady=10)


# Read load manifest
def load_window():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                display_load(lines)
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("An error occurred:", e)


# Display load manifest
def display_load(lines):
    global username, greeting_label
    the_load_window = tk.Toplevel(root)
    the_load_window.title("Load/Offload")
    main_frame = tk.Frame(the_load_window)
    main_frame.pack(side=tk.RIGHT, padx=50, pady=50)
    root.withdraw()  # close main window

    # Greeting label with the username
    greeting_label = tk.Label(the_load_window, text=f"On duty: {username}", font=("Arial", 16))
    greeting_label.pack(pady=10)

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
    update_username_button = tk.Button(left_frame, text="Update Username", command=update_username)
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

    # 8x12 grid display
    frame = tk.Frame(main_frame)
    frame.pack()

    buttons_dict = {}  # Dictionary to keep track of buttons
    blinking_buttons = {}  # Dictionary to track blinking buttons

    def blink(button):
        if button.winfo_exists():
            current_color = button.cget('bg')
            new_color = 'red' if current_color == 'light blue' else 'light blue'
            button.config(bg=new_color)
            blinking_buttons[button] = root.after(500, lambda b=button: blink(b))

    # Function to turn all light blue cells to red and start blinking
    def start_blinking():
        for button in buttons_dict.values():
            if button.cget('bg') == 'light blue':
                button.config(bg='red')
                blinking_buttons[button] = root.after(500, lambda b=button: blink(b))

    # New function to change cell color from green to red and vice versa
    def change_cell_color(btn):
        if btn.cget('bg') == 'light green':
            btn.config(bg='light blue')
        elif btn.cget('bg') == 'light blue':
            btn.config(bg='light green')

            # Stop blinking if the cell becomes light green again
            if btn in blinking_buttons:
                root.after_cancel(blinking_buttons[btn])
                del blinking_buttons[btn]

    # Button to turn all light blue cells to red and start blinking
    start_blinking_button = tk.Button(left_frame, text="Start Blinking", command=start_blinking)
    start_blinking_button.pack(pady=5)

    # Textbox for entering messages
    message_textbox = tk.Text(left_frame, height=10, width=40)
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
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                display_balance(lines)
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("An error occurred:", e)


# Display balance manifest
def display_balance(lines):
    global username, greeting_label
    the_balance_window = tk.Toplevel(root)
    the_balance_window.title("Balance")
    main_frame = tk.Frame(the_balance_window)
    main_frame.pack(side=tk.RIGHT, padx=50, pady=50)
    root.withdraw()  # close balance window

    # Greeting label with the username
    greeting_label = tk.Label(the_balance_window, text=f"On duty: {username}", font=("Arial", 16))
    greeting_label.pack(pady=10)

    # Frame for the content display area on the left
    left_frame = tk.Frame(the_balance_window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Button to update the username
    update_username_button = tk.Button(left_frame, text="Update Username", command=update_username)
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
    blinking_buttons = {}  # Dictionary to track blinking buttons

    def blink(button):
        if button.winfo_exists():
            current_color = button.cget('bg')
            new_color = 'red' if current_color == 'light blue' else 'light blue'
            button.config(bg=new_color)
            blinking_buttons[button] = root.after(500, lambda b=button: blink(b))

    # Function to turn all light blue cells to red and start blinking
    def start_blinking():
        for button in buttons_dict.values():
            if button.cget('bg') == 'light blue':
                button.config(bg='red')
                blinking_buttons[button] = root.after(500, lambda b=button: blink(b))

    # New function to change cell color from green to red and vice versa
    def change_cell_color(btn):
        if btn.cget('bg') == 'light green':
            btn.config(bg='light blue')
        elif btn.cget('bg') == 'light blue':
            btn.config(bg='light green')

            # Stop blinking if the cell becomes light green again
            if btn in blinking_buttons:
                root.after_cancel(blinking_buttons[btn])
                del blinking_buttons[btn]

    # Button to turn all light blue cells to red and start blinking
    start_blinking_button = tk.Button(left_frame, text="Start Blinking", command=start_blinking)
    start_blinking_button.pack(pady=5)

    # Textbox for entering messages
    message_textbox = tk.Text(left_frame, height=10, width=40)
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
        the_balance_window.destroy()
        root.deiconify()

    the_balance_window.protocol("WM_DELETE_WINDOW", on_closing)


# Login function
def login():
    global username, login_window, root
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_frame = tk.Frame(login_window)
    login_frame.pack(padx=100, pady=80)

    # Username label and entry
    username_label = tk.Label(login_frame, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    # Login button
    login_button = tk.Button(login_frame, text="Login", command=lambda: check_login(username_entry.get()))
    login_button.pack()


# Check login credentials
def check_login(user):
    global username
    if user:  # Check if the username is not empty
        username = user  # Set the global username variable
        login_window.destroy()  # Close the login window
        root.deiconify()  # Show the main window with greeting
        main_window_greeting(username)
    else:
        tk.messagebox.showerror("Error", "Please enter a username.")


# Main window with greeting
def main_window_greeting(username):
    global root
    greeting_label = tk.Label(root, text="Hello, " + username, font=("Arial", 18))
    greeting_label.pack(pady=50)


# Main window
root = tk.Tk()
root.title("ShipsAI")
root.geometry("650x450")

# Hide the main window initially, Show login window
root.withdraw()
login()

# Load/offload button
load_button = tk.Button(root, text="Load/Offload", command=load_window, width=18, height=2)
load_button.pack(padx=30, pady=90)

# Balance button
balance_button = tk.Button(root, text="Balance", command=balance_window, width=18, height=2)
balance_button.pack(padx=30, pady=5)

# Run the tkinter main loop
root.mainloop()
