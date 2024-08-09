from time import sleep
import customtkinter as ctk
from api.api_media import create_company, get_company_details
from app.gui.pop_up import close_loading_popup, show_loading_popup
from app.logic.business_logic import load_file_headers, load_file_columns, get_column_data
from tkinter import filedialog, messagebox
from app.logic.test_connect import test_zr_connection
from config.log_config import logger
from functions.dict_xml import contract_to_xml
from globals.global_vars import data_csv, footer_data

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

mandatory_columns = [
    "Company_id","Company_Name", "Company_ValidUntil","Participant_Contractid",
    "Participant_Firstname","Participant_Surname",
    "Participant_CardNumber","Participant_LPN1"
]
optional_columns = [
    "Company_ValidFrom", "Company_Surname", "Company_phone1","Company_email1", "Company_Street", "Company_Town",
    "Company_Postbox",  "Participant_FilialId",  "Participant_FirstName",  "Participant_Surname",  "Participant_Type",
    "Participant_Cardclass",  "Participant_IdentificationType",  "Participant_ValidFrom","Participant_ValidUntil",  
    "Participant_IgnorePresence",  "Participant_Present","Participant_Status",  "Participant_GrpNo",  "Participant_ChrgOvdrftAcct",
    "Participant_DisplayText",  "Participant_Limit",  "Participant_Status","Participant_Delete", "Participant_LPN2", "Participant_LPN3"
]

rows_data = []

print(f"hnaaa rows data \n {rows_data}")

class CSVLoaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Customer Media Processor")
        self.geometry("1300x700")

        self.optional_field_count = 0
        self.optional_fields = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.create_file_input_frame()
        self.create_mandatory_fields_frame()
        self.create_optional_fields_frame()
        self.create_sync_button()
        self.create_footer_frame()

    def create_file_input_frame(self):
        file_data_frame = ctk.CTkFrame(self.main_frame)
        file_data_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        file_data_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(file_data_frame, text="File Path:").grid(row=0, column=0, padx=5, pady=5)
        self.path_entry = ctk.CTkEntry(file_data_frame, width=400)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.browse_button = ctk.CTkButton(file_data_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.no_headers_var = ctk.BooleanVar(value=False)
        self.no_headers_check = ctk.CTkCheckBox(file_data_frame, text="No Headers", variable=self.no_headers_var)
        self.no_headers_check.grid(row=0, column=3, padx=5, pady=5)

        self.load_data_button = ctk.CTkButton(file_data_frame, text="Load Data", command=self.load_file_data)
        self.load_data_button.grid(row=0, column=4, padx=5, pady=5)

        ctk.CTkLabel(file_data_frame, text="Template ID:").grid(row=1, column=0, padx=5, pady=5)
        self.template_entry = ctk.CTkEntry(file_data_frame, width=400)
        self.template_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.template_entry.bind('<KeyRelease>', self.on_template_change)

    def create_mandatory_fields_frame(self):
        mandatory_frame = ctk.CTkFrame(self.main_frame)
        mandatory_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        mandatory_frame.grid_columnconfigure((1, 3, 5, 7, 9), weight=1)

        ctk.CTkLabel(mandatory_frame, text="Mandatory Fields", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=10, pady=10)

        self.dropdowns = []
        for i, label in enumerate(mandatory_columns):
            row = (i // 4) + 1
            col = (i % 4) * 2

            ctk.CTkLabel(mandatory_frame, text=label).grid(row=row, column=col, padx=5, pady=5, sticky="w")
            dropdown = ctk.CTkOptionMenu(mandatory_frame, width=150,)
            dropdown.grid(row=row, column=col+1, padx=5, pady=5, sticky="ew")
            dropdown.set("No Colomn selected")
            self.dropdowns.append((label, dropdown))

    def create_optional_fields_frame(self):
        optional_frame = ctk.CTkFrame(self.main_frame)
        optional_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        optional_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(optional_frame, text="Optional Fields", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        self.optional_field_var = ctk.StringVar()
        self.optional_field_dropdown = ctk.CTkOptionMenu(optional_frame, variable=self.optional_field_var, values=["No optional field"] + optional_columns, width=150)
        self.optional_field_dropdown.grid(row=1, column=0, padx=5, pady=5)
        self.optional_field_dropdown.set("No optional field")

        self.header_var = ctk.StringVar()
        self.header_dropdown = ctk.CTkOptionMenu(optional_frame, variable=self.header_var, values=[""], width=150)
        self.header_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.header_dropdown.set("No Column selected")

        add_button = ctk.CTkButton(optional_frame, text="+", width=30, command=self.add_optional_field)
        add_button.grid(row=1, column=2, padx=5, pady=5)

        self.optional_fields_container = ctk.CTkFrame(optional_frame)
        self.optional_fields_container.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.optional_fields_container.grid_columnconfigure((0, 1, 2), weight=1)

    def create_sync_button(self):
        sync_frame = ctk.CTkFrame(self.main_frame)
        sync_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        sync_frame.grid_columnconfigure(0, weight=1)

        self.sync_button = ctk.CTkButton(sync_frame, text="Sync", command=self.save_data)
        self.sync_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
    def create_footer_frame(self):
        footer_frame = ctk.CTkFrame(self.main_frame)
        footer_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        footer_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)  

        zr_def_values = {
            "zr_ip": "127.0.0.1",
            "zr_port": "8443",
            "username": "6",
            "password": "4711"
        }

        entries = [
            ("ZR IP", "zr_ip"),
            ("ZR Port", "zr_port"),
            ("Username", "username"),
            ("Password", "password")
        ]

        for i, (label, attr) in enumerate(entries):
            ctk.CTkLabel(footer_frame, text=label).grid(row=0, column=2 * i, padx=5, pady=5, sticky="w")
            entry = ctk.CTkEntry(footer_frame)
            entry.insert(0, zr_def_values.get(attr, ""))  
            entry.grid(row=0, column=2 * i + 1, padx=5, pady=5, sticky="ew")
            setattr(self, attr, entry)
            if attr == "password":
                entry.configure(show="*")

        self.confirm_button = ctk.CTkButton(footer_frame, text="Test & Confirm", command=self.save_zr_data)
        self.confirm_button.grid(row=0, column=8, padx=5, pady=10, sticky="e")

    def browse_file(self): 
        logger.debug("Selecting file process started...")       
        try:
            filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            logger.debug("Selecting CSV file ...")       

            if filename:
                self.path_entry.delete(0, ctk.END)
                self.path_entry.insert(0, filename)
                
                logger.success(f"CSV File Selected : {filename}")       

                self.load_file_data()

        except Exception as e:
                logger.error(f"Selecting CSV file Failed with error {str(e)}...")       
                messagebox.showerror("Error", "An error occurred - Selecting File")
         
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
                dropdown.configure(values=[""] + headers)
                dropdown.set("")
            self.header_dropdown.configure(values=[""] + headers)
            self.header_dropdown.set("")
        else:
            messagebox.showwarning("Warning", "The file appears to be empty.")

    def add_optional_field(self):
        field_name = self.optional_field_var.get()
        header_value = self.header_var.get()

        if field_name == "No optional field":
            messagebox.showwarning("Warning", "Please select an optional field.")
            return

        if header_value == "":
            messagebox.showwarning("Warning", "Please select a header value.")
            return

        if any(field[0] == field_name for field in self.optional_fields):
            messagebox.showwarning("Warning", "This optional field has already been added.")
            return

        # Calculate row and column based on the number of fields added
        index = len(self.optional_fields)
        row = index // 3
        col = (index % 3) * 2  # We use * 2 to leave space for the delete button in the next column

        # Create the label for the field
        label = ctk.CTkLabel(self.optional_fields_container, text=f"{field_name}: {header_value}")
        label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        # Create the delete button next to the label
        delete_button = ctk.CTkButton(self.optional_fields_container, text="X", width=30,
                                    command=lambda: self.delete_optional_field(field_name, label, delete_button))
        delete_button.grid(row=row, column=col + 1, padx=10, pady=5)

        # Add the field and header value to the list
        self.optional_fields.append((field_name, header_value))

        # Update the dropdown menu to remove the selected field name
        current_options = list(self.optional_field_dropdown.cget("values"))
        current_options.remove(field_name)

        # Handle the case where no more options are left
        if len(current_options) == 1:
            current_options = ["No optional field"]
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(current_options) == 1 else current_options[1])

        # Reset header dropdown
        self.header_dropdown.set("")

    def delete_optional_field(self, field_name, label, button):
        label.destroy()
        button.destroy()
        self.optional_fields = [field for field in self.optional_fields if field[0] != field_name]

        # Update dropdown options
        current_options = list(self.optional_field_dropdown.cget("values"))
        if "No optional field" not in current_options:
            current_options = ["No optional field"] + current_options
        current_options.append(field_name)
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(self.optional_fields) == 0 else current_options[1])

    def on_template_change(self, event):
        template_id = self.template_entry.get()
        logger.info(f"Template ID: {template_id}")

    def save_zr_data(self):
        global footer_data

        footer_data['zr_ip'] = self.zr_ip.get()
        footer_data['zr_port'] = self.zr_port.get()
        footer_data['username'] = self.username.get()
        footer_data['password'] = self.password.get()

        test_zr_connection()
        logger.info(f"ZR data saved: {footer_data}")
        messagebox.showinfo("Success", "ZR Data saved successfully!")

    def save_data(self):
        global data_csv, rows_data
        file_path = self.path_entry.get()

        data_csv = {}
        rows_data = []
        unique_company_ids = set()

        selected_columns = [(label, dropdown.get()) for label, dropdown in self.dropdowns if dropdown.get() != ""]
        selected_columns += [(name, header) for name, header in self.optional_fields]

        column_indices = [self.dropdowns[0][1].cget("values").index(column) - 1 for _, column in selected_columns]

        column_data, error = get_column_data(file_path, *column_indices)

        if error:
            messagebox.showerror("Error", f"Failed to retrieve column data: {error}")
            return

        for row in column_data:
            row_dict = {label: row[i] for i, (label, _) in enumerate(selected_columns)}
            rows_data.append(row_dict)
            
            company_id = row_dict.get('Company_id')
            
            if company_id and company_id not in unique_company_ids:
                logger.info(f"Data saved: {company_id}")
                unique_company_ids.add(company_id)

        print("Unique Company IDs:", " ".join(map(str, unique_company_ids)))

        for company_id in unique_company_ids:
            status_code, company_details = get_company_details(company_id)
            if status_code != 404:
                logger.info(f"Company ID {company_id} found")
                #logger.info(f"Company Detail : {company_details}")
            else:
                logger.info(f"Company ID {company_id} not found")
                
                # Find the corresponding row data for this company_id
                company_data = next((row for row in rows_data if row.get('Company_id') == company_id), None)
                
                if company_data:
                    data_contract = {
                        "contract": {
                            "id": company_data.get('Company_id'),
                            "name": company_data.get('Company_Name'),
                            "xValidFrom": company_data.get('Company_ValidFrom', 'NOVALIDFROM'),
                            "xValidUntil": company_data.get('Company_ValidUntil', '2025-12-31')
                        },
                        "person": {
                            "surname": company_data.get('Company_Surname', 'NOSURNAME'),
                            "phone1": company_data.get('Company_phone1', 'NONUMBER'),
                            "email1": company_data.get('Company_email1', 'NOEMAIL')
                        },
                        "stdAddr": {
                            "street": company_data.get('Company_Street', 'NOSTREET'),
                            "town": company_data.get('Company_Town', 'NOTOWN'),
                            "postbox": company_data.get('Company_Postbox', 'NOPOSTBOX')
                        }
                    }
                    
                    contract_xml = contract_to_xml(data_contract)
                    status_code, result = create_company(contract_xml)
                    
                    if status_code == 201:
                        logger.info(f"Company ID {company_id} created successfully")
                    else:
                        logger.error(f"Failed to create Company ID {company_id}. Status code: {status_code}")


        sleep(10)
        
        
            
            

        # Populate the data_csv dictionary with new data
        data_csv['template_id'] = self.template_entry.get()
        data_csv['file_path'] = file_path
        data_csv['no_headers'] = self.no_headers_var.get()
        data_csv['mandatory_fields'] = [(label, column) for label, column in selected_columns if label in mandatory_columns]
        data_csv['optional_fields'] = [(label, column) for label, column in selected_columns if label not in mandatory_columns]
        data_csv['rows_data'] = rows_data
        

        logger.info(f"Data saved")
        #messagebox.showinfo("Success", "Data saved successfully!")
        
