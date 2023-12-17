import tkinter as tk
from tkinter import filedialog
import json
import balance
import os
import tkinter.messagebox
import onload_offload_main
import re
import datetime

def check_string(s):
    if s.strip() == '':
        return False
    if len(s) > 256:
        return False
    pattern = r'^[\W_]*(NAN|UNUSED)[\W_]*$'
    return re.match(pattern, s) is None

def check_weight(s):
    try:
        int(s)
        if 0 <= int(s) <= 99999:
            return True
        else:
            return False
    except ValueError:
        return False


def format_datetime(time):
    compare_list = {1: 'st', 2: 'nd', 3: 'rd'}

    day = time.day
    if day == 1 or day == 21 or day == 31:
        digit = 1
    elif day == 2 or day == 22:
        digit = 2
    elif day == 2 or day == 23:
        digit = 3
    else:
        digit = 0
    suffix = compare_list.get(digit, 'th')

    formatted_date = time.strftime(f"%B {day}{suffix} %Y: %H:%M")
    return formatted_date


def save_to_log(action):
    timestamp = format_datetime(datetime.datetime.now())
    log_message = f"{timestamp}  {action}\n"
    if not os.path.exists(".hidden_folder"):
        os.makedirs(".hidden_folder")
    with open('.hidden_folder/event.log', 'a') as file:
        file.write(log_message)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.recover_button = tk.Button(self, text="Recover Steps", command=self.recover)
        self.recover_button.pack(anchor="nw")
        # Username entry and submit button
        self.name_entry = tk.Entry(self)
        self.submit_button = tk.Button(self, text="Submit", command=self.save_user_name)
        self.submit_button.pack(side="bottom", anchor="sw")
        self.name_entry.pack(side="bottom", anchor="sw")
        self.info_label = tk.Label(self, text="Login:")
        self.info_label.pack(side="bottom", anchor="sw")

        # Software name label
        self.software_name_label = tk.Label(self, text="ShipAI", font=("Arial", 20))
        self.software_name_label.pack(pady=20)

        # Load/Offload and Balancing buttons
        self.load_offload_button = tk.Button(self, text="Load/Offload", command=self.open_load_page)
        self.load_offload_button.pack()
        self.balancing_button = tk.Button(self, text="Balancing", command=self.open_balance_page)
        self.balancing_button.pack()

    def recover(self):
        load_file_path = 'output.json'
        balance_file_path = 'output_balance.json'
        if os.path.exists(load_file_path):
            with open(load_file_path, 'r') as file:
                data = json.load(file)
            prev_step = data['currentSteps']
            if not prev_step:
                prev_step = 0
            else:
                prev_step = prev_step-1
            loadresultpage = self.controller.frames[LoadResultPage]
            loadresultpage.initialize_ui(prev_step)
            self.controller.show_frame(LoadResultPage)
        elif os.path.exists(balance_file_path):
            with open(balance_file_path, 'r') as file:
                data = json.load(file)
            prev_step = data['currentSteps']
            if not prev_step:
                prev_step = 0
            else:
                prev_step = prev_step-1
            balancepage = self.controller.frames[BalancePage]
            balancepage.initialize_ui(prev_step)
            self.controller.show_frame(BalancePage)
        else:
            tk.messagebox.showinfo("Error", "No recover steps found.")
    def save_user_name(self):
        user_name = self.name_entry.get()
        save_to_log(f"{user_name} signs in")
        self.name_entry.delete(0, 'end')
        msg = f"Welcome, {user_name}.\n"
        tk.messagebox.showinfo("Message", msg)

    def open_balance_page(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.controller.manifest_file_path = file_path
            balance_page = self.controller.frames[BalancePage]
            balance_page.load_data_and_initialize_ui()
            self.controller.show_frame(BalancePage)
            save_to_log(f"Manifest {file_path} is opened")


    def open_load_page(self):
        file_path = filedialog.askopenfilename()
        self.controller.manifest_file_path = file_path
        if file_path:
            loadoffload_page = self.controller.frames[LoadOffloadPage]
            loadoffload_page.update_file_path(file_path)
            self.controller.show_frame(LoadOffloadPage)



class LoadOffloadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_step_index = 0
        self.output_json = None
        self.manifest_file_path = self.controller.manifest_file_path
        self.contain = {}
        self.offload = []
        self.load_name_list = []
        self.load_weight_list = []
        self.container_data = {}
        self.selected_row = -1
        self.selected_column = -1
        self.default_bg = None
        self.selected_container_label = tk.Label(self, text="Selected Container: None")
        self.selected_container_label.grid(row=0, column=0, sticky="w")
        self.selected_container_label.grid_propagate(False)
        self.add_button = tk.Button(self, text="Add", command=self.add_container)
        self.add_button.grid(row=1, column=0, sticky='w')
        self.add_button.grid_propagate(False)
        self.load_name = tk.Label(self, text="Load container name: ")
        self.load_name.grid(row=3, column=0, sticky='w')
        self.loadname_entry = tk.Entry(self)
        self.loadname_entry.grid(row=3, column=1, padx=(0, 25), pady=4, sticky='w')
        self.load_weight = tk.Label(self, text="Load container weight: ")
        self.load_weight.grid(row=4, column=0, sticky='w')
        self.loadweight_entry = tk.Entry(self)
        self.loadweight_entry.grid(row=4, column=1, padx=(0, 25), pady=4, sticky='w')
        self.onload_button = tk.Button(self, text="Add", command=self.load_add)
        self.onload_button.grid(row=5, column=0, sticky='w')
        self.matrix_frames = [[tk.Button(self, width=2, height=2, borderwidth=1, relief="solid") for _ in range(12)]
                              for _ in range(8)]
        for i in range(len(self.matrix_frames) - 1, -1, -1):
            for j in range(len(self.matrix_frames[i])):
                self.matrix_frames[i][j].grid(row=8 - i, column=j + 200)
                self.matrix_frames[i][j].grid_propagate(False)
                self.default_bg = self.matrix_frames[i][j].cget('bg')

        self.done_button = tk.Button(self, text="Done Adding Info", command=self.done_select)
        self.done_button.grid(row=6, column=1, columnspan=12)
        self.add_button.grid_propagate(False)
        self.submit_button = tk.Button(self, text="Submit", command=self.save_user_name)
        self.submit_button.grid(row=42, column=0,sticky='w')
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=41, column=0, sticky='w')
        self.info_label = tk.Label(self, text="Login:")
        self.info_label.grid(row=40, column=0,sticky='w', pady=(25, 0))
        self.msg_label = tk.Label(self, text="Message :")
        self.msg_label.grid(row=31, column=0, sticky='w')
        self.message_textbox = tk.Text(self, height=4, width=40)
        self.message_textbox.grid(row=32, column=0)
        self.message_button = tk.Button(self, text="Add to log", command=self.msg_to_log)
        self.message_button.grid(row=33, column=0, sticky='w')
        self.read_file_and_initialize_ui()

    def msg_to_log(self):
        message = self.message_textbox.get("1.0", "end-1c")
        save_to_log(message)
        self.message_textbox.delete("1.0", "end")
        tk.messagebox.showinfo("Info", "Your message is added to log")

    def save_user_name(self):
        user_name = self.name_entry.get()
        save_to_log(f"{user_name} signs in")
        self.name_entry.delete(0, 'end')
        msg = f"Welcome, {user_name}.\n"
        tk.messagebox.showinfo("Message", msg)

    def update_file_path(self, file_path):
        self.contain = {}
        self.offload = []
        self.load_name_list = []
        self.load_weight_list = []
        self.container_data = {}
        self.selected_row = -1
        self.selected_column = -1
        self.selected_container_label.config(text="Selected Container: None")
        self.manifest_file_path = file_path
        for i in range(len(self.matrix_frames) - 1, -1, -1):
            for j in range(len(self.matrix_frames[i])):
                self.matrix_frames[i][j].config(text="", bg=self.default_bg, command=lambda:None)
        self.read_file_and_initialize_ui()

    def read_file_and_initialize_ui(self):
        if self.manifest_file_path:
            file_path = self.manifest_file_path
            if file_path:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                for line in lines:
                    position, weight, spot_name = line.strip().split(", ")
                    row, col = map(int, position.strip('[]').split(','))

                    self.container_data[(row-1, col-1)] = spot_name

                    if spot_name == "NAN":
                        self.matrix_frames[row-1][col-1].config(text="", bg="grey")
                    elif spot_name == "UNUSED":
                        continue
                    else:
                        self.matrix_frames[row - 1][col - 1].config(
                            text=spot_name,
                            bg="green",
                            command=lambda name=spot_name, r=row, c=col: self.set_selected_container(name, r, c)
                        )

    def set_selected_container(self, name, row, col):
            # Set the text of the label to the name of the selected container
            self.selected_container_label.config(text=f"Selected Container: {name}")
            self.selected_row = row-1
            self.selected_column = col-1

    def add_container(self):
        if self.selected_row != -1 and self.selected_column != -1:
            slot = (self.selected_row, self.selected_column)
            if slot not in self.offload:
                #print(slot)
                temp_msg = "Selected Ship slot [" + str(self.selected_row+1) + ", " + str(self.selected_column+1) + "]"
                self.offload.append(slot)
                self.selected_row = -1
                self.selected_column = -1
                self.selected_container_label.config(text="Selected Container: None")
                tk.messagebox.showinfo("Selected", temp_msg)
            else:
                self.selected_container_label.config(text="Selected Container: None")
                tk.messagebox.showinfo("Warning", "Already Selected the container!")


    def load_add(self):
        if self.loadname_entry.get() and self.loadweight_entry.get():
            if check_string(self.loadname_entry.get()) and check_weight(self.loadweight_entry.get()):
                self.load_name_list.append(self.loadname_entry.get())
                self.load_weight_list.append(self.loadweight_entry.get())
                self.loadname_entry.delete(0, 'end')
                self.loadweight_entry.delete(0, 'end')
                tk.messagebox.showinfo("Selected",
                                       "Added 1 load container to pending list.")
                return
        tk.messagebox.showinfo("Error", "Please enter valid inputs for load.")


    def done_select(self):
        if self.manifest_file_path and (self.offload or self.load_name_list):
            loadresult_page = self.controller.frames[LoadResultPage]
            loadresult_page.load_data_and_initialize_ui(self.manifest_file_path,
                                                        self.offload,
                                                        self.load_name_list,
                                                        self.load_weight_list,
                                                        self.container_data)
            self.controller.show_frame(LoadResultPage)
        else:
            tk.messagebox.showinfo("Done", "No action required.")
            self.controller.show_frame(StartPage)



class LoadResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_step_index = 0
        self.data = []
        self.output_json = None
        self.submit_button = tk.Button(self, text="Submit", command=self.save_user_name)
        self.submit_button.grid(row=42, column=0, sticky='w')
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=41, column=0, sticky='w')
        self.info_label = tk.Label(self, text="Login:")
        self.info_label.grid(row=40, column=0, sticky='w', pady=(25, 0))
        self.msg_label = tk.Label(self, text="Message :")
        self.msg_label.grid(row=31, column=0, sticky='w')
        self.message_textbox = tk.Text(self, height=4, width=40)
        self.message_textbox.grid(row=32, column=0)
        self.message_button = tk.Button(self, text="Add to log", command=self.msg_to_log)
        self.message_button.grid(row=33, column=0, sticky='w')
        self.initialize_ui(0)

    def msg_to_log(self):
        message = self.message_textbox.get("1.0", "end-1c")
        save_to_log(message)
        self.message_textbox.delete("1.0", "end")
        tk.messagebox.showinfo("Info", "Your message is added to log")
    def save_user_name(self):
        user_name = self.name_entry.get()
        save_to_log(f"{user_name} signs in")
        self.name_entry.delete(0, 'end')
        msg = f"Welcome, {user_name}.\n"
        tk.messagebox.showinfo("Message", msg)

    def load_data_and_initialize_ui(self, mani_path, offload, load_name, load_weight, data):
        file_path = mani_path
        if file_path:
            if onload_offload_main.onload_offload_algorithm(mani_path, offload, load_name, load_weight):
                self.data = data
                self.initialize_ui(0)
                return True
            else:
                tk.messagebox.showinfo("Error", "Problems occurs.")
                self.controller.show_frame(StartPage)
                return False

    def initialize_ui(self, step):
        file_path = 'output.json'
        self.current_step_index = step
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                self.output_json = json.load(file)
        self.step_label = tk.Label(self, text="")
        self.step_label.grid(row=0, column=0, sticky="w")
        self.time_label = tk.Label(self, text="")
        self.time_label.grid(row=2, column=0, sticky='w')

        # Matrix Display
        self.matrix_frames = [[tk.Frame(self, width=20, height=20, borderwidth=1, relief="solid") for _ in range(12)]
                              for _ in range(8)]

        for i in range(len(self.matrix_frames) - 1, -1, -1):
            for j in range(len(self.matrix_frames[i])):
                self.matrix_frames[i][j].grid(row=10 - i, column=j+5)

        self.next_button = tk.Button(self, text="Next", command=self.next_step)
        self.next_button.grid(row=20, column=0, columnspan=12)

        self.display_step()
        #self.controller.show_frame(StartPage)

    def display_step(self):
        if self.output_json:
            step_data = self.output_json['steps'][self.current_step_index]
            # Offload Process
            if not step_data['dest']:
                target = "[" + str((step_data['target'])[0] + 1) + ", " + str((step_data['target'])[1] + 1) + "]"
                self.step_label.config(
                    text=f"Step {step_data['No']}: Move from {step_data['targetLoc']} slot  {target} to "
                         f"{step_data['destLoc']}")
                row = step_data['target'][0]
                column = step_data['target'][1]
                key = (row, column)
                if key in self.data:
                    name = self.data[key]
                    self.data[key] = "UNUSED"
                    save_to_log(f"Container \"{name}\" is offloaded.")
            elif not step_data['target']:
                dest = "[" + str(step_data['dest'][0] + 1) + ", " + str(step_data['dest'][1] + 1) + "]"
                self.step_label.config(
                    text=f"Step {step_data['No']}: Move from {step_data['targetLoc']} to "
                         f"{step_data['destLoc']} slot {dest}")
                row = step_data['dest'][0]
                column = step_data['dest'][1]
                key = (row, column)
                if key in self.data:
                    name = self.data[key]
                    self.data[key] = "LOAD"
                save_to_log(f"One container is loaded.")
            else:
                target = "[" + str(step_data['target'][0] + 1) + ", " + str(step_data['target'][1] + 1) + "]"
                dest = "[" + str(step_data['dest'][0] + 1) + ", " + str(step_data['dest'][1] + 1) + "]"
                self.step_label.config(
                    text=f"Step {step_data['No']}: Move from {target} slot  {step_data['target']} to "
                         f"{step_data['destLoc']} slot {dest}")
                dest_row = step_data['dest'][0]
                dest_column = step_data['dest'][1]
                target_row = step_data['target'][0]
                target_column = step_data['target'][1]
                key_1 = (dest_row, dest_column)
                key_2 = (target_row, target_column)
                if key_1 and key_2 in self.data:
                    name = self.data[key_2]
                    self.data[key_2] = "UNUSED"
                    self.data[key_1] = name

            self.time_label.config(text=f"Estimated Time for this step: {step_data['cost']} minute(s). ")

            for i in range(8):
                for j in range(12):
                    loc_str = [i, j]
                    key = (i,j)
                    if self.data:
                        color = "green" if loc_str == step_data['target'] and "ship" == step_data['targetLoc'] \
                            else "red" if loc_str == step_data['dest'] and "ship" == step_data['destLoc'] \
                            else "grey" if self.data[key] != "UNUSED" else "white"
                        self.matrix_frames[i][j].config(bg=color)

    def next_step(self):
        load_file_path = 'output.json'
        self.current_step_index += 1

        if self.current_step_index >= len(self.output_json['steps']):
            self.next_button.config(text="Done", command=self.finish_display)
        else:
            self.display_step()
        self.output_json['currentSteps'] = self.current_step_index + 1
        if os.path.exists(load_file_path):
            with open(load_file_path, 'w') as file:
                json.dump(self.output_json, file, indent=4)

    def finish_display(self):
        try:
            os.remove('output.json')
        except OSError as e:
            tk.messagebox.showinfo("Error", "json file delete error.")
        self.data = []
        tk.messagebox.showinfo("Balancing Complete", "Please send the updated manifest.")
        save_to_log(
            f"Load & Offload is done, and a updated manifest is created under your import file folder. "
            f"A reminder pop-up to operator to send file was displayed.")
        self.controller.show_frame(StartPage)


class BalancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_step_index = 0
        self.output_json = None
        self.submit_button = tk.Button(self, text="Submit", command=self.save_user_name)
        self.submit_button.grid(row=42, column=0, sticky='w')
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=41, column=0, sticky='w')
        self.info_label = tk.Label(self, text="Login:")
        self.info_label.grid(row=40, column=0, sticky='w', pady=(25, 0))
        self.msg_label = tk.Label(self, text="Message :")
        self.msg_label.grid(row=31, column=0, sticky='w')
        self.message_textbox = tk.Text(self, height=4, width=40)
        self.message_textbox.grid(row=32, column=0)
        self.message_button = tk.Button(self, text="Add to log", command=self.msg_to_log)
        self.message_button.grid(row=33, column=0, sticky='w')
        self.initialize_ui(0)

    def msg_to_log(self):
        message = self.message_textbox.get("1.0", "end-1c")
        self.message_textbox.delete("1.0", "end")
        tk.messagebox.showinfo("Info", "Your message is added to log")
        save_to_log(message)

    def save_user_name(self):
        user_name = self.name_entry.get()
        save_to_log(f"{user_name} signs in")
        self.name_entry.delete(0, 'end')
        msg = f"Welcome, {user_name}.\n"
        tk.messagebox.showinfo("Message", msg)

    def load_data_and_initialize_ui(self):
        # Use the file path to load data
        file_path = self.controller.manifest_file_path
        if file_path:
            if balance.run(file_path):
                self.initialize_ui(0)
            else:
                tk.messagebox.showinfo("Balancing Complete", "The ship is already balanced.")
                self.controller.show_frame(StartPage)

    def initialize_ui(self, step):
        file_path = 'output_balance.json'
        self.current_step_index = step
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                self.output_json = json.load(file)
        self.step_label = tk.Label(self, text="")
        self.step_label.grid(row=0, column=0, sticky="w")
        self.time_label = tk.Label(self, text="")
        self.time_label.grid(row=2, column=0, sticky='w')

        self.matrix_frames = [[tk.Frame(self, width=20, height=20, borderwidth=1, relief="solid") for _ in range(12)]
                              for _ in range(8)]

        for i in range(len(self.matrix_frames) - 1, -1, -1):
            for j in range(len(self.matrix_frames[i])):
                self.matrix_frames[i][j].grid(row=10-i, column=j+5)

        # Next/Done Button
        self.next_button = tk.Button(self, text="Next", command=self.next_step)
        self.next_button.grid(row=30, column=0, columnspan=12)

        self.display_step()
        #self.controller.show_frame(StartPage)

    def display_step(self):
        if self.output_json:
            step_data = self.output_json['steps'][self.current_step_index]
            self.step_label.config(
                text=f"Step {step_data['No']}: Move from {step_data['targetLoc']} slot  {step_data['target']} to "
                     f"{step_data['destLoc']} slot {step_data['dest']}")
            self.time_label.config(text=f"Estimated Time for this step: {step_data['cost']} minute(s). ")

            # Update matrix display
            for i, row in enumerate(step_data['array']):
                for j, cell in enumerate(row):
                    loc_str = [i+1, j+1]
                    color = "green" if loc_str == step_data['target'] and "Ship" == step_data['targetLoc'] \
                        else "red" if loc_str == step_data['dest'] and "Ship" == step_data['destLoc'] \
                        else "grey" if cell == 'T' else "white"
                    self.matrix_frames[i][j].config(bg=color)


    def next_step(self):
        balance_file_path = 'output_balance.json'
        if self.output_json:
            self.current_step_index += 1

            if self.current_step_index >= len(self.output_json['steps']):
                self.next_button.config(text="Done", command=self.finish_balancing)
            else:
                self.display_step()
            self.output_json['currentSteps'] = self.current_step_index + 1
            if os.path.exists(balance_file_path):
                with open(balance_file_path, 'w') as file:
                    json.dump(self.output_json, file, indent=4)
        else:
            self.controller.show_frame(StartPage)
    def finish_balancing(self):
        try:
            os.remove('output_balance.json')
        except OSError as e:
            tk.messagebox.showinfo("Error", "json file delete error.")

        tk.messagebox.showinfo("Balancing Complete", "Please send the updated manifest.")
        save_to_log(f"Ship is balanced, and a updated manifest is created under your import file folder. A reminder pop-up to operator to send file was displayed.")
        self.controller.show_frame(StartPage)


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        container = tk.Frame(self)
        self.geometry('800x600')
        self.title("ShipAI")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.json_file_path = None
        self.manifest_file_path = None

        self.frames = {}

        for F in (StartPage, LoadOffloadPage, BalancePage, LoadResultPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()