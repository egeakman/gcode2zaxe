import contextlib
import os
import json
import zipfile
import hashlib
import tempfile
import datetime

TMP = tempfile.gettempdir()


def create_zaxe(zaxepath, tmp_gcode, snapshot, infopath):
    with zipfile.ZipFile(zaxepath, "w", zipfile.ZIP_DEFLATED) as f:
        f.write(tmp_gcode, "data.zaxe_code")
        f.write(snapshot, "snapshot.png")
        f.write(infopath, "info.json")


def convert_to_bytes(value):
    with open(value, "rb") as f:
        return f.read()


def md5(tmp_gcode):
    hash_md5 = hashlib.md5()
    with open(tmp_gcode, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def read_gcode(gcode):
    gcode_info = {}
    with open(gcode, "r") as f:
        for line in f.readlines():
            if line.startswith(";TIME:"):
                time = int(line.split(";TIME:")[1].strip())
                gcode_info["time"] = str(datetime.timedelta(seconds=time))

    with open(gcode, "r") as f:
        for line in f.readlines():
            if line.startswith(";Filament used:"):
                filament_used = round(
                    float(line.split(";Filament used:")[1].strip().replace("m", "")), 2
                )
                gcode_info["filament_used"] = float(filament_used) * 1000

        return gcode_info


def write_tmps(gcode, tmp_gcode, snapshot):
    encoded = convert_to_bytes(gcode)

    with open(tmp_gcode, "wb") as f:
        f.write(encoded)

    open(snapshot, "w").close()
    

def make_info(infopath, filament_type, nozzle_diameter, gcode, model, tmp_gcode, name):
    with open(infopath, "w") as f:
        f.write(json.dumps({
        "material": filament_type,
        "nozzle_diameter": nozzle_diameter,
        "filament_used": read_gcode(gcode)["filament_used"]
        if "filament_used" in read_gcode(gcode)
        else 0,
        "model": model,
        "checksum": md5(tmp_gcode),
        "name": name.split("/")[-1]
        if name.split("/")[-1] != name
        else name.split("\\")[-1],
        "duration": read_gcode(gcode)["time"]
        if "time" in read_gcode(gcode)
        else "00:00:00",
        "extruder_temperature": 210 if filament_type == "zaxe_pla" else 240,
        "bed_temperature": 60 if filament_type == "zaxe_pla" else 80,
        "version": "2.0.0",
    }))


def cleanup(tmp_gcode, infopath, snapshot):
    with contextlib.suppress(FileNotFoundError):
        os.remove(tmp_gcode)
        os.remove(infopath)
        os.remove(snapshot)
