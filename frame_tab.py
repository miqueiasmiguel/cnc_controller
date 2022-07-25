from typing import Type
import tkinter as tk
from tkinter import ttk
import serial
from frame_tab_auto import AutoFrame
from frame_tab_manual import ManualFrame
from frame_tab_setup import SetupFrame
from controller import Controller


class TabFrame(tk.Frame):
    def __init__(
        self,
        master: Type[tk.Frame],
        controller: Type[Controller],
        ser: Type[serial.Serial] = None,
    ):
        self.master = master
        super().__init__(self.master)
        self.ser = ser
        self.controller = controller
        self.current_tab = 0
        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(master=self.master)
        self.tab_auto = ttk.Frame(master=self.tab_control)
        self.tab_manual = ttk.Frame(master=self.tab_control)
        self.tab_setup = ttk.Frame(master=self.tab_control)

        self.tab_control.add(child=self.tab_auto, text="Automático")
        self.tab_control.add(child=self.tab_manual, text="Manual")
        self.tab_control.add(child=self.tab_setup, text="Configurações")
        self.tab_control.pack(anchor="w")

        self.frame_auto = AutoFrame(
            master=self.tab_auto, controller=self.controller, ser=self.ser
        )
        self.frame_auto.pack()
        self.frame_manual = ManualFrame(
            master=self.tab_manual, ser=self.ser, controller=self.controller
        )
        self.frame_manual.pack()
        self.frame_setup = SetupFrame(master=self.tab_setup, ser=self.ser)
        self.frame_setup.pack()

        self.tab_control.bind("<<NotebookTabChanged>>", self.set_current_tab)

    def set_current_tab(self, event):
        self.controller.active_tab = event.widget.index("current")
