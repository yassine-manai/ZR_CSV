import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from app.logic.business_logic import load_file_headers, load_file_columns, get_column_data

mandatory_columns = ["Season Parker", "PMVC", "First Name", "LastName", "Licence Plate", "EPAN","PTcpt_name", "ptcpt id"]

class CSVLoaderApp:
    def __init__(self, master):
        self.master = master
        master.title("CSV/PSV File Processor")
        master.geometry("1200x700")

        self.local_data = {}  # Dictionary to store local data

        self.create_file_input_frame()
        self.create_mandatory_fields_frame()
        self.create_data_display_frame()
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
            row = i // 4
            col = (i % 4) * 2
            
            label_widget = ttk.Label(mandatory_frame, text=label)
            label_widget.grid(row=row, column=col, padx=10, pady=5, sticky=tk.W)
            
            dropdown = ttk.Combobox(mandatory_frame, width=25, state="readonly")
            dropdown.grid(row=row, column=col+1, padx=5, pady=5, sticky=tk.W)
            dropdown.bind("<<ComboboxSelected>>", self.update_data_display)
            
            self.dropdowns.append(dropdown)


    def create_optional_fields_frame(self):
        optional_frame = ttk.LabelFrame(self.master, text="Optional Fields")
        optional_frame.pack(pady=20, padx=20, fill=tk.X)

        hello_world_label = ttk.Label(optional_frame, text="Hello World")
        hello_world_label.pack(pady=10)

    def create_data_display_frame(self):
        self.data_frame = ttk.LabelFrame(self.master, text="Data Display")
        self.data_frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

        self.data_tree = ttk.Treeview(self.data_frame, columns=tuple(mandatory_columns), show="headings")
        for col in mandatory_columns:
            self.data_tree.heading(col, text=col)
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
            for dropdown in self.dropdowns:
                dropdown['values'] = headers
                dropdown.set(headers[0] if headers else '')
            self.update_data_display()
        else:
            messagebox.showwarning("Warning", "The file appears to be empty.")

    def update_data_display(self, event=None):
        path = self.path_entry.get()
        columns = [dropdown.get() for dropdown in self.dropdowns if dropdown.get()]

        if path and len(columns) >= 2:
            data, error = get_column_data(path, *columns[:2])  # Using first two selected columns
            if error:
                messagebox.showerror("Error", error)
            else:
                self.data_tree.delete(*self.data_tree.get_children())
                for item in data[:10]:  # Display only the first 10 rows
                    self.data_tree.insert("", "end", values=item)

    def on_template_change(self, event):
        template_id = self.template_entry.get()
        print(f"Template ID: {template_id}")

    def save_data(self):
        self.local_data = {
            'template_id': self.template_entry.get(),
            'file_path': self.path_entry.get(),
            'no_headers': self.no_headers_var.get(),
            'fields': [dropdown.get() for dropdown in self.dropdowns],
            'zr_ip': self.zr_ip.get(),
            'zr_port': self.zr_port.get(),
            'username': self.username.get(),
            'password': self.password.get()
        }
        print("Data saved:", self.local_data)
        messagebox.showinfo("Success", "Data saved successfully!")