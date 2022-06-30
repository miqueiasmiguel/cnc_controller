from typing import Type
import serial
import tkinter as tk
from tkinter import ttk
from frame_serial_connection import SerialFrame
from frame_tab import TabFrame
from frame_movement import MovementFrame
from controller import Controller
from frame_display import DisplayFrame
import setup


class MainApplication(tk.Frame):
    def __init__(self, master: Type[tk.Frame]):
        self.master = master
        super().__init__(self.master)
        self.ser = serial.Serial()
        self.controller = Controller(events=setup.EVENTS)
        self.create_widgets()

    def create_widgets(self):
        self.frame_left = ttk.Frame(master=self.master)
        self.frame_left.pack(anchor="w")
        self.frame_middle = ttk.Frame(master=self.master)
        self.frame_middle.pack(anchor="n")
        self.frame_right = ttk.Frame(master=self.master)
        self.frame_right.pack(anchor="e")

        self.frame_serial = SerialFrame(
            master=self.frame_left, controller=self.controller, ser=self.ser
        )
        self.frame_serial.pack()
        self.frame_display = DisplayFrame(
            master=self.frame_left, controller=self.controller
        )
        self.frame_tab = TabFrame(
            master=self.frame_left, ser=self.ser, controller=self.controller
        )
        self.frame_tab.pack()
        self.frame_movement = MovementFrame(
            master=self.frame_left, ser=self.ser, controller=self.controller
        )
        self.frame_movement.pack()


if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()
