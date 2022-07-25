import threading
import time
import serial
import serial.tools.list_ports
from typing import Type
import tkinter as tk
from tkinter import ttk
from controller import Controller


class SerialFrame(tk.Frame):
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
            event="machine_free", observer=self, callback=self.run_scheduler_commands
        )
        self.baud_rates = [
            "2400",
            "4800",
            "9600",
            "19200",
            "38400",
            "57600",
            "115200",
            "230400",
            "250000",
        ]
        self.port_names = [port.name for port in serial.tools.list_ports.comports()]
        self.create_widgets()

        self.close_flag = False

    def create_widgets(self):
        self.labelframe_serial = ttk.LabelFrame(master=self.master, text="Serial")
        self.label_port = ttk.Label(master=self.labelframe_serial, text="Porta:")
        self.label_baudrate = ttk.Label(
            master=self.labelframe_serial, text="Baud rate:"
        )
        self.combobox_port = ttk.Combobox(
            master=self.labelframe_serial,
            values=self.port_names,
            state="readonly",
            width=9,
        )
        self.combobox_baudrate = ttk.Combobox(
            master=self.labelframe_serial,
            values=self.baud_rates,
            state="readonly",
            width=9,
        )
        self.button_refresh = ttk.Button(
            master=self.labelframe_serial, text="Atualizar", command=self.__port_refresh
        )
        self.button_connect = ttk.Button(
            master=self.labelframe_serial,
            text="Conectar",
            command=self.__serial_connect,
        )

        self.labelframe_serial.pack(anchor="w")
        self.label_port.grid(row=0, column=0, sticky=tk.W)
        self.label_baudrate.grid(row=0, column=1, sticky=tk.W)
        self.combobox_port.grid(row=1, column=0)
        self.combobox_baudrate.grid(row=1, column=1)
        self.button_refresh.grid(row=2, column=0)
        self.button_connect.grid(row=2, column=1)

        self.combobox_baudrate.current(6)
        if self.port_names:
            self.combobox_port.current(0)

    def __port_refresh(self):
        self.combobox_port["values"] = [
            port.name for port in serial.tools.list_ports.comports()
        ]

    def __serial_connect(self):
        self.port_name = self.combobox_port.get()
        self.baud_rate = self.combobox_baudrate.get()
        self.ser.port = self.port_name
        self.ser.baudrate = self.baud_rate
        # self.ser.timeout = 5

        if not self.ser.isOpen():
            try:
                self.close_flag = False
                self.ser.open()
                self.button_connect["text"] = "Desconectar"
                self.__disable_widgets()
                print("Conectado")
                self.print_state()
            except Exception as e:
                print(e)
        else:
            try:
                self.close_flag = True
                self.ser.close()
                self.button_connect["text"] = "Conectar"
                self.combobox_port["state"] = tk.NORMAL
                self.combobox_baudrate["state"] = tk.NORMAL
                print("Desconectado")
            except Exception as e:
                print(e)

    def __disable_widgets(self):
        self.button_connect["state"] = tk.DISABLED
        self.button_refresh["state"] = tk.DISABLED
        self.combobox_baudrate["state"] = tk.DISABLED
        self.combobox_port["state"] = tk.DISABLED
        self.master.after(1700, self.__activate_widgets)

    def __activate_widgets(self):
        self.button_connect["state"] = tk.NORMAL
        self.button_refresh["state"] = tk.NORMAL

    def print_state(self):
        def status_report():
            while not self.close_flag:
                if self.controller.status == "Idle":
                    self.controller.busy = False
                else:
                    self.controller.busy = True
                if self.ser.is_open and self.ser.out_waiting == 0:
                    self.ser.write(str.encode("?"))
                    status = self.ser.readline()
                    print(status)
                    self.controller.decode_status(string=status)
                time.sleep(0.2)

        threading.Thread(target=status_report).start()

    def run_scheduler_commands(self):
        if self.controller.scheduler != []:
            time.sleep(1)
            commands = self.controller.scheduler.pop(0)
            for command in commands:
                encoded_command = str.encode(command)
                print(encoded_command)
                self.ser.write(encoded_command)
                response = self.ser.readline()
                print(response)
                time.sleep(0.5)
