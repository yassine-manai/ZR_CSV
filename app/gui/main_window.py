import tkinter as tk
from app.logic.business_logic import load_file_headers, load_file_columns, get_column_data
from tkinter import filedialog, messagebox, ttk
from config.log_config import logger
from globals.global_vars import data_csv

mandatory_columns = ["Season Parker", "PMVC", "First Name", "LastName","Lpn", "tkep", "Licence Plate", "EPAN","PTcpt_name", "ptcpt id"]
optional_columns = ["Park", "LPNS"]
rows_data = []

class CSVLoaderApp:
    def __init__(self, master):
        self.master = master
        master.title("CSV/PSV File Processor")
        master.geometry("1300x700")

        self.optional_columns = ["Park", "LPNS"]
        self.optional_field_count = 0

        self.create_file_input_frame()
        self.create_mandatory_fields_frame()
        self.create_optional_fields_frame()
        self.create_footer_frame()

    def create_file_input_frame(self):
        file_data_frame = ttk.LabelFrame(self.master, text="File Data Infos")
        file_data_frame.pack(side=tk.TOP, pady=20, padx=20, fill=tk.X)

        input_frame = ttk.Frame(file_data_frame)
        input_frame.pack(pady=10, fill=tk.X)

        self.path_label = ttk.Label(input_frame, text="File Path:")
        self.path_label.pack(side=tk.LEFT, padx=(0, 10))
        self.path_entry = ttk.Entry(input_frame, width=50)
        self.path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.browse_button = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=(10, 20))

        self.no_headers_var = tk.BooleanVar(value=False)
        self.no_headers_check = ttk.Checkbutton(input_frame, text="No Headers", variable=self.no_headers_var)
        self.no_headers_check.pack(side=tk.LEFT, padx=(0, 10))

        self.load_data_button = ttk.Button(input_frame, text="Load Data", command=self.load_file_data)
        self.load_data_button.pack(side=tk.LEFT)
        
        template_frame = ttk.Frame(file_data_frame)
        template_frame.pack(pady=10, fill=tk.X)

        self.template_label = ttk.Label(template_frame, text="Template ID:")
        self.template_label.pack(side=tk.LEFT, padx=(0, 10))
        self.template_entry = ttk.Entry(template_frame, width=50)
        self.template_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.template_entry.bind('<KeyRelease>', self.on_template_change)

    def create_mandatory_fields_frame(self):
        mandatory_frame = ttk.LabelFrame(self.master, text="Mandatory Fields *")
        mandatory_frame.pack(pady=20, padx=20, fill=tk.X)
            
        self.dropdowns = []
        
        for i, label in enumerate(mandatory_columns):
            row = i // 5
            col = (i % 5) * 2
            
            label_widget = ttk.Label(mandatory_frame, text=label)
            label_widget.grid(row=row, column=col, padx=10, pady=5, sticky=tk.W)
            
            dropdown = ttk.Combobox(mandatory_frame, width=20, state="readonly")
            dropdown.grid(row=row, column=col+1, padx=5, pady=5, sticky=tk.W)
            
            self.dropdowns.append((label, dropdown))

    def create_optional_fields_frame(self):
        optional_frame = ttk.LabelFrame(self.master, text="Optional Fields")
        optional_frame.pack(pady=20, padx=20, fill=tk.X)

        # Create a frame for the dropdown and add button
        add_field_frame = ttk.Frame(optional_frame)
        add_field_frame.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=5)

        # Create dropdown for optional field selection
        self.optional_field_var = tk.StringVar()
        self.optional_field_dropdown = ttk.Combobox(add_field_frame, textvariable=self.optional_field_var, 
                                                    values=self.optional_columns, state="readonly", width=20)
        self.optional_field_dropdown.set("Select optional field")
        self.optional_field_dropdown.pack(side=tk.LEFT, padx=(0, 5))

        # Create add button
        add_button = ttk.Button(add_field_frame, text="+", command=self.add_optional_field)
        add_button.pack(side=tk.LEFT)

        # Create a frame for optional fields
        self.optional_fields_container = ttk.Frame(optional_frame)
        self.optional_fields_container.pack(fill=tk.X, expand=True, padx=10, pady=10)


    def add_optional_field(self):
        field_name = self.optional_field_var.get()
        if field_name == "Select optional field":
            messagebox.showwarning("Warning", "Please select an optional field.")
            return

        if any(field[0] == field_name for field in self.optional_fields):
            messagebox.showwarning("Warning", "This optional field has already been added.")
            return

        row = self.optional_field_count // 4
        col = (self.optional_field_count % 4) * 3

        # Create label
        label = ttk.Label(self.optional_fields_container, text=field_name)
        label.grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)

        # Create dropdown
        dropdown = ttk.Combobox(self.optional_fields_container, width=20, state="readonly")
        dropdown.grid(row=row, column=col+1, padx=5, pady=5, sticky=tk.W)

        if hasattr(self, 'dropdowns') and self.dropdowns:
            dropdown['values'] = self.dropdowns[0][1]['values']

        # Create delete button
        delete_button = ttk.Button(self.optional_fields_container, text="X", width=2,
                                   command=lambda: self.delete_optional_field(field_name, label, dropdown, delete_button))
        delete_button.grid(row=row, column=col+2, padx=(0, 5), pady=5, sticky=tk.W)

        self.optional_fields.append((field_name, dropdown))
        self.optional_field_count += 1
        
        # Remove the added field from the dropdown options
        current_options = list(self.optional_field_dropdown['values'])
        current_options.remove(field_name)
        self.optional_field_dropdown['values'] = current_options
        self.optional_field_dropdown.set("Select optional field")



    def create_footer_frame(self):
        footer_frame = ttk.Frame(self.master)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        entries = [
            ("ZR IP", "zr_ip"),
            ("ZR Port", "zr_port"),
            ("Username", "username"),
            ("Password", "password")
        ]

        for label, attr in entries:
            setattr(self, attr, tk.StringVar(value=label))
            entry = ttk.Entry(footer_frame, textvariable=getattr(self, attr))
            entry.pack(side=tk.LEFT, padx=5)
            if attr == "password":
                entry.configure(show="*")

        self.confirm_button = ttk.Button(footer_frame, text="Confirm", command=self.save_data)
        self.confirm_button.pack(side=tk.RIGHT, padx=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV/PSV Files", "*.csv")])
        if filename:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filename)
            self.load_file_data()

    def load_file_data(self):
        path = self.path_entry.get()
        if not path:
            messagebox.showerror("Error", "Please enter a file path or choose a file.")
            return

        headers, error = load_file_headers(path) if not self.no_headers_var.get() else load_file_columns(path)
        
        if error:
            messagebox.showerror("Error", error)
        elif headers:
            for label, dropdown in self.dropdowns:
                dropdown['values'] = [""] + headers  
                dropdown.set("")  
            for name, dropdown in self.optional_fields:
                dropdown['values'] = [""] + headers  
                dropdown.set("")   
        else:
            messagebox.showwarning("Warning", "The file appears to be empty.")
            
    def delete_optional_field(self, field_name, label, dropdown, button):
        label.destroy()
        dropdown.destroy()
        button.destroy()
        self.optional_fields = [field for field in self.optional_fields if field[0] != field_name]
        self.optional_field_count -= 1

        # Add the removed field back to the dropdown options
        current_options = list(self.optional_field_dropdown['values'])
        current_options.append(field_name)
        self.optional_field_dropdown['values'] = current_options
        self.optional_field_count -= 1

        
    def on_template_change(self, event):
        template_id = self.template_entry.get()
        logger.info(f"Template ID: {template_id}")

    def save_data(self):
        global data_csv
        file_path = self.path_entry.get()
        
        # Collect selected columns and their indices
        selected_columns = [(label, dropdown.current()) for label, dropdown in self.dropdowns if dropdown.current() != -1]
        selected_columns += [(name, dropdown.current()) for name, dropdown in self.optional_fields if dropdown.current() != -1]
        
        # Get column indices
        column_indices = [index for _, index in selected_columns]
        
        # Get the actual data for selected columns
        column_data, error = get_column_data(file_path, *column_indices)
        
        if error:
            messagebox.showerror("Error", f"Failed to retrieve column data: {error}")
            return
        
        # Create a list of dictionaries, each representing a row
        rows_data = []
        for row in column_data:
            row_dict = {label: row[i] for i, (label, _) in enumerate(selected_columns)}
            rows_data.append(row_dict)
        
        data_csv = {
            'template_id': self.template_entry.get(),
            'file_path': file_path,
            'no_headers': self.no_headers_var.get(),
            'mandatory_fields': [(label, index) for label, index in selected_columns if label in mandatory_columns],
            'optional_fields': [(label, index) for label, index in selected_columns if label not in mandatory_columns],
            'zr_ip': self.zr_ip.get(),
            'zr_port': self.zr_port.get(),
            'username': self.username.get(),
            'password': self.password.get(),
            'rows_data': rows_data  
        }
        
        logger.info(f"Data saved: {data_csv.get('rows_data')}")
        messagebox.showinfo("Success", "Data saved successfully!")
                
        
