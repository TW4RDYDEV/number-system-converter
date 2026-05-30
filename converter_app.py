import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class NumberConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number System Converter by TWARDY")
        self.root.geometry("720x760")
        self.root.minsize(720, 760)

        self.number_types = ["Decimal", "Binary", "Hexadecimal"]
        self.current_result = ""
        self.history = []

        self.live_mode_enabled = tk.BooleanVar(value=True)
        self.light_mode_enabled = tk.BooleanVar(value=False)

        self.dark_theme = {
            "bg": "#1e1e1e",
            "panel": "#2d2d2d",
            "text": "#ffffff",
            "muted": "#aaaaaa",
            "accent": "#00ff88",
            "button": "#00ff88",
            "button_text": "#000000",
            "secondary": "#444444",
            "entry": "#2d2d2d",
            "entry_text": "#ffffff",
            "check_bg": "#1e1e1e",
            "check_select": "#00ff88"
        }

        self.light_theme = {
            "bg": "#f4f4f4",
            "panel": "#ffffff",
            "text": "#111111",
            "muted": "#555555",
            "accent": "#007a3d",
            "button": "#00b866",
            "button_text": "#000000",
            "secondary": "#dddddd",
            "entry": "#ffffff",
            "entry_text": "#000000",
            "check_bg": "#f4f4f4",
            "check_select": "#00b866"
        }

        self.theme = self.dark_theme

        self.setup_styles()
        self.create_widgets()
        self.apply_theme()
        self.update_to_options()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.pack(pady=(5, 15))

        self.title_label = tk.Label(
            self.title_frame,
            text="Number System Converter",
            font=("Segoe UI", 22, "bold")
        )
        self.title_label.pack(side="left")

        self.watermark_label = tk.Label(
            self.title_frame,
            text=" by TWARDY",
            font=("Segoe UI", 10, "bold")
        )
        self.watermark_label.pack(side="left", anchor="s", padx=(4, 0), pady=(0, 4))

        self.settings_frame = tk.Frame(self.main_frame)
        self.settings_frame.pack(fill="x", pady=(0, 10))

        self.live_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Live conversion",
            variable=self.live_mode_enabled,
            command=self.handle_live_toggle,
            font=("Segoe UI", 10),
            cursor="hand2",
            onvalue=True,
            offvalue=False
        )
        self.live_checkbox.pack(side="left")

        self.theme_checkbox = tk.Checkbutton(
            self.settings_frame,
            text="Light mode",
            variable=self.light_mode_enabled,
            command=self.toggle_theme,
            font=("Segoe UI", 10),
            cursor="hand2",
            onvalue=True,
            offvalue=False
        )
        self.theme_checkbox.pack(side="right")

        self.converter_frame = tk.Frame(self.main_frame)
        self.converter_frame.pack(pady=5)

        self.from_label = tk.Label(
            self.converter_frame,
            text="Convert from:",
            font=("Segoe UI", 11)
        )
        self.from_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.from_type = ttk.Combobox(
            self.converter_frame,
            values=self.number_types,
            state="readonly",
            width=23,
            style="BlackText.TCombobox"
        )
        self.from_type.grid(row=0, column=1, padx=10, pady=10)
        self.from_type.current(0)
        self.from_type.bind("<<ComboboxSelected>>", self.on_type_change)

        self.to_label = tk.Label(
            self.converter_frame,
            text="Convert to:",
            font=("Segoe UI", 11)
        )
        self.to_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.to_type = ttk.Combobox(
            self.converter_frame,
            state="readonly",
            width=23,
            style="BlackText.TCombobox"
        )
        self.to_type.grid(row=1, column=1, padx=10, pady=10)
        self.to_type.bind("<<ComboboxSelected>>", self.on_type_change)

        self.input_label = tk.Label(
            self.converter_frame,
            text="Enter number:",
            font=("Segoe UI", 11)
        )
        self.input_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.number_entry = tk.Entry(
            self.converter_frame,
            font=("Consolas", 13),
            width=26,
            relief="flat"
        )
        self.number_entry.grid(row=2, column=1, padx=10, pady=10)
        self.number_entry.bind("<KeyRelease>", self.handle_typing)
        self.number_entry.bind("<Return>", lambda event: self.convert_number(add_to_history=True))

        self.prefix_hint = tk.Label(
            self.main_frame,
            text="Supports prefixes like 0b1010 and 0xF3C. Binary spaces are allowed.",
            font=("Segoe UI", 9)
        )
        self.prefix_hint.pack(pady=(0, 8))

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=(10, 15))

        self.convert_button = tk.Button(
            self.button_frame,
            text="Convert",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            width=16,
            command=lambda: self.convert_number(add_to_history=True),
            cursor="hand2"
        )
        self.convert_button.grid(row=0, column=0, padx=6)

        self.copy_button = tk.Button(
            self.button_frame,
            text="Copy Result",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            width=16,
            command=self.copy_result,
            cursor="hand2"
        )
        self.copy_button.grid(row=0, column=1, padx=6)

        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            width=16,
            command=self.reset_app,
            cursor="hand2"
        )
        self.reset_button.grid(row=0, column=2, padx=6)

        self.result_title = tk.Label(
            self.main_frame,
            text="Result:",
            font=("Segoe UI", 13, "bold")
        )
        self.result_title.pack(pady=(5, 8))

        self.result_label = tk.Label(
            self.main_frame,
            text="Waiting for input...",
            font=("Consolas", 17, "bold"),
            width=48,
            height=2,
            cursor="hand2",
            wraplength=620
        )
        self.result_label.pack(pady=(0, 5))
        self.result_label.bind("<Button-1>", self.copy_result)

        self.copy_hint = tk.Label(
            self.main_frame,
            text="Click the result or press Copy Result to copy it",
            font=("Segoe UI", 9)
        )
        self.copy_hint.pack(pady=(0, 12))

        self.details_frame = tk.Frame(self.main_frame)
        self.details_frame.pack(fill="x", pady=(0, 12))

        self.details_label = tk.Label(
            self.details_frame,
            text="Number details will appear here.",
            font=("Consolas", 10),
            justify="left",
            anchor="w"
        )
        self.details_label.pack(fill="x", padx=10, pady=10)

        self.history_title_frame = tk.Frame(self.main_frame)
        self.history_title_frame.pack(fill="x", pady=(5, 5))

        self.history_title = tk.Label(
            self.history_title_frame,
            text="Conversion History",
            font=("Segoe UI", 13, "bold")
        )
        self.history_title.pack(side="left")

        self.save_history_button = tk.Button(
            self.history_title_frame,
            text="Save History",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            command=self.save_history,
            cursor="hand2"
        )
        self.save_history_button.pack(side="right", padx=(5, 0))

        self.clear_history_button = tk.Button(
            self.history_title_frame,
            text="Clear History",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            command=self.clear_history,
            cursor="hand2"
        )
        self.clear_history_button.pack(side="right")

        self.history_listbox = tk.Listbox(
            self.main_frame,
            font=("Consolas", 10),
            height=8,
            activestyle="none"
        )
        self.history_listbox.pack(fill="both", expand=True)
        self.history_listbox.bind("<Double-Button-1>", self.copy_selected_history)

    def apply_theme(self):
        self.theme = self.light_theme if self.light_mode_enabled.get() else self.dark_theme

        self.root.configure(bg=self.theme["bg"])
        self.main_frame.configure(bg=self.theme["bg"])
        self.title_frame.configure(bg=self.theme["bg"])
        self.settings_frame.configure(bg=self.theme["bg"])
        self.converter_frame.configure(bg=self.theme["bg"])
        self.button_frame.configure(bg=self.theme["bg"])
        self.history_title_frame.configure(bg=self.theme["bg"])
        self.details_frame.configure(bg=self.theme["panel"])

        labels = [
            self.title_label,
            self.watermark_label,
            self.from_label,
            self.to_label,
            self.input_label,
            self.prefix_hint,
            self.result_title,
            self.copy_hint,
            self.details_label,
            self.history_title
        ]

        for label in labels:
            label.configure(
                bg=self.theme["bg"],
                fg=self.theme["text"]
            )

        self.title_label.configure(fg=self.theme["accent"])
        self.watermark_label.configure(fg=self.theme["muted"])
        self.prefix_hint.configure(fg=self.theme["muted"])
        self.copy_hint.configure(fg=self.theme["muted"])
        self.details_label.configure(bg=self.theme["panel"], fg=self.theme["text"])

        self.live_checkbox.configure(
            bg=self.theme["bg"],
            fg=self.theme["text"],
            activebackground=self.theme["bg"],
            activeforeground=self.theme["text"],
            selectcolor=self.theme["check_select"]
        )

        self.theme_checkbox.configure(
            bg=self.theme["bg"],
            fg=self.theme["text"],
            activebackground=self.theme["bg"],
            activeforeground=self.theme["text"],
            selectcolor=self.theme["check_select"]
        )

        self.result_label.configure(
            bg=self.theme["panel"],
            fg=self.theme["accent"]
        )

        self.number_entry.configure(
            bg=self.theme["entry"],
            fg=self.theme["entry_text"],
            insertbackground=self.theme["entry_text"]
        )

        self.convert_button.configure(
            bg=self.theme["button"],
            fg=self.theme["button_text"],
            activebackground=self.theme["button"],
            activeforeground=self.theme["button_text"]
        )

        secondary_buttons = [
            self.copy_button,
            self.reset_button,
            self.save_history_button,
            self.clear_history_button
        ]

        for button in secondary_buttons:
            button.configure(
                bg=self.theme["secondary"],
                fg=self.theme["text"],
                activebackground=self.theme["secondary"],
                activeforeground=self.theme["text"]
            )

        self.history_listbox.configure(
            bg=self.theme["panel"],
            fg=self.theme["text"],
            selectbackground=self.theme["accent"],
            selectforeground="#000000"
        )

        self.style.configure(
            "BlackText.TCombobox",
            fieldbackground="#e6e6e6",
            background="#e6e6e6",
            foreground="#000000",
            selectforeground="#000000",
            selectbackground="#e6e6e6",
            arrowcolor="#000000"
        )

        self.style.map(
            "BlackText.TCombobox",
            fieldbackground=[
                ("readonly", "#e6e6e6"),
                ("disabled", "#e6e6e6")
            ],
            foreground=[
                ("readonly", "#000000"),
                ("disabled", "#000000")
            ],
            selectforeground=[
                ("readonly", "#000000")
            ],
            selectbackground=[
                ("readonly", "#e6e6e6")
            ],
            background=[
                ("readonly", "#e6e6e6")
            ]
        )

    def toggle_theme(self):
        self.apply_theme()

    def update_to_options(self):
        selected_from = self.from_type.get()

        available_options = [
            option for option in self.number_types
            if option != selected_from
        ]

        current_to = self.to_type.get()
        self.to_type["values"] = available_options

        if current_to in available_options:
            self.to_type.set(current_to)
        else:
            self.to_type.current(0)

    def on_type_change(self, event=None):
        self.update_to_options()
        self.convert_number(add_to_history=False)

    def handle_live_toggle(self):
        if self.live_mode_enabled.get():
            self.convert_number(add_to_history=False)

    def handle_typing(self, event=None):
        if self.live_mode_enabled.get():
            self.convert_number(add_to_history=False)

    def clean_input(self, number, from_type):
        number = number.strip()

        if from_type == "Binary":
            number = number.replace(" ", "").replace("_", "")

            if number.lower().startswith("0b"):
                number = number[2:]

        elif from_type == "Hexadecimal":
            number = number.replace(" ", "").replace("_", "")

            if number.lower().startswith("0x"):
                number = number[2:]

        elif from_type == "Decimal":
            number = number.replace(" ", "").replace("_", "")

        return number

    def validate_input(self, number, from_type):
        if number.strip() == "":
            return False, "Please enter a number."

        cleaned = self.clean_input(number, from_type)

        if cleaned == "":
            return False, f"Please enter a valid {from_type} number."

        if from_type == "Decimal":
            if not cleaned.isdigit():
                return False, "Decimal numbers can only contain digits from 0 to 9."

            return True, ""

        if from_type == "Binary":
            invalid_chars = sorted(set(char for char in cleaned if char not in "01"))

            if invalid_chars:
                return False, f"Binary numbers can only contain 0 and 1. Invalid: {', '.join(invalid_chars)}"

            return True, ""

        if from_type == "Hexadecimal":
            valid_hex_chars = "0123456789abcdefABCDEF"
            invalid_chars = sorted(set(char for char in cleaned if char not in valid_hex_chars))

            if invalid_chars:
                return False, f"Hexadecimal numbers can only contain 0-9 and A-F. Invalid: {', '.join(invalid_chars)}"

            return True, ""

        return False, "Unknown number type."

    def convert_to_decimal(self, cleaned_number, from_type):
        if from_type == "Decimal":
            return int(cleaned_number)

        if from_type == "Binary":
            return int(cleaned_number, 2)

        if from_type == "Hexadecimal":
            return int(cleaned_number, 16)

        raise ValueError("Unknown number type.")

    def convert_from_decimal(self, decimal_number, to_type):
        if to_type == "Decimal":
            return str(decimal_number)

        if to_type == "Binary":
            return bin(decimal_number)[2:]

        if to_type == "Hexadecimal":
            return hex(decimal_number)[2:].upper()

        raise ValueError("Unknown number type.")

    def group_binary(self, binary_number):
        if binary_number == "0":
            return "0"

        reversed_binary = binary_number[::-1]

        groups = [
            reversed_binary[i:i + 4][::-1]
            for i in range(0, len(reversed_binary), 4)
        ]

        return " ".join(groups[::-1])

    def build_details_text(self, decimal_value):
        binary_value = bin(decimal_value)[2:]
        hex_value = hex(decimal_value)[2:].upper()
        grouped_binary = self.group_binary(binary_value)
        bit_length = decimal_value.bit_length()

        return (
            f"Decimal:        {decimal_value}\n"
            f"Binary:         {binary_value}\n"
            f"Grouped Binary: {grouped_binary}\n"
            f"Hexadecimal:    {hex_value}\n"
            f"Bit Length:     {bit_length}"
        )

    def convert_number(self, add_to_history=False):
        number = self.number_entry.get()
        from_type = self.from_type.get()
        to_type = self.to_type.get()

        if from_type == to_type:
            self.show_soft_error("You cannot convert a number to the same type.")
            return

        is_valid, error_message = self.validate_input(number, from_type)

        if not is_valid:
            self.current_result = ""
            self.result_label.config(text="Waiting for valid input...")
            self.details_label.config(text=error_message)
            self.copy_hint.config(text="Fix the input to convert.", fg=self.theme["muted"])

            if add_to_history:
                messagebox.showerror("Input Error", error_message)

            return

        cleaned_number = self.clean_input(number, from_type)

        try:
            decimal_value = self.convert_to_decimal(cleaned_number, from_type)
            final_result = self.convert_from_decimal(decimal_value, to_type)

            self.current_result = final_result

            self.result_label.config(
                text=final_result,
                fg=self.theme["accent"]
            )

            self.details_label.config(
                text=self.build_details_text(decimal_value)
            )

            self.copy_hint.config(
                text="Click the result or press Copy Result to copy it",
                fg=self.theme["muted"]
            )

            if add_to_history:
                history_line = f"{cleaned_number} {from_type} → {to_type} = {final_result}"
                self.add_to_history(history_line)

        except ValueError:
            self.show_soft_error("Something went wrong while converting the number.")

    def show_soft_error(self, message):
        self.current_result = ""
        self.result_label.config(text="Error")
        self.details_label.config(text=message)
        self.copy_hint.config(text=message, fg=self.theme["muted"])

    def add_to_history(self, history_line):
        if not self.history or self.history[-1] != history_line:
            self.history.append(history_line)
            self.history_listbox.insert(tk.END, history_line)
            self.history_listbox.see(tk.END)

    def copy_result(self, event=None):
        if self.current_result == "":
            self.copy_hint.config(
                text="Nothing to copy yet.",
                fg=self.theme["muted"]
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_result)
        self.root.update()

        self.copy_hint.config(
            text="Copied result to clipboard!",
            fg=self.theme["accent"]
        )

    def copy_selected_history(self, event=None):
        selection = self.history_listbox.curselection()

        if not selection:
            return

        selected_text = self.history_listbox.get(selection[0])

        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
        self.root.update()

        self.copy_hint.config(
            text="Copied selected history line!",
            fg=self.theme["accent"]
        )

    def save_history(self):
        if not self.history:
            messagebox.showinfo("No History", "There is no conversion history to save yet.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Conversion History",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("Number System Converter by TWARDY - Conversion History\n")
                file.write("=" * 60)
                file.write("\n\n")

                for item in self.history:
                    file.write(item + "\n")

            messagebox.showinfo("Saved", "Conversion history saved successfully.")

        except OSError:
            messagebox.showerror("Save Error", "Could not save the history file.")

    def clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)

        self.copy_hint.config(
            text="History cleared.",
            fg=self.theme["muted"]
        )

    def reset_app(self):
        self.number_entry.delete(0, tk.END)
        self.current_result = ""

        self.from_type.current(0)
        self.update_to_options()

        self.result_label.config(
            text="Waiting for input...",
            fg=self.theme["accent"]
        )

        self.details_label.config(
            text="Number details will appear here."
        )

        self.copy_hint.config(
            text="Click the result or press Copy Result to copy it",
            fg=self.theme["muted"]
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberConverterApp(root)
    root.mainloop()