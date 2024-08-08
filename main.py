import tkinter as tk
from app.gui.main_window import CSVLoaderApp
from globals.global_vars import  data_csv
def main():
    root = tk.Tk()
    app = CSVLoaderApp(root)
    root.mainloop()
    print(data_csv)
    
if __name__ == "__main__":
    main()
