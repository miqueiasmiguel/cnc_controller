import re


EVENTS = [
    "new_coord",  # a coordenada atual foi atualizada
    "set_coord",  # quando a coordenada é definida pelas spinboxes
    "set_door",  # armazenar as dimensões da porta e o caminho dos desenhos gcode
    "machine_busy",  # a máquina ficou ocupada
    "machine_free",  # a máquina ficoou livre
]

STATUSPAT = re.compile(
    r"^<(\w+)\|MPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*)\|FS:([+\-]?\d*\.?\d*),([+\-]?\d*\.?\d*)\|(WCO:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*))?(Ov:([+\-]?\d*\.?\d*),([+\-]?\d*\.?\d*),([+\-]?\d*\.?\d*))?>"
)
GCODEPAT = re.compile(
    r"(?i)^[gG0-9]{1,3}(?:\s+x-?(?P<x>[0-9.]{1,15})|\s+y-?(?P<y>[0-9.]{1,15})|\s+z-?(?P<z>[0-9.]{1,15}))*"
)
GCODEPAT2 = re.compile(
    r"(?i)(?:X(?P<x>[+\-]?\d*\.?\d*))?\s?(?:Y(?P<y>[+\-]?\d*\.?\d*))?\s?(?:Z(?P<z>[+\-]?\d*\.?\d*))?"
)
