import threading
import customtkinter as ctk
from tkinter import StringVar, filedialog, messagebox
from api.api_media import create_company, create_participant, get_company_details, get_participant
from app.gui.pop_up import close_loading_popup, create_loading_popup
from app.logic.business_logic import load_file_headers, load_file_columns, get_data
from app.logic.test_connect import test_zr_connection
from classes.validator_class import Company_validation, Consumer_validation
from config.log_config import logger
from functions.data_format import generate_unique_random
from functions.dict_xml import consumer_to_xml, contract_to_xml
from globals.global_vars import data_csv, zr_data, glob_vals

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

mandatory_columns = [
    "Company_id", "Company_Name", "Company_ValidUntil", "Participant_Contractid",
    "Participant_Firstname", "Participant_Surname",
    "Participant_CardNumber", "Participant_LPN1"
]
optional_columns = [
    "Company_ValidFrom", "Company_Surname", "Company_phone1", "Company_email1", "Company_Street", "Company_Town",
    "Company_Postbox", "Participant_FilialId", "Participant_FirstName", "Participant_Surname", "Participant_Type",
    "Participant_Cardclass", "Participant_IdentificationType", "Participant_ValidFrom", "Participant_ValidUntil",
    "Participant_Present", "Participant_Status", "Participant_GrpNo", "Participant_ChrgOvdrftAcct",
    "Participant_DisplayText", "Participant_Status", "Participant_LPN2", "Participant_LPN3"
]

date_format_dict = {
    "dd-mm-yyyy": "%d-%m-%Y",
    "dd.mm.yyyy": "%d.%m.%Y",
    "dd:mm:yyyy": "%d:%m:%Y",
    "yyyy-mm-dd": "%Y-%m-%d"
}


rows_data = []

logger.info("Starting Process & user interface . . . ")

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
        file_data_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # File path input section
        ctk.CTkLabel(file_data_frame, text="File Path:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.path_entry = ctk.CTkEntry(file_data_frame, width=400)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.browse_button = ctk.CTkButton(file_data_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.no_headers_var = ctk.BooleanVar(value=False)
        self.no_headers_check = ctk.CTkCheckBox(file_data_frame, text="No Headers", variable=self.no_headers_var)
        self.no_headers_check.grid(row=0, column=3, padx=5, pady=5)

        self.load_data_button = ctk.CTkButton(file_data_frame, text="Load Data", command=self.load_file_data)
        self.load_data_button.grid(row=0, column=4, padx=5, pady=5)

        # Template ID section
        ctk.CTkLabel(file_data_frame, text="Template ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Season Parker ID
        ctk.CTkLabel(file_data_frame, text="Season Parker ID:").grid(row=1, column=1, padx=5, pady=5, sticky="e")
        self.template1_var = StringVar(value="1")
        self.template1_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template1_var, width=50)
        self.template1_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # PMVC ID
        ctk.CTkLabel(file_data_frame, text="PMVC ID:").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.template2_var = StringVar(value="2")
        self.template2_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template2_var, width=50)
        self.template2_entry.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

        # CPM ID
        ctk.CTkLabel(file_data_frame, text="CPM ID:").grid(row=1, column=5, padx=5, pady=5, sticky="e")
        self.template3_var = StringVar(value="3")
        self.template3_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template3_var, width=50)
        self.template3_entry.grid(row=1, column=6, padx=5, pady=5, sticky="ew")

        # Date Format
        ctk.CTkLabel(file_data_frame, text="Date Format:").grid(row=1, column=7, padx=5, pady=5, sticky="e")
        self.date_format_var = StringVar(value="yyyy-mm-dd")
        self.date_format_dropdown = ctk.CTkOptionMenu(file_data_frame, variable=self.date_format_var,
                                                    values=list(date_format_dict.keys()), width=100,
                                                    command=self.update_date_format)
        
        self.date_format_dropdown.grid(row=1, column=8, padx=5, pady=5, sticky="ew")

        file_data_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # Initialize global variable values
        self.update_global_values()

    def update_date_format(self, selected_format):
        global glob_vals
        glob_vals['date_format_val'] = date_format_dict.get(selected_format, '%d-%m-%Y')
        logger.info(f"Date Format updated to: {glob_vals['date_format_val']}")
        self.update_template_id()  

    def update_global_values(self):
        global glob_vals
        selected_format = self.date_format_var.get()
        glob_vals['date_format_val'] = date_format_dict.get(selected_format, '%d-%m-%Y')
        glob_vals['season_parker'] = self.template1_var.get()
        glob_vals['pmvc'] = self.template2_var.get()
        glob_vals['cmp'] = self.template3_var.get()

    def update_template_id(self):
        global glob_vals
        self.update_global_values()
        try:
            template_id1 = int(glob_vals['season_parker'])
            template_id2 = int(glob_vals['pmvc'])
            template_id3 = int(glob_vals['cmp'])
            logger.info(f"------------ {glob_vals['date_format_val']}")
            logger.info(f"Template ID updated to: {template_id1} -- {template_id2} -- {template_id3}")
        except ValueError:
            logger.error("Error: Invalid template ID value.")

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
            dropdown = ctk.CTkOptionMenu(mandatory_frame, width=150,values="", command=self.check_mandatory_fields)
            dropdown.grid(row=row, column=col+1, padx=5, pady=5, sticky="ew")
            dropdown.set("- - - - - - - - - ")
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

        self.optional_fields_container = ctk.CTkFrame(optional_frame,height=0)
        self.optional_fields_container.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.optional_fields_container.grid_columnconfigure((0, 1, 2), weight=1)

    def create_sync_button(self):
        sync_frame = ctk.CTkFrame(self.main_frame)
        sync_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        sync_frame.grid_columnconfigure(0, weight=1)

        self.sync_button = ctk.CTkButton(sync_frame, text="Sync", command=self.start_sync, state="disabled")
        self.sync_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    def create_footer_frame(self):
        footer_frame = ctk.CTkFrame(self.main_frame)
        footer_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        footer_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)  

        entries = [
            ("ZR IP", "zr_ip"),
            ("ZR Port", "zr_port"),
            ("Username", "username"),
            ("Password", "password")
        ]

        for i, (label, attr) in enumerate(entries):
            ctk.CTkLabel(footer_frame, text=label).grid(row=0, column=2 * i, padx=5, pady=5, sticky="w")
            entry = ctk.CTkEntry(footer_frame)

            entry.insert(0, zr_data.get(attr, ""))  
            entry.grid(row=0, column=2 * i + 1, padx=5, pady=5, sticky="ew")
            setattr(self, attr, entry)


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
            self.check_mandatory_fields()
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
        


        index = len(self.optional_fields)
        row = index // 3
        col = (index % 3) * 2

        label = ctk.CTkLabel(self.optional_fields_container, text=f"{field_name}: {header_value}")
        label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        delete_button = ctk.CTkButton(self.optional_fields_container, text="X", width=30,
                                    command=lambda: self.delete_optional_field(field_name, label, delete_button))
        delete_button.grid(row=row, column=col + 1, padx=10, pady=5)

        self.optional_fields.append((field_name, header_value))

        current_options = list(self.optional_field_dropdown.cget("values"))
        current_options.remove(field_name)

        if len(current_options) == 1:
            current_options = ["No optional field"]
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(current_options) == 1 else current_options[1])

        self.header_dropdown.set("")

    def delete_optional_field(self, field_name, label, button):
        label.destroy()
        button.destroy()
        self.optional_fields = [field for field in self.optional_fields if field[0] != field_name]

        current_options = list(self.optional_field_dropdown.cget("values"))
        if "No optional field" not in current_options:
            current_options = ["No optional field"] + current_options
        current_options.append(field_name)
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(self.optional_fields) == 0 else current_options[1])

    def check_mandatory_fields(self, *args):
        # Check if all dropdowns have valid selections
        all_selected = all(
            dropdown.get().strip() not in ["No Column selected", "", " ", "- - - - - - - - - "] for _, dropdown in self.dropdowns
        )

        self.sync_button.configure(state="normal" if all_selected else "disabled")

    def start_sync(self):
        self.loading_popup = create_loading_popup(self.master, "Syncing data...")
        threading.Thread(target=self.save_data_threaded, daemon=True).start()
     
    def save_data_threaded(self):
        try:
            self.update_template_id()  
            self.save_data()
            # for x in lc for compagny
            # for x in lp for ptcpt
        finally:
            self.close_loading_popup()

    def close_loading_popup(self):
        if hasattr(self, 'loading_popup'):
            close_loading_popup(self.loading_popup)
            del self.loading_popup

    def save_zr_data(self):
        global zr_data

        zr_data['zr_ip'] = self.zr_ip.get().strip()
        zr_data['zr_port'] = self.zr_port.get().strip()
        zr_data['username'] = self.username.get().strip()
        zr_data['password'] = self.password.get().strip()
        
        logger.debug(zr_data)        
        test_zr_connection(zr_data)  
        
        # file as list of dict
        rows_data = self.read_data_from_file()  

        # Get unique company IDs
        company_ids = set(row.get('Company_id') for row in rows_data if row.get('Company_id'))

        # call ZR version 
        
        # build LIst [ compagnyobject]
        lc=[]
        # build list [ ptcpt object]
        lp=[]
        
        # for in lc check compagny id on zr






    def process_participants(self, company_id, rows_data, template_ids):
        possible_numbers = set(range(1001))
        logger.info(f"Processing participants for Company ID: {company_id}")

        company_rows = [row for row in rows_data if row.get('Company_id') == company_id]
        logger.info(company_rows)
        
        for row in company_rows:
            participant_id = row.get('Participant_Contractid')
            logger.debug(f"Processing Participant ID: {participant_id}")

            if participant_id:
                status_code, participant_details = get_participant(company_id, participant_id)
                
                if status_code != 404:
                    logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")
                else:
                    logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")
                    
                    # Create participant data
                    card_nbm = generate_unique_random(possible_numbers)
                    
                    data_consumer = {
                        "id": participant_id,
                        "contractid": company_id,
                        "xValidFrom": row.get('Participant_ValidFrom', '2000-01-01'),
                        "xValidUntil": row.get('Participant_ValidUntil', '2025-01-01'),
                        "filialId": row.get('Participant_FilialId', 7077),
                        "firstName": row.get('Participant_Firstname', ''),
                        "surname": row.get('Participant_Surname', ''),
                        "ptcptType": row.get('Participant_Type', '3'),
                        "cardno": card_nbm,
                        "cardclass": row.get('Participant_Cardclass', '0'),
                        "identificationType": row.get('Participant_IdentificationType', '51'),
                        "validFrom": row.get('Participant_ValidFrom', '2020-01-01'),
                        "validUntil": row.get('Participant_ValidUntil', '2025-01-01'),
                        "admission": "",
                        "ignorePresence": row.get('Participant_IgnorePresence', '0'),
                        "present": row.get('Participant_Present', 'false'),
                        "status": row.get('Participant_Status', '0'),
                        "ptcptGrpNo": row.get('Participant_GrpNo', '-1'),
                        "displayText": row.get('Participant_DisplayText', '-1'),
                        "limit": row.get('Participant_Limit', '9999900'),
                        "memo": "Note1",
                        "delete": row.get('Participant_Delete', '0'),
                        "lpn1": row.get('Participant_LPN1', 'NOLPN'),
                        "lpn2": row.get('Participant_LPN2', 'NOLPN'),
                        "lpn3": row.get('Participant_LPN3', 'NOLPN'),
                    }

                    logger.debug(data_consumer)
                    validated_consumer = Consumer_validation(**data_consumer)   
                    consumer_xml = consumer_to_xml(validated_consumer.dict())
                    logger.debug(f"Participant data: {consumer_xml}")
                    
                    ptcpt_type = row.get('Participant_Type', 3)
                    if ptcpt_type == 2:
                        template_id = template_ids["season_parker"]
                    if ptcpt_type == 6:
                        template_id = template_ids["pmvc"]
                    else:
                        template_id = template_ids.get("default", template_ids["season_parker"])
                    
                    status_code, result = create_participant(company_id, template_id, consumer_xml)
                    
                    if status_code == 201:
                        logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                    else:
                        logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

    def save_data(self):
        global data_csv, rows_data, glob_vals
        file_path = self.path_entry.get()

        template_ids = glob_vals

        logger.info("Starting api call process . . . ")

        data_csv = {}
        rows_data = []
        unique_company_ids = set()

        selected_columns = [(label, dropdown.get()) for label, dropdown in self.dropdowns if dropdown.get() != "No Column selected"]
        selected_columns += [(name, header) for name, header in self.optional_fields]

        column_indices = [self.dropdowns[0][1].cget("values").index(column) - 1 for _, column in selected_columns]

        column_data, error = get_data(file_path, *column_indices)

        if error:
            logger.error(f"Failed to retrieve column data: {error}")
            messagebox.showerror("Error", f"Failed to retrieve column data: {error}")
            return

        for row in column_data:
            row_dict = {label: row[i] for i, (label, _) in enumerate(selected_columns)}
            rows_data.append(row_dict)
            
            company_id = row_dict.get('Company_id')
            
            if company_id and company_id not in unique_company_ids:
                logger.info(f"Data saved for company id : {company_id}")
                unique_company_ids.add(company_id)

        logger.info(f"Unique Company IDs: {', '.join(map(str, unique_company_ids))}")

        for company_id in unique_company_ids:
            status_code, company_details = get_company_details(company_id)
            if status_code != 404:
                logger.info(f"Company ID {company_id} found")
                
                # Process participants for existing company
                self.process_participants(company_id, rows_data, template_ids)
            else:
                logger.info(f"Company ID {company_id} not found")
                
                # Find the corresponding row data for this company_id
                company_data = next((row for row in rows_data if row.get('Company_id') == company_id), None)
                
                if company_data:
                    data_contract = {
                            "id": int(company_data.get('Company_id')),
                            "name": company_data.get('Company_Name'),
                            "xValidFrom": company_data.get('Company_ValidFrom', ''),
                            "xValidUntil": company_data.get('Company_ValidUntil', '2025-12-31'),
                            "filialId": 7077,
                            "surname": company_data.get('Company_Surname', 'NOSURNAME'),
                            "phone1": company_data.get('Company_phone1', 'NONUMBER'),
                            "email1": company_data.get('Company_email1', 'NOEMAIL'),
                            "street": company_data.get('Company_Street', 'NOSTREET'),
                            "town": company_data.get('Company_Town', 'NOTOWN'),
                            "postbox": company_data.get('Company_Postbox', 'NOPOSTBOX')
                        }
                    
                    
                    logger.debug(data_contract)
                    validated_company = Company_validation(**data_contract)   
                    company_xml = contract_to_xml(validated_company.dict())
                    logger.debug(f"Participant data: {company_xml}")

                    status_code, result = create_company(company_xml)
                    logger.debug(f"Status code : {status_code}")
                    
                    if status_code == 201:
                        logger.info(f"Company ID {company_id} created successfully")
                        # Process participants for newly created company
                        self.process_participants(company_id, rows_data, template_ids)
                    else:
                        logger.error(f"Failed to create Company ID {company_id}. Status code: {status_code}")
                        
        logger.info("Data save process completed")
        messagebox.showinfo("Success", "Data processing completed successfully!")