# coding=utf-8
"""
Created on 26.2.2018
Updated on 12.6.2018

Potku is a graphical user interface for analyzation and
visualization of measurement data collected from a ToF-ERD
telescope. For physics calculations Potku uses external
analyzation components.
Copyright (C) 2013-2018 Jarkko Aalto, Severi Jääskeläinen, Samuel Kaiponen,
Timo Konu, Samuli Kärkkäinen, Samuli Rahkonen, Miika Raunio, Heta Rekilä and
Sinikka Siironen

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (file named 'LICENCE').
"""
__author__ = "Severi Jääskeläinen \n Samuel Kaiponen \n Heta Rekilä " \
             "\n Sinikka Siironen"
__version__ = "2.0"

import os

import widgets.input_validation as iv

from PyQt5 import uic
from PyQt5 import QtWidgets

from dialogs.new_sample import NewSampleDialog
from dialogs.file_dialogs import open_file_dialog


class LoadMeasurementDialog(QtWidgets.QDialog):
    """Dialog for loading a measurement.
    """
    def __init__(self, samples, directory):
        """Inits a load measurement dialog.

        Args:
            samples: Samples of request.
            directory: Directory where to open the file browser.
        """
        super().__init__()

        self.ui = uic.loadUi(os.path.join(
            "ui_files", "ui_new_measurement.ui"), self)

        self.ui.browseButton.clicked.connect(self.__browse_files)
        self.ui.addSampleButton.clicked.connect(self.__add_sample)
        self.ui.loadButton.clicked.connect(self.__load_measurement)
        self.ui.cancelButton.clicked.connect(self.close)
        self.name = ""
        self.sample = None
        self.directory = directory
        self.filename = ""
        self.samples = samples

        self.__close = True
        for sample in samples:
            self.ui.samplesComboBox.addItem(
                "Sample " + "%02d" % sample.serial_number + " " + sample.name)

        if not samples:
            iv.set_input_field_red(self.ui.samplesComboBox)

        iv.set_input_field_red(self.ui.nameLineEdit)
        self.ui.nameLineEdit.textChanged.connect(lambda: self.__check_text(
            self.ui.nameLineEdit))

        iv.set_input_field_red(self.ui.pathLineEdit)
        self.ui.pathLineEdit.textChanged.connect(lambda: self.__check_text(
            self.ui.pathLineEdit))

        self.nameLineEdit.textEdited.connect(
            lambda: iv.sanitize_file_name(self.nameLineEdit))

        self.exec_()

    def __add_sample(self):
        dialog = NewSampleDialog(self.samples)
        if dialog.name:
            self.ui.samplesComboBox.addItem(dialog.name)
            self.ui.samplesComboBox.setCurrentIndex(
                self.ui.samplesComboBox.findText(dialog.name))
            iv.set_input_field_white(self.ui.samplesComboBox)

    def __load_measurement(self):
        self.path = self.ui.pathLineEdit.text()
        self.name = self.ui.nameLineEdit.text().replace(" ", "_")
        self.sample = self.ui.samplesComboBox.currentText()
        if not self.path:
            self.ui.browseButton.setFocus()
            return
        if not self.name:
            self.ui.nameLineEdit.setFocus()
            return
        if not self.sample:
            self.ui.addSampleButton.setFocus()
            return

        sample = self.__find_existing_sample()

        if sample:
            # Check if measurement on the same name already exists.
            for key in sample.measurements.measurements.keys():
                if sample.measurements.measurements[key].name == self.name:
                    QtWidgets.QMessageBox.critical(self, "Already exists",
                                                   "There already is a "
                                                   "measurement with this name!"
                                                   "\n\n Choose another "
                                                   "name.",
                                                   QtWidgets.QMessageBox.Ok,
                                                   QtWidgets.QMessageBox.Ok)
                    self.__close = False
                    break
                else:
                    self.__close = True
        else:
            self.close()
        if self.__close:
            self.close()

    def __browse_files(self):
        self.filename = open_file_dialog(self, self.directory,
                                         "Select a measurement to load",
                                         "Raw Measurement (*.asc)")
        self.ui.pathLineEdit.setText(self.filename)

    @staticmethod
    def __check_text(input_field):
        iv.check_text(input_field)

    def __find_existing_sample(self):
        """
        Find existing sample that matches the sample name in dialog.

        Return:
            Sample object or None.
        """
        for sample in self.samples:
            if "Sample " + "%02d" % sample.serial_number + " " + sample.name \
                    == self.sample:
                return sample
        return None
