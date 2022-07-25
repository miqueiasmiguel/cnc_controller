from typing import Type
import tkinter as tk
from tkinter import ttk, filedialog
import serial
from controller import Controller
from file_handler import FileHandler


class AutoFrame(tk.Frame):
    def __init__(
        self,
        master: Type[tk.Frame],
        controller: Type[Controller],
        ser: Type[serial.Serial] = None,
    ):
        self.master = master
        super().__init__(self.master)
        self.ser = ser
        self.hinge_path = None
        self.knob_path = None
        self.controller = controller
        self.file_handler = FileHandler()
        self.controller.subscribe(
            event="set_door", observer=self, callback=self.set_door_dimensions
        )
        self.create_widgets()

    def create_widgets(self):
        self.labelframe_auto = ttk.Labelframe(master=self.master, text="Propriedades")
        self.labelframe_auto.pack(anchor="w")

        self.label_height = ttk.Label(master=self.labelframe_auto, text="Altura (cm):")
        self.label_width = ttk.Label(master=self.labelframe_auto, text="Largura (cm):")
        self.label_d = ttk.Label(master=self.labelframe_auto, text="d (cm):")
        self.label_k = ttk.Label(master=self.labelframe_auto, text="k (cm):")
        self.label_hinge = ttk.Label(master=self.labelframe_auto, text="Ferragem:")
        self.label_knob = ttk.Label(master=self.labelframe_auto, text="Maçaneta:")
        self.spinbox_height = ttk.Spinbox(
            master=self.labelframe_auto,
            from_=0,
            to=999999,
            format="%.2f",
            increment=0.1,
        )
        self.spinbox_width = ttk.Spinbox(
            master=self.labelframe_auto,
            from_=0,
            to=999999,
            format="%.2f",
            increment=0.1,
        )
        self.spinbox_d = ttk.Spinbox(
            master=self.labelframe_auto,
            from_=0,
            to=999999,
            format="%.2f",
            increment=0.1,
        )
        self.spinbox_k = ttk.Spinbox(
            master=self.labelframe_auto,
            from_=0,
            to=999999,
            format="%.2f",
            increment=0.1,
        )
        self.button_hinge = ttk.Button(
            master=self.labelframe_auto, text="Selecionar", command=self.__browse_hinge
        )
        self.button_knob = ttk.Button(
            master=self.labelframe_auto, text="Selecionar", command=self.__browse_knob
        )
        self.button_previsualize = ttk.Button(
            master=self.labelframe_auto,
            text="Pré-visualizar",
            command=self.__generate_door,
        )

        self.label_height.grid(row=0, column=0, sticky=tk.W)
        self.spinbox_height.grid(row=0, column=1)
        self.label_width.grid(row=1, column=0, sticky=tk.W)
        self.spinbox_width.grid(row=1, column=1)
        self.label_d.grid(row=2, column=0, sticky=tk.W)
        self.spinbox_d.grid(row=2, column=1)
        self.label_k.grid(row=3, column=0, sticky=tk.W)
        self.spinbox_k.grid(row=3, column=1)
        self.label_hinge.grid(row=4, column=0, sticky=tk.W)
        self.button_hinge.grid(row=4, column=1)
        self.label_knob.grid(row=5, column=0, sticky=tk.W)
        self.button_knob.grid(row=5, column=1)
        self.button_previsualize.grid(row=6, column=0)

    def __browse_hinge(self):
        self.hinge_path = filedialog.askopenfilename()

    def __browse_knob(self):
        self.knob_path = filedialog.askopenfilename()

    def set_door_dimensions(self):
        self.controller.door_height = float(self.spinbox_height.get())
        self.controller.door_width = float(self.spinbox_width.get())
        self.controller.door_d = float(self.spinbox_d.get())
        self.controller.door_k = float(self.spinbox_k.get())
        self.controller.door_hinge_path = self.hinge_path
        self.controller.door_knob_path = self.knob_path

    def __generate_door(self):
        self.controller.dispatch(event="set_door")
        self.file_handler.plot_door(
            hinge_path=self.controller.door_hinge_path,
            knob_path=self.controller.door_knob_path,
            height=self.controller.door_height,
            width=self.controller.door_width,
            d=self.controller.door_d,
            k=self.controller.door_k,
        )
