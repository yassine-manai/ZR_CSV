import tkinter as tk
from app.gui.main_window import CSVLoaderApp

def main():
    root = tk.Tk()
    app = CSVLoaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()