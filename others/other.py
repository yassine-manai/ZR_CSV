# Name field
        self.name_label = ttk.Label(mandatory_frame, text="Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(mandatory_frame, width=50,state="readonly") 
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Dropdown list
        self.dropdown_label = ttk.Label(mandatory_frame, text="Field:")
        self.dropdown_label.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.dropdown = ttk.Combobox(mandatory_frame, width=50, state="readonly")  
        self.dropdown.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)



def create_footer_frame(self):
        footer_frame = ttk.Frame(self.master)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        self.zr_ip = tk.StringVar(value="ZR IP")
        self.zr_port = tk.StringVar(value="ZR Port")
        self.username = tk.StringVar(value="Username")
        self.password = tk.StringVar(value="Password")
        

        self.name_label = ttk.Label(footer_frame, text="ZR_IP:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)   
        self.zr_ip_entry = ttk.Entry(footer_frame, textvariable=self.zr_ip, state='readonly')
        self.zr_ip_entry.pack(side=tk.LEFT, padx=5)

        self.name_label = ttk.Label(footer_frame, text="ZR_PORT:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)  
        self.zr_port_entry = ttk.Entry(footer_frame, textvariable=self.zr_port, state='readonly')
        self.zr_port_entry.pack(side=tk.LEFT, padx=5)

        self.name_label = ttk.Label(footer_frame, text="Username:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)  
        self.username_entry = ttk.Entry(footer_frame, textvariable=self.username, state='readonly')
        self.username_entry.pack(side=tk.LEFT, padx=5)

        self.name_label = ttk.Label(footer_frame, text="Password:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)  
        self.password_entry = ttk.Entry(footer_frame, textvariable=self.password, state='readonly', show='*')
        self.password_entry.pack(side=tk.LEFT, padx=5)

        self.settings_icon = ttk.Button(footer_frame, text="Config ⚙", command=self.toggle_settings)
        self.settings_icon.pack(side=tk.RIGHT, padx=5)

        self.confirm_button = ttk.Button(footer_frame, text="Confirm", command=self.confirm_settings)
        self.cancel_button = ttk.Button(footer_frame, text="Cancel", command=self.cancel_settings)

        self.editing_settings = False




import tkinter as tk
from app.logic.business_logic import load_file_headers, load_file_columns, get_column_data
from tkinter import filedialog, messagebox, ttk
from config.log_config import logger

mandatory_columns = ["Season Parker", "PMVC", "First Name", "LastName", "Lpn", "tkep", "Licence Plate", "EPAN", "PTcpt_name", "ptcpt id"]
optional_labels = ["Park", "Store"]

class CSVLoaderApp:
    def __init__(self, master):
        self.master = master
        master.title("CSV/PSV File Processor")
        master.geometry("1300x700")

        self.local_data = {}
        self.optional_columns = []
        self.optional_field_count = 0

        self.create_file_input_frame()
        self.create_mandatory_fields_frame()
        self.create_optional_fields_frame()
        self.create_data_display_frame()
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
        self.no_headers_check = ttk.Checkbutton(input_frame, text="No Headers", 
                                                variable=self.no_headers_var)
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
            dropdown.bind("<<ComboboxSelected>>", self.update_data_display)
            
            self.dropdowns.append((label, dropdown))

    def create_optional_fields_frame(self):
        optional_frame = ttk.LabelFrame(self.master, text="Optional Fields")
        optional_frame.pack(pady=20, padx=20, fill=tk.X)

        # Create a frame for the + icon and dropdown
        add_field_frame = ttk.Frame(optional_frame)
        add_field_frame.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=5)

        self.optional_field_label = tk.StringVar(value=optional_labels[0])
        field_label_dropdown = ttk.Combobox(add_field_frame, textvariable=self.optional_field_label, values=optional_labels, state="readonly", width=20)
        field_label_dropdown.pack(side=tk.LEFT, padx=(0, 5))

        self.add_button = ttk.Button(add_field_frame, text="+", command=self.add_optional_field)
        self.add_button.pack(side=tk.LEFT)

        # Create a frame for optional fields
        self.optional_fields_container = ttk.Frame(optional_frame)
        self.optional_fields_container.pack(fill=tk.X, expand=True, padx=10, pady=10)

    def add_optional_field(self):
        field_label = self.optional_field_label.get().strip()
        if not field_label:
            messagebox.showwarning("Warning", "Please select a field label.")
            return

        row = self.optional_field_count // 4
        col = (self.optional_field_count % 4) * 4  # Adjusted column positioning

        # Create label
        label = ttk.Label(self.optional_fields_container, text=field_label)
        label.grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)

        # Create label dropdown
        dropdown_label = ttk.Combobox(self.optional_fields_container, width=20, state="readonly")
        dropdown_label.grid(row=row, column=col+1, padx=5, pady=5, sticky=tk.W)
        dropdown_label['values'] = optional_labels
        
        # Create value dropdown
        dropdown_value = ttk.Combobox(self.optional_fields_container, width=20, state="readonly")
        dropdown_value.grid(row=row, column=col+2, padx=5, pady=5, sticky=tk.W)
        dropdown_value.bind("<<ComboboxSelected>>", self.update_data_display)

        # Populate value dropdown with file headers when a label is selected
        dropdown_label.bind("<<ComboboxSelected>>", lambda event: self.update_value_dropdown(dropdown_label, dropdown_value))

        # Create delete button
        delete_button = ttk.Button(self.optional_fields_container, text="X", width=2,
                                command=lambda: self.delete_optional_field(label, dropdown_label, dropdown_value, delete_button))
        delete_button.grid(row=row, column=col+3, padx=(0, 5), pady=5, sticky=tk.W)

        self.optional_columns.append((field_label, dropdown_label, dropdown_value))
        self.optional_field_count += 1

    def update_value_dropdown(self, label_dropdown, value_dropdown):
    # Check if the label dropdown has a selected value
        label_value = label_dropdown.get()
        if label_value:
            # Update value dropdown based on selected label
            if hasattr(self, 'headers') and self.headers:
                value_dropdown['values'] = [""] + self.headers
            else:
                value_dropdown['values'] = [""]
            value_dropdown.set("")
        else:
            value_dropdown['values'] = [""]

    def create_data_display_frame(self):
        self.data_frame = ttk.LabelFrame(self.master, text="Data Display")
        self.data_frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

        self.data_tree = ttk.Treeview(self.data_frame)
        self.data_tree.pack(fill=tk.BOTH, expand=True)

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
        filename = filedialog.askopenfilename(filetypes=[("CSV/PSV Files", "*.csv *.PSV")])
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
            self.headers = headers  # Save headers for dropdown usage
            
            # Update mandatory field dropdowns
            for label, dropdown in self.dropdowns:
                dropdown['values'] = [""] + headers
                dropdown.set("")

            # Update optional field dropdowns
            for _, dropdown_label, dropdown_value in self.optional_columns:
                dropdown_label['values'] = optional_labels
                self.update_value_dropdown(dropdown_value)

            self.update_data_display()
        else:
            messagebox.showwarning("Warning", "The file appears to be empty.")
            
    def delete_optional_field(self, label, dropdown_label, dropdown_value, button):
        label.destroy()
        dropdown_label.destroy()
        dropdown_value.destroy()
        button.destroy()
        self.optional_columns = [field for field in self.optional_columns if field[1] != dropdown_label]
        self.optional_field_count -= 1
        self.update_data_display()

    def update_data_display(self, event=None):
        path = self.path_entry.get()
        columns = [(label, dropdown.get()) for label, dropdown in self.dropdowns if dropdown.get()]
        columns += [(name, dropdown_value.get()) for name, dropdown_value in self.optional_columns if dropdown_value.get()]

        if not path:
            messagebox.showwarning("Warning", "Please select a file.")
            return

        column_names = [col[1] for col in columns]
        data, error = get_column_data(path, *column_names)
        if error:
            messagebox.showerror("Error", error)
            return

        # Update treeview columns to show column indexes
        self.data_tree['columns'] = [f"Column {i+1}" for i in range(len(column_names))]
        self.data_tree['show'] = 'headings'

        # Clear existing columns and add new ones
        for col in self.data_tree['columns']:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=100)
            self.data_tree.column(col, anchor='center')

        # Clear existing data
        self.data_tree.delete(*self.data_tree.get_children())

        # Insert new data showing indexes
        for row_index, item in enumerate(data[:10]):  # Display only the first 10 rows
            self.data_tree.insert("", "end", values=[row_index+1] + item)

        if not data:
            messagebox.showinfo("Info", "No data to display.")

        logger.info("Displayed Data Columns and Locations:")
        for i, col in enumerate(self.data_tree['columns']):
            logger.info(f"Index {i}: {col}")
        for row_index, item in enumerate(data[:10]):
            logger.info(f"Row {row_index+1}: Indexes {row_index+1} with values {item}")
        
    def on_template_change(self, event):
        template_id = self.template_entry.get()
        logger.info(f"Template ID: {template_id}")

    def save_data(self):
        self.local_data = {
            'template_id': self.template_entry.get(),
            'file_path': self.path_entry.get(),
            'no_headers': self.no_headers_var.get(),
            'mandatory_fields': [(label, dropdown.get()) for label, dropdown in self.dropdowns if dropdown.get()],
            'optional_fields': [(name, dropdown_value.get()) for name, dropdown_value in self.optional_columns if dropdown_value.get()],
            'zr_ip': self.zr_ip.get(),
            'zr_port': self.zr_port.get(),
            'username': self.username.get(),
            'password': self.password.get()
        }
        logger.info("Data saved:", self.local_data)
        messagebox.showinfo("Success", "Data saved successfully!")
