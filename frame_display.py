from typing import Type
import tkinter as tk
from tkinter import ttk
from controller import Controller


class DisplayFrame(tk.Frame):
    def __init__(self, master: Type[tk.Frame], controller: Type[Controller] = None):
        self.master = master
        super().__init__(self.master)
        self.controller = controller
        self.controller.subscribe(
            event="new_coord", observer=self, callback=self.update_display
        )
        self.create_widgets()

    def create_widgets(self):
        self.labelframe_display = ttk.Labelframe(
            master=self.master, text="Valores atuais"
        )
        self.labelframe_display.pack(anchor="w")

        self.var_current_x = tk.StringVar(master=self.labelframe_display)
        self.var_current_y = tk.StringVar(master=self.labelframe_display)
        self.var_current_z = tk.StringVar(master=self.labelframe_display)
        self.var_abs_x = tk.StringVar(master=self.labelframe_display)
        self.var_abs_y = tk.StringVar(master=self.labelframe_display)
        self.var_abs_z = tk.StringVar(master=self.labelframe_display)
        self.var_wco_x = tk.StringVar(master=self.labelframe_display)
        self.var_wco_y = tk.StringVar(master=self.labelframe_display)
        self.var_wco_z = tk.StringVar(master=self.labelframe_display)
        self.var_current_status = tk.StringVar(master=self.labelframe_display)

        self.label_x = ttk.Label(master=self.labelframe_display, text="X:")
        self.label_y = ttk.Label(master=self.labelframe_display, text="Y:")
        self.label_z = ttk.Label(master=self.labelframe_display, text="Z:")
        self.label_status = ttk.Label(master=self.labelframe_display, text="Status:")
        self.label_current = ttk.Label(master=self.labelframe_display, text="Current:")
        self.label_abs = ttk.Label(master=self.labelframe_display, text="ABS:")
        self.label_wco = ttk.Label(master=self.labelframe_display, text="WCO:")

        self.label_current_x = tk.Label(
            master=self.labelframe_display, textvariable=self.var_current_x
        )
        self.label_current_y = tk.Label(
            master=self.labelframe_display, textvariable=self.var_current_y
        )
        self.label_current_z = tk.Label(
            master=self.labelframe_display, textvariable=self.var_current_z
        )
        self.label_abs_x = tk.Label(
            master=self.labelframe_display, textvariable=self.var_abs_x
        )
        self.label_abs_y = tk.Label(
            master=self.labelframe_display, textvariable=self.var_abs_y
        )
        self.label_abs_z = tk.Label(
            master=self.labelframe_display, textvariable=self.var_abs_z
        )
        self.label_wco_x = tk.Label(
            master=self.labelframe_display, textvariable=self.var_wco_x
        )
        self.label_wco_y = tk.Label(
            master=self.labelframe_display, textvariable=self.var_wco_y
        )
        self.label_wco_z = tk.Label(
            master=self.labelframe_display, textvariable=self.var_wco_z
        )
        self.label_current_status = tk.Label(
            master=self.labelframe_display, textvariable=self.var_current_status
        )

        self.label_current.grid(row=0, column=1)
        self.label_abs.grid(row=0, column=2)
        self.label_wco.grid(row=0, column=3)
        self.label_x.grid(row=1, column=0)
        self.label_y.grid(row=2, column=0)
        self.label_z.grid(row=3, column=0)
        self.label_current_x.grid(row=1, column=1)
        self.label_current_y.grid(row=2, column=1)
        self.label_current_z.grid(row=3, column=1)
        self.label_abs_x.grid(row=1, column=2)
        self.label_abs_y.grid(row=2, column=2)
        self.label_abs_z.grid(row=3, column=2)
        self.label_wco_x.grid(row=1, column=3)
        self.label_wco_y.grid(row=2, column=3)
        self.label_wco_z.grid(row=3, column=3)
        self.label_status.grid(row=4, column=0)
        self.label_current_status.grid(row=4, column=1)

    def update_display(
        self,
        x_coord,
        y_coord,
        z_coord,
        x_abs,
        y_abs,
        z_abs,
        wco_x,
        wco_y,
        wco_z,
        status,
    ):
        self.var_current_x.set(x_coord)
        self.var_current_y.set(y_coord)
        self.var_current_z.set(z_coord)
        self.var_abs_x.set(x_abs)
        self.var_abs_y.set(y_abs)
        self.var_abs_z.set(z_abs)
        self.var_wco_x.set(wco_x)
        self.var_wco_y.set(wco_y)
        self.var_wco_z.set(wco_z)
        self.var_current_status.set(status)
