import serial
from typing import Type
import tkinter as tk
from tkinter import ttk
from controller import Controller


class ManualFrame(tk.Frame):
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
        self.controller.subscribe(
            event="set_coord", observer=self, callback=self.set_manual_coord
        )
        self.create_widgets()

    def create_widgets(self):
        # Setup
        self.labelframe_setup = ttk.Labelframe(master=self.master, text="Configuração")
        self.labelframe_setup.pack(anchor="w")

        var_feed_rate = tk.IntVar(master=self.labelframe_setup, value=1)
        var_step_size = tk.DoubleVar(master=self.labelframe_setup, value=1)

        self.label_feedrate = ttk.Label(master=self.labelframe_setup, text="Feed rate:")
        self.label_stepsize = ttk.Label(
            master=self.labelframe_setup, text="Tamanho do passo:"
        )
        self.spinbox_feedrate = tk.Spinbox(
            master=self.labelframe_setup,
            from_=0,
            to=999999,
            textvariable=var_feed_rate,
        )
        self.spinbox_stepsize = tk.Spinbox(
            master=self.labelframe_setup,
            from_=0,
            to=999999,
            format="%.2f",
            textvariable=var_step_size,
        )

        self.label_feedrate.grid(row=0, column=0, sticky=tk.W)
        self.label_stepsize.grid(row=0, column=1, sticky=tk.W)
        self.spinbox_feedrate.grid(row=1, column=0)
        self.spinbox_stepsize.grid(row=1, column=1)

        # Joystick
        self.labelframe_direction = ttk.Labelframe(
            master=self.master, text="Por direção"
        )
        self.labelframe_direction.pack(anchor="w")

        self.button_y_up = ttk.Button(
            master=self.labelframe_direction,
            text="Y +",
            command=lambda: self.__move_joystick(
                axis="Y",
                direction=1,
                feedrate=self.controller.w_feed_rate.get(),
                step=self.controller.w_step_size.get(),
            ),
        )
        self.button_y_down = ttk.Button(
            master=self.labelframe_direction,
            text="Y -",
            command=lambda: self.__move_joystick(
                axis="Y",
                direction=0,
                feedrate=self.controller.w_feed_rate.get(),
                step=self.controller.w_step_size.get(),
            ),
        )
        self.button_x_up = ttk.Button(
            master=self.labelframe_direction,
            text="X +",
            command=lambda: self.__move_joystick(
                axis="X",
                direction=1,
                feedrate=self.controller.w_feed_rate.get(),
                step=self.controller.w_step_size.get(),
            ),
        )
        self.button_x_down = ttk.Button(
            master=self.labelframe_direction,
            text="X -",
            command=lambda: self.__move_joystick(
                axis="X",
                direction=0,
                feedrate=self.controller.w_feed_rate.get(),
                step=self.controller.w_step_size.get(),
            ),
        )
        self.button_z_up = ttk.Button(
            master=self.labelframe_direction,
            text="Z +",
            command=lambda: self.__move_joystick(
                axis="Z",
                direction=1,
                feedrate=self.controller.w_feed_rate.get(),
                step=self.controller.w_step_size.get(),
            ),
        )
        self.button_z_down = ttk.Button(
            master=self.labelframe_direction,
            text="Z -",
            command=lambda: self.__move_joystick(
                axis="Z",
                direction=0,
                feedrate=self.controller.w_feed_rate.get(),
                step=self.controller.w_step_size.get(),
            ),
        )

        self.button_y_up.grid(row=0, column=1)
        self.button_y_down.grid(row=2, column=1)
        self.button_x_up.grid(row=1, column=2)
        self.button_x_down.grid(row=1, column=0)
        self.button_z_up.grid(row=0, column=2)
        self.button_z_down.grid(row=2, column=2)

        # By coordenate
        self.labelframe_coord = ttk.Labelframe(
            master=self.master, text="Por coordenada"
        )
        self.labelframe_coord.pack(anchor="w")

        var_x_coord = tk.DoubleVar(master=self.labelframe_coord, value=0)
        var_y_coord = tk.DoubleVar(master=self.labelframe_coord, value=0)
        var_z_coord = tk.DoubleVar(master=self.labelframe_coord, value=0)

        self.label_x = ttk.Label(master=self.labelframe_coord, text="X:")
        self.label_y = ttk.Label(master=self.labelframe_coord, text="Y:")
        self.label_z = ttk.Label(master=self.labelframe_coord, text="Z:")
        self.spinbox_x = tk.Spinbox(
            master=self.labelframe_coord,
            from_=0,
            to=999999,
            format="%.2f",
            increment=0.1,
            textvariable=var_x_coord,
        )
        self.spinbox_y = tk.Spinbox(
            master=self.labelframe_coord,
            from_=0,
            to=999999,
            format="%.2f",
            increment=0.1,
            textvariable=var_y_coord,
        )
        self.spinbox_z = tk.Spinbox(
            master=self.labelframe_coord,
            from_=0,
            to=999999,
            format="%.2f",
            increment=0.1,
            textvariable=var_z_coord,
        )

        self.label_x.grid(row=0, column=0)
        self.spinbox_x.grid(row=0, column=1)
        self.label_y.grid(row=1, column=0)
        self.spinbox_y.grid(row=1, column=1)
        self.label_z.grid(row=2, column=0)
        self.spinbox_z.grid(row=2, column=1)

        # Controller
        self.controller.w_feed_rate = self.spinbox_feedrate
        self.controller.w_step_size = self.spinbox_stepsize
        self.controller.w_x_coord = self.spinbox_x
        self.controller.w_y_coord = self.spinbox_y
        self.controller.w_z_coord = self.spinbox_z

    def __move_joystick(self, axis: str, direction: int, feedrate: int, step: float):
        axis = axis.upper()
        if direction == 1:
            direction = ""
        else:
            direction = "-"
        feedrate = str(feedrate)
        step = str(step)
        command = "$J=G21G91" + axis + direction + step + "F" + feedrate + "\n"
        self.ser.write(str.encode(command))
        self.ser.readline()

    def set_manual_coord(self):
        self.controller.feed_rate_set = self.spinbox_feedrate.get()
        self.controller.stepsize_set = self.spinbox_stepsize.get()
        self.controller.x_coord_set = self.spinbox_x.get()
        self.controller.y_coord_set = self.spinbox_y.get()
        self.controller.z_coord_set = self.spinbox_z.get()
