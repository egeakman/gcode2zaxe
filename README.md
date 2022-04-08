# gcode2zaxe

A CLI application that converts gcode files to Zaxe print-ready files. You can use it from the command line after installing it. The executable name is `g2z`. **Don't forget to star the project on [GitHub](https://github.com/egeakman/gcode2zaxe).**

## Installation

Run:&nbsp; ``python -m pip install --upgrade gcode2zaxe``

## Usage

* Show help: ``g2z -h``

* Convert gcode file to zaxe file: ``g2z -g <gcode_file_path>``

## Optional Parameters

* ``-n, --name:`` Output file base name. Defaults to the gcode file name -> (``-g <gcode_file_path>``).

* ``-f, --filament:`` Filament type. Defaults to ``zaxe_pla``. Materials mostly start with ``zaxe_``.

* ``-d, --nozzle_diameter:`` Nozzle diameter. Defaults to ``0.4``.

* ``-m, --model:`` Zaxe printer model. Defaults to ``X1``. See available models in the [models list](https://github.com/egeakman/gcode2zaxe/blob/master/resources/models.json).

## Contributing

* If you have any suggestions or found any bugs, please open an issue or create a pull request.

* Don't hesitate to open an issue if you have any questions about the code.

## Footnotes

* This application does not guarantee that the output file will be valid or compatible with the printer.

* Use at your own risk. I take no responsibility for any damage to your printer.

* This application has no affiliation with Zaxe or its affiliates.

* This project is licensed under the [AGPLv3 license](https://raw.githubusercontent.com/egeakman/gcode2zaxe/master/LICENSE).
