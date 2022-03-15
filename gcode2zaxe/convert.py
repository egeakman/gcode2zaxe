import os
import json
import zipfile
import hashlib
import tempfile
from argparse import ArgumentParser

TMP = tempfile.gettempdir()

parser = ArgumentParser()
parser.add_argument("-g", "--gcode", help="gcode file to convert", required=True)
parser.add_argument(
    "-n", "--name", help="name of the model", required=False, default=None
)
parser.add_argument(
    "-o", "--output", help="output folder", required=False, default=os.getcwd()
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

if args.name is None:
    args.name = args.gcode

if args.output is os.getcwd():
    zaxepath = f"./{args.name}.zaxe"

else:
    zaxepath = f"{args.output}/{args.name}.zaxe"


def create_zaxe():
    with zipfile.ZipFile(zaxepath, "w", zipfile.ZIP_DEFLATED) as f:
        f.write(args.gcode, "data.zaxe_code")
        f.write(snapshot, "snapshot.png")
        f.write(infopath, "info.json")


def convert_to_bytes(value):
    with open(value, "rb") as f:
        return f.read()


def md5():
    hash_md5 = hashlib.md5()
    with open(os.path.join(TMP, "o.gcode"), "wb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def main():
    with open(os.path.join(TMP, "info.json"), "w") as f:
        f.write(json.dumps(info))

    encoded = convert_to_bytes(args.gcode)

    with open(os.path.join(TMP, "o.gcode"), "w") as f:
        f.write(encoded)

    open(os.path.join(TMP, "snapshot.png"), "w").close()

    create_zaxe()


info = {
    "material": args.filament,
    "nozzle_diameter": args.nozzle_diameter,
    "filament_used": 1000.0,
    "model": args.model,
    "checksum": md5(),
    "name": args.name,
    "duration": "00:20:00",
    "extruder_temperature": 220,
    "bed_temperature": 60,
    "version": "1.0.4",
}
