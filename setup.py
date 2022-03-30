import contextlib
import json
import urllib.request
from setuptools import setup, find_packages


def latest_version(package_name):
    url = f"https://pypi.python.org/pypi/{package_name}/json"
    with contextlib.suppress(Exception):
        response = urllib.request.urlopen(urllib.request.Request(url), timeout=1)
        data = json.load(response)
        versions = data["releases"].keys()
        versions = sorted(versions)
        return f">={versions[-1]}"
    return ""


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gcode2zaxe",
    author="Ege Akman",
    author_email="egeakmanegeakman@hotmail.com",
    url="https://github.com/egeakman/gcode2zaxe",
    description="Gcode to Zaxe Converter | executable: g2z",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="2022.3.30",
    license="AGPLv3",
    download_url="https://github.com/egeakman/gcode2zaxe/archive/2022.3.30.tar.gz",
    packages=find_packages(where=".", exclude=["tests"]),
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "g2z=gcode2zaxe.convert:main",
        ]
    },
    install_requires=[
        f"setuptools{latest_version('setuptools')}",
    ],
    keywords=[
        "3D",
        "gcode",
        "Zaxe",
        "converter",
        "gcode2zaxe",
        "slicer",
        "model",
        "reverse engineering",
    ],
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    project_urls={
        "Homepage": "https://github.com/egeakman/gcode2zaxe",
        "Issues": "https://github.com/egeakman/gcode2zaxe/issues",
    },
)
