import re
import os
from setup import GCODEPAT, GCODEPAT2


class FileHandler:
    def __init__(self):
        pass

    def clear_comments(self, line: str) -> str:
        line = line.replace(line[line.find("(") : line.find(")") + 1], "").strip()
        line = line.rstrip("\n")
        if line.find(";") != -1:
            line = line[: line.index(";")]
        if line.find("%") != -1:
            line = line.replace("%", "")

        return line

    def decode_gcode(self, path: str) -> list[tuple]:
        """Função utilizada para transformar um script GCODE em
        uma lista contendo os pontos
        """
        points = []
        old_x = 0
        old_y = 0
        old_z = 0
        new_x = 0
        new_y = 0
        new_z = 0
        match = None
        with open(path, "r") as file:
            for line in file:
                line = self.clear_comments(line)

                if len(line) == 0:
                    continue
                elif line[0] == "G":
                    match = GCODEPAT.match(line)
                elif line[0] in ["X", "Y", "Z"]:
                    match = GCODEPAT2.match(line)
                else:
                    match = None

                if match:
                    new_x = match["x"]
                    new_y = match["y"]
                    new_z = match["z"]

                    if new_x == None:
                        new_x = old_x
                    if new_y == None:
                        new_y = old_y
                    if new_z == None:
                        new_z = old_z

                    points.append((new_x, new_y, new_z))

                old_x = new_x
                old_y = new_y
                old_z = new_z

        return points

    def get_min_max(self, points: list[tuple]) -> dict:
        """Dado uma lista, recupera os máximos e mínimos e os armazena em um dicionário"""
        min_max = {}
        min_max["x_min"] = 0
        min_max["x_max"] = 0
        min_max["y_min"] = 0
        min_max["y_max"] = 0

        for point in points:
            point = list(point)
            point.pop(-1)
            point = tuple(point)

            x, y = point
            if float(x) > min_max["x_max"]:
                min_max["x_max"] = float(x)
            if float(y) > min_max["y_max"]:
                min_max["y_max"] = float(y)
            if float(x) < min_max["x_min"]:
                min_max["x_min"] = float(x)
            if float(y) < min_max["y_min"]:
                min_max["y_min"] = float(y)

        return min_max

    def plot_door(
        self,
        hinge_path: str,
        knob_path: str,
        height: float,
        width: float,
        d: float,
        k: float,
    ) -> None:
        hinge_points = self.decode_gcode(hinge_path)
        knob_points = self.decode_gcode(knob_path)

        hinge_minmax = self.get_min_max(hinge_points)
        knob_minmax = self.get_min_max(knob_points)

        offset_h1_y = d
        offset_h2_y = (
            height - d - hinge_minmax["y_max"] / 10 - hinge_minmax["y_min"] / 10
        )

        offset_k_x = width - k - knob_minmax["x_max"] / 10 - knob_minmax["x_min"] / 10
        offset_k_y = (
            height / 2 - (knob_minmax["y_max"] / 10 - knob_minmax["y_min"] / 10) / 2
        )

        import turtle as t

        canvas = t.Screen()
        t.TurtleScreen._RUNNING = True
        zero_abs = (-100, -100)
        zero_abs_x, zero_abs_y = zero_abs

        # vai para zero
        t.penup()
        t.goto(zero_abs)

        # gera a porta
        zero = (zero_abs_x, zero_abs_y)
        zero_x, zero_y = zero
        t.goto(zero)
        t.pendown()
        t.goto(0 + zero_x, height + zero_y)
        t.goto(width + zero_x, height + zero_y)
        t.goto(width + zero_x, 0 + zero_y)
        t.goto(zero)
        t.penup()

        # gera hinge 1
        zero = (zero_abs_x + 0, zero_abs_y + offset_h1_y)
        zero_x, zero_y = zero
        t.goto(zero_x, zero_y)
        t.pendown()
        for point in hinge_points:
            x, y, z = point
            t.goto(float(x) / 10 + zero_x, float(y) / 10 + zero_y)
        t.penup()

        # gera hinge 2
        zero = (zero_abs_x + 0, zero_abs_x + offset_h2_y)
        zero_x, zero_y = zero
        t.goto(zero_x, zero_y)
        t.pendown()
        for point in hinge_points:
            x, y, z = point
            t.goto(float(x) / 10 + zero_x, float(y) / 10 + zero_y)
        t.penup()

        # gera knob
        zero = (zero_abs_x + offset_k_x, zero_abs_y + offset_k_y)
        zero_x, zero_y = zero
        t.goto(zero_x, zero_y)
        t.pendown()
        for point in knob_points:
            x, y, z = point
            t.goto(float(x) / 10 + zero_x, float(y) / 10 + zero_y)
        t.penup()

        t.done()
        canvas.exitonclick()

    def move_gcode(self, path: str, x: float, y: float, z: float):
        """Desloca o desenho em um offset pre-definido"""

        points = self.decode_gcode(path)

        for point in points:
            old_x, old_y, old_z = point
            new_x = old_x + x
            new_y = old_y + y
            new_z = old_z + z
            point = (new_x, new_y, new_z)

        return points

    def offset_coord(self, string: str, offset_x: float, offset_y: float) -> str:
        """Retorna a linha com um offset"""
        for axis in ["X", "I"]:
            COORDPAT = re.compile(r"{}[+\-]?\d+\.?\d*".format(axis))
            if COORDPAT.search(string):
                coord = COORDPAT.search(string).group()
                new_value = round(float(coord.replace(axis, "")) + offset_x, 5)
                new_coord = axis + str(new_value)
                new_string = COORDPAT.sub(new_coord, string)
            else:
                new_string = string
            string = new_string

        for axis in ["Y", "J"]:
            COORDPAT = re.compile(r"{}[+\-]?\d+\.?\d*".format(axis))
            if COORDPAT.search(string):
                coord = COORDPAT.search(string).group()
                new_value = round(float(coord.replace(axis, "")) + offset_y, 5)
                new_coord = axis + str(new_value)
                new_string = COORDPAT.sub(new_coord, string)
            else:
                new_string = string
            string = new_string
        return new_string

    def modify_gcode(self, path: str, new_path: str, offset_x: float, offset_y: float):
        """Lê o arquivo desejado, aplica o offset e salva em outro arquivo temporário"""

        filename, extension = os.path.splitext(os.path.basename(new_path))
        temp_path = "temp/" + filename + extension

        with open(path, "r") as original_file:
            with open(temp_path, "a+") as temp_file:
                while True:
                    eof = temp_file.read()
                    if eof == "":
                        temp_file.write("\n")
                        for line in original_file:
                            if line[0] == "M":
                                continue
                            temp_file.write(
                                self.offset_coord(
                                    string=line, offset_x=offset_x, offset_y=offset_y
                                )
                            )
                        break

        return temp_path
