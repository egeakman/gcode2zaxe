import os
import json
import tempfile
from gcode2zaxe import lib as g2z_lib
from styles import Styles
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QMessageBox,
    QWidget,
    QDoubleSpinBox,
    QLabel,
    QToolTip,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QHBoxLayout,
)


class ui_functions:
    @staticmethod
    def return_model_list():
        with open("resources.json", "r") as f:
            datastore = json.load(f)
        return list(datastore["models"])

    @staticmethod
    def return_filament_types():
        with open("resources.json", "r") as f:
            datastore = json.load(f)
        return list(datastore["materials"])


class ui_design(QWidget):
    def __init__(self, parent=None):
        super(ui_design, self).__init__(parent)

        QToolTip.setFont(QFont("SansSerif", 10))

        TMP = tempfile.gettempdir()

        self.snapshot = os.path.join(TMP, "snapshot.png")
        self.infopath = os.path.join(TMP, "info.json")
        self.tmp_gcode = os.path.join(TMP, "o.gcode")

        self.gcode_file_choosen = False
        self.output_dir = [""]
        self.environment = os.environ["HOMEPATH"]

        title_font_id = QFontDatabase.addApplicationFont("fonts/ZLK.ttf")
        input_font_id = QFontDatabase.addApplicationFont("fonts/asap_bold_italic.ttf")

        self.title = QLabel("GCode 2 Zaxe")
        self.title.setFont(
            QFont(QFontDatabase.applicationFontFamilies(title_font_id)[0], 80)
        )
        self.title.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.title.setStyleSheet(Styles.title_style)

        self.subtitle = QLabel("Made by Ege Akman and Arda Sak")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        self.subtitle.setStyleSheet(Styles.subtitle_style)

        self.gcode_input_label = QLabel("Gcode File:")
        self.gcode_input_label.setStyleSheet(Styles.input_label_style)
        self.gcode_input_label.setFont(
            QFont(QFontDatabase.applicationFontFamilies(input_font_id)[0], pointSize=20)
        )
        self.gcode_input_button = QPushButton("Choose file")
        self.gcode_input_button.setToolTip("Gcode file to convert")
        self.gcode_input_button.clicked.connect(self.choose_file)

        self.filament_type_label = QLabel("Filament Type:")
        self.filament_type_label.setStyleSheet(Styles.input_label_style)
        self.filament_type_label.setFont(
            QFont(QFontDatabase.applicationFontFamilies(input_font_id)[0], pointSize=20)
        )
        self.filament_type_input = QComboBox()
        self.filament_type_input.addItems(ui_functions.return_filament_types())

        self.model_input_label = QLabel("Printer Model:")
        self.model_input_label.setStyleSheet(Styles.input_label_style)
        self.model_input_label.setFont(
            QFont(QFontDatabase.applicationFontFamilies(input_font_id)[0], pointSize=20)
        )
        self.model_combobox = QComboBox()
        self.model_combobox.addItems(ui_functions.return_model_list())
        self.model_combobox.setToolTip("Model of the printer")

        self.spin_box_label = QLabel("Nozzle Diameter:")
        self.spin_box_label.setStyleSheet(Styles.input_label_style)
        self.spin_box_label.setFont(
            QFont(QFontDatabase.applicationFontFamilies(input_font_id)[0], pointSize=20)
        )
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setSingleStep(0.05)
        self.spin_box.setValue(0.4)
        self.spin_box.setMinimum(0)
        self.spin_box.setToolTip("Nozzle Diameter")
        self.spin_box.setDecimals(3)

        self.output_name_input_label = QLabel("Output Directory:")
        self.output_name_input_label.setStyleSheet(Styles.input_label_style)
        self.output_name_input_label.setFont(
            QFont(QFontDatabase.applicationFontFamilies(input_font_id)[0], pointSize=20)
        )
        self.output_name_input = QPushButton("Save as")
        self.output_name_input.setToolTip("Output file path and name | Required")
        self.output_name_input.clicked.connect(self.saveas)
        self.output_name_icon = QLabel()
        self.output_name_icon.setVisible(False)
        self.output_name_icon.setPixmap(QPixmap("icons/accept.png"))
        self.output_name_icon.setStyleSheet(Styles.input_label_style)

        self.convert_button = QPushButton("Convert")
        self.convert_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.convert_button.clicked.connect(self.convert)

        self.upper_placement()
        self.center_placement()
        self.bottom_placement()
        self.main_placement()

        self.setLayout(self.main_hbox)

    def main_placement(self):
        self.main_hbox = QHBoxLayout()
        self.main_hbox.addStretch()
        self.main_hbox.addLayout(self.main_vbox())
        self.main_hbox.addStretch()

    def saveas(self):
        self.output_dir = QFileDialog.getSaveFileName(
            self, "Save as", self.environment + "\Downloads", "Zaxe (*.zaxe)"
        )
        if self.output_dir[0] != "":
            self.output_name_icon.setVisible(True)
        else:
            self.output_name_icon.setVisible(False)

    def choose_file(self):
        if self.gcode_file_choosen:
            self.dir = ""
            self.gcode_input_button.setText("Choose file")
            self.gcode_file_choosen = False
        else:
            self.dir = QFileDialog.getOpenFileName(
                self,
                "Choose gcode file",
                self.environment + "\Downloads",
                "Gcode (*.gcode)",
            )
            if self.is_file_valid():
                self.gcode_file_choosen = True
                self.gcode_input_button.setText("Chosen")

    def get_file_name(self):
        return self.dir[0].split("/")[-1].split(".")[0]

    def is_file_valid(self):
        file = self.dir[0].split("/")[-1].split(".")[-1]
        return file.lower() == "gcode"

    def main_vbox(self):
        main_vbox = QVBoxLayout()

        main_vbox.addLayout(self.title_upper_vbox)
        main_vbox.addStretch()
        main_vbox.addLayout(self.center_vbox)
        main_vbox.addStretch()
        main_vbox.addLayout(self.bottom_hbox)
        return main_vbox

    def upper_placement(self):
        self.title_upper_vbox = QVBoxLayout()
        self.title_upper_vbox.addWidget(self.title)
        self.title_upper_vbox.addStretch()

    def center_placement(self):
        self.center_vbox = QVBoxLayout()
        self.center_vbox.setContentsMargins(0, 0, 0, 200)

        self.gcode_hbox = QHBoxLayout()
        self.gcode_hbox.addStretch()
        self.gcode_hbox.addWidget(self.gcode_input_label)
        self.gcode_hbox.addWidget(self.gcode_input_button)
        self.gcode_hbox.addStretch()

        self.model_hbox = QHBoxLayout()
        self.model_hbox.addStretch()
        self.model_hbox.addWidget(self.model_input_label)
        self.model_hbox.addWidget(self.model_combobox)
        self.model_hbox.addStretch()

        self.nozzle_hbox = QHBoxLayout()
        self.nozzle_hbox.addStretch()
        self.nozzle_hbox.addWidget(self.spin_box_label)
        self.nozzle_hbox.addWidget(self.spin_box)
        self.nozzle_hbox.addStretch()

        self.filament_hbox = QHBoxLayout()
        self.filament_hbox.addStretch()
        self.filament_hbox.addWidget(self.filament_type_label)
        self.filament_hbox.addWidget(self.filament_type_input)
        self.filament_hbox.addStretch()

        self.name_hbox = QHBoxLayout()
        self.name_hbox.addStretch()
        self.name_hbox.addWidget(self.output_name_input_label)
        self.name_hbox.addWidget(self.output_name_input)
        self.name_hbox.addWidget(self.output_name_icon)
        self.name_hbox.addStretch()

        self.center_vbox.addLayout(self.gcode_hbox)
        self.center_vbox.addLayout(self.model_hbox)
        self.center_vbox.addLayout(self.nozzle_hbox)
        self.center_vbox.addLayout(self.filament_hbox)
        self.center_vbox.addLayout(self.name_hbox)
        self.center_vbox.addWidget(self.convert_button)

    def bottom_placement(self):
        self.bottom_hbox = QHBoxLayout()
        self.bottom_hbox.addStretch()
        self.bottom_hbox.addWidget(self.subtitle)

    def convert(self):
        with open("resources.json", "r") as f:
            datastore = json.load(f)
        if self.is_convertable():

            try:
                g2z_lib.write_tmps(
                    self.dir[0],
                    self.tmp_gcode,
                    self.snapshot,
                )
                g2z_lib.make_info(
                    self.infopath,
                    datastore["materials"][self.filament_type_input.currentText()],
                    self.spin_box.value(),
                    self.dir[0],
                    datastore["models"][self.model_combobox.currentText()],
                    self.tmp_gcode,
                    self.output_dir[0],
                ),
                g2z_lib.create_zaxe(
                    self.output_dir[0], self.tmp_gcode, self.snapshot, self.infopath
                )
                g2z_lib.cleanup(self.tmp_gcode, self.infopath, self.snapshot)

                self.message_box(
                    msg="Converted successfully.",
                    buttons=QMessageBox.StandardButton.Ok,
                    title="Success!",
                    icon=QMessageBox.Icon.Information,
                )
            except Exception:
                self.message_box(
                    "An unknown error occured. Please try again.",
                    buttons=QMessageBox.StandardButton.Ok,
                    title="Error",
                )

    def is_convertable(self):
        if self.gcode_file_choosen:
            if self.output_dir[0] != "":
                return True
            else:
                self.message_box(
                    msg="You have to choose an output directory first.",
                    buttons=QMessageBox.StandardButton.Ok,
                    title="Error",
                )
        else:
            self.message_box(
                msg="You have to choose a gcode file first.",
                buttons=QMessageBox.StandardButton.Ok,
                title="Error",
            )

    def message_box(self, msg, buttons, icon=QMessageBox.Icon.Critical, title=None):
        message = QMessageBox(self)
        message.setIcon(icon)
        message.setStandardButtons(buttons)
        message.setWindowTitle(title)
        message.setText(msg)
        return message.exec()
