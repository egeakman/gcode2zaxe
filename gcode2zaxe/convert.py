import contextlib
import os
import json
import zipfile
import hashlib
import tempfile
import datetime
from argparse import ArgumentParser

TMP = tempfile.gettempdir()

parser = ArgumentParser()
parser.add_argument("-g", "--gcode", help="gcode file to convert", required=True)
parser.add_argument(
    "-n", "--name", help="name of the output file", required=False, default=None
)
parser.add_argument(
    "-f",
    "--filament",
    help='filament type | mostly starts with "zaxe_" e.g. "zaxe_pla"',
    required=False,
    default="zaxe_pla",
)
parser.add_argument(
    "-d", "--nozzle_diameter", help="nozzle diameter", required=False, default=0.4
)
parser.add_argument(
    "-m", "--model", help="model of the printer", required=False, default="X1"
)
args = parser.parse_args()

snapshot = os.path.join(TMP, "snapshot.png")
infopath = os.path.join(TMP, "info.json")
tmp_gcode = os.path.join(TMP, "o.gcode")
args.name = (
    args.gcode
    if args.name is None
    else os.path.join(os.path.dirname(args.gcode), args.name)
)
zaxepath = f"{args.name}.zaxe"


def create_zaxe():
    with zipfile.ZipFile(zaxepath, "w", zipfile.ZIP_DEFLATED) as f:
        f.write(tmp_gcode, "data.zaxe_code")
        f.write(snapshot, "snapshot.png")
        f.write(infopath, "info.json")


def convert_to_bytes(value):
    with open(value, "rb") as f:
        return f.read()


def md5():
    hash_md5 = hashlib.md5()
    with open(tmp_gcode, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def read_gcode():
    gcode_info = {}
    with open(args.gcode, "r") as f:
        for line in f.readlines():
            if line.startswith(";TIME:"):
                time = int(line.split(";TIME:")[1].strip())
                gcode_info["time"] = str(datetime.timedelta(seconds=time))

    with open(args.gcode, "r") as f:
        for line in f.readlines():
            if line.startswith(";Filament used:"):
                filament_used = round(
                    float(line.split(";Filament used:")[1].strip().replace("m", "")), 2
                )
                gcode_info["filament_used"] = float(filament_used) * 1000

        return gcode_info


def make_info():
    material = args.filament.lower()

    return {
        "material": material,
        "nozzle_diameter": args.nozzle_diameter,
        "filament_used": read_gcode()["filament_used"]
        if "filament_used" in read_gcode()
        else 0,
        "model": args.model,
        "checksum": md5(),
        "name": args.name.split("/")[-1]
        if args.name.split("/")[-1] != args.name
        else args.name.split("\\")[-1],
        "duration": read_gcode()["time"] if "time" in read_gcode() else "00:00:00",
        "extruder_temperature": 210 if material == "zaxe_pla" else 240,
        "bed_temperature": 60 if material == "zaxe_pla" else 80,
        "version": "2.0.0",
    }


def cleanup():
    with contextlib.suppress(FileNotFoundError):
        os.remove(tmp_gcode)
        os.remove(infopath)
        os.remove(snapshot)


def main():

    encoded = convert_to_bytes(args.gcode)

    with open(tmp_gcode, "wb") as f:
        f.write(encoded)

    with open(infopath, "w") as f:
        f.write(json.dumps(make_info()))

    open(snapshot, "w").close()
    create_zaxe()
    cleanup()
