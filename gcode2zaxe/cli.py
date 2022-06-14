import tempfile
import os
import json
from argparse import ArgumentParser
from gcode2zaxe import lib

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


def main():
    encoded = lib.convert_to_bytes(args.gcode)

    with open(tmp_gcode, "wb") as f:
        f.write(encoded)

    with open(infopath, "w") as f:
        f.write(
            json.dumps(
                lib.make_info(
                    args.filament,
                    args.nozzle_diameter,
                    args.gcode,
                    args.model,
                    tmp_gcode,
                    args.name,
                )
            )
        )

    open(snapshot, "w").close()
    lib.create_zaxe(zaxepath, tmp_gcode, snapshot, infopath)
    lib.cleanup(tmp_gcode, infopath, snapshot)
