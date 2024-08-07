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
        