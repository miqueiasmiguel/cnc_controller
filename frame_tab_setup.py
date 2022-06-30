from typing import Type
import tkinter as tk
from tkinter import ttk
import serial


class SetupFrame(tk.Frame):
    def __init__(self, master: Type[tk.Frame], ser: Type[serial.Serial] = None):
        self.master = master
        super().__init__(self.master)
        self.ser = ser
        self.create_widgets()

    def create_widgets(self):
        self.labelframe_zero = ttk.Labelframe(master=self.master, text="Zero")
        self.labelframe_zero.pack(anchor="w")

        self.button_zero_x = ttk.Button(
            master=self.labelframe_zero, text="Zerar X", command=self.__reset_x
        )
        self.button_zero_y = ttk.Button(
            master=self.labelframe_zero, text="Zerar Y", command=self.__reset_y
        )
        self.button_zero_z = ttk.Button(
            master=self.labelframe_zero, text="Zerar Z", command=self.__reset_z
        )
        self.button_zero_return = ttk.Button(
            master=self.labelframe_zero,
            text="Retornar para zero",
            command=self.__return_to_zero,
        )

        self.button_zero_x.grid(row=0, column=0, sticky="e")
        self.button_zero_y.grid(row=0, column=1, sticky="ew")
        self.button_zero_z.grid(row=0, column=2, sticky="w")
        self.button_zero_return.grid(row=1, column=1)

    def __reset_x(self):
        self.ser.write(str.encode("G10P0L20X0\n"))
        self.ser.readline()

    def __reset_y(self):
        self.ser.write(str.encode("G10P0L20Y0\n"))
        self.ser.readline()

    def __reset_z(self):
        self.ser.write(str.encode("G10P0L20Z0\n"))
        self.ser.readline()

    def __return_to_zero(self):
        self.ser.write(str.encode("G21G90G0Z5\n"))
        self.ser.readline()
        self.ser.write(str.encode("G90G0X0Y0\n"))
        self.ser.readline()
        self.ser.write(str.encode("G90G0Z0\n"))
        self.ser.readline()


if __name__ == "__main__":
    root = tk.Tk()
    app = SetupFrame(root)
    root.mainloop()
