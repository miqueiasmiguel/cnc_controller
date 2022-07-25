import os
import time
from typing import Type
import tkinter as tk
from tkinter import ttk
import serial
from controller import Controller
from file_handler import FileHandler


class MovementFrame(tk.Frame):
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
        self.file_handler = FileHandler()
        self.create_widgets()
        self.paused = 0

    def create_widgets(self):
        self.labelframe_movement = ttk.Labelframe(master=self.master, text="Movimento")
        self.labelframe_movement.pack(anchor="w")

        self.button_start = ttk.Button(
            master=self.labelframe_movement, text="Iniciar", command=self.__start
        )
        self.button_pause = ttk.Button(
            master=self.labelframe_movement, text="Pausar", command=self.__pause
        )
        self.button_stop = ttk.Button(
            master=self.labelframe_movement, text="Parar", command=self.__stop
        )

        self.button_start.grid(row=0, column=0)
        self.button_pause.grid(row=0, column=1)
        self.button_stop.grid(row=0, column=2)

    def __start(self):
        if self.controller.active_tab == 0:  # automático
            self.__start_auto()
        elif self.controller.active_tab == 1:  # manual
            self.__move_coord()
        elif self.controller.active_tab == 2:  # config
            pass

    def __start_auto(self):

        self.controller.dispatch(event="set_door")
        height = self.controller.door_height * 10  # transformando em mm
        width = self.controller.door_width * 10  # transformando em mm
        d = self.controller.door_d * 10  # distância da dobradiça em mm
        k = self.controller.door_k * 10  # distância da maçaneta em mm

        hinge_points = self.file_handler.decode_gcode(self.controller.door_hinge_path)
        knob_points = self.file_handler.decode_gcode(self.controller.door_knob_path)

        hinge_minmax = self.file_handler.get_min_max(hinge_points)
        knob_minmax = self.file_handler.get_min_max(knob_points)

        offset_h1_y = d
        offset_h2_y = height - 2 * d - hinge_minmax["y_max"] - hinge_minmax["y_min"]

        offset_k_x = width - k - knob_minmax["x_max"] - knob_minmax["x_min"]
        offset_k_y = (
            height / 2
            - d
            - hinge_minmax["y_max"]
            - hinge_minmax["y_min"]
            + (knob_minmax["y_max"] - knob_minmax["y_min"]) / 2
        )

        # define novo (0,0)
        print("Z H1")
        self.controller.scheduler.append([f"G10P0L20Y{-offset_h1_y}\n"])

        # 1° dobradiça
        print("H1")
        with open(self.controller.door_hinge_path, "r") as file:
            commands = []
            for line in file:
                line = self.file_handler.clear_comments(line)
                if not line.isspace() and len(line) > 0:
                    commands.append(line + "\n")
            self.controller.scheduler.append(commands)

        # espera até estar disponível
        while self.controller.status != "Idle":
            print("Ocupado")
            time.sleep(1)

        # define novo (0,0)
        print("Z H2")
        self.controller.scheduler.append([f"G10P0L20Y{-offset_h2_y}\n"])

        # vai para zero
        self.controller.scheduler.append([f"G90 G0 X0 Y0\n"])

        # 2° dobradiça
        print("H2")
        with open(self.controller.door_hinge_path, "r") as file:
            commands = []
            for line in file:
                line = self.file_handler.clear_comments(line)
                if not line.isspace() and len(line) > 0:
                    commands.append(line + "\n")
            self.controller.scheduler.append(commands)

        # espera até estar disponível
        while self.controller.status != "Idle":
            print("Ocupado")
            time.sleep(1)

        # define novo (0,0)
        print("Z M")
        self.controller.scheduler.append([f"G10P0L20X{-offset_k_x}Y{offset_k_y}\n"])

        # vai para zero
        self.controller.scheduler.append([f"G90 G0 X0 Y0\n"])

        # maçaneta
        print("M")
        with open(self.controller.door_knob_path, "r") as file:
            commands = []
            for line in file:
                line = self.file_handler.clear_comments(line)
                if not line.isspace() and len(line) > 0:
                    commands.append(line + "\n")
            self.controller.scheduler.append(commands)

        # espera até estar disponível
        while self.controller.status != "Idle":
            print("Ocupado")
            time.sleep(1)

        # define antigo (0,0)
        old_wco_y = height / 2 - (knob_minmax["y_max"] - knob_minmax["y_min"]) / 2
        old_wco_x = offset_k_x
        print("ZZ")
        self.controller.scheduler.append([f"G10P0L20X{old_wco_x}Y{old_wco_y}\n"])

        # retorna para antigo (0,0)
        self.controller.scheduler.append([f"G90 G0 X0 Y0\n"])

        """
        try:
            os.remove("temp/door1.gcode")
        except:
            pass

        # Processa a primeira dobradiça
        self.file_handler.modify_gcode(
            path=self.controller.door_hinge_path,
            new_path="door1.gcode",
            offset_x=0,
            offset_y=offset_h1_y,
            )
        
        # Processa a segunda dobradiça
        self.file_handler.modify_gcode(
            path=self.controller.door_hinge_path,
            new_path="door1.gcode",
            offset_x=0,
            offset_y=offset_h2_y,
        )

        # Processa o puxador
        self.file_handler.modify_gcode(
            path=self.controller.door_knob_path,
            new_path="door1.gcode",
            offset_x=offset_k_x,
            offset_y=offset_k_y,
        )

        # Executa gcode temporário
        with open("temp/door1.gcode", "r") as file:
            commands = []
            for line in file:
                line = self.file_handler.clear_comments(line)
                if not line.isspace() and len(line) > 0:
                    commands.append(line + "\n")
            self.controller.scheduler.append(commands)


        # Retorna para zero
        self.controller.scheduler.append(["G90 G0 X0 Y0"])
        """

    def __move_coord(self):
        self.controller.dispatch(event="set_coord")
        x_coord = str(self.controller.x_coord_set)
        y_coord = str(self.controller.y_coord_set)
        z_coord = str(self.controller.z_coord_set)
        feed_rate = str(self.controller.feed_rate_set)
        command = (
            "$J=G21G90"
            + "X"
            + x_coord
            + "Y"
            + y_coord
            + "Z"
            + z_coord
            + "F"
            + feed_rate
            + "\n"
        )
        self.ser.write(str.encode(command))
        self.ser.readline()

    def __pause(self):
        if self.paused == 0:
            self.ser.write(str.encode("!"))
            self.button_pause["text"] = "Retomar"
            self.paused = 1
        else:
            self.ser.write(str.encode("~"))
            self.button_pause["text"] = "Pausar"
            self.paused = 0

    def __stop(self):
        self.ser.write(str.encode("\x85"))
