from tkinter import  Tk

from PIL.ImageTk import PhotoImage

from model import Producto

if __name__ == '__main__':
    root = Tk()
    app = Producto(root)
    root.mainloop()
