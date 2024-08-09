import threading
import customtkinter as ctk

    
class pop_up(ctk.CTk):

    def create_loading_popup(self, message="Loading...", timer=None):
        # Create a Toplevel window (popup)
        self.loading_popup = ctk.CTkToplevel(self.main_frame)
        self.loading_popup.title("Loading")
        self.loading_popup.geometry("300x100")  # Set the size of the popup
        self.loading_popup.resizable(False, False)  # Prevent resizing
        
        # Center the popup on the screen
        self.loading_popup.update_idletasks()
        x = (self.loading_popup.winfo_screenwidth() // 2) - (self.loading_popup.winfo_width() // 2)
        y = (self.loading_popup.winfo_screenheight() // 2) - (self.loading_popup.winfo_height() // 2)
        self.loading_popup.geometry(f'+{x}+{y}')
        
        # Create a frame inside the popup
        loading_frame = ctk.CTkFrame(self.loading_popup)
        loading_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Add a loading label
        loading_label = ctk.CTkLabel(loading_frame, text=message, font=("Arial", 14))
        loading_label.pack(pady=10)

        # Optionally, add a progress bar or spinner
        progress_bar = ctk.CTkProgressBar(loading_frame, mode="indeterminate")
        progress_bar.pack(fill="x", pady=10)
        progress_bar.start()

        # This will make the popup modal (blocks interaction with other windows)
        self.loading_popup.transient(self.main_frame)
        self.loading_popup.grab_set()

        # If a timer is specified, close the popup after the specified time
        if timer:
            threading.Timer(timer, self.close_loading_popup).start()

        # Block interaction with other windows until the popup is closed
        self.main_frame.wait_window(self.loading_popup)

    def close_loading_popup(self):
        if self.loading_popup:
            self.loading_popup.destroy()  