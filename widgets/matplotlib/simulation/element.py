# coding=utf-8
"""
Created on 1.3.2018
Updated on 2.7.2018

Potku is a graphical user interface for analyzation and
visualization of measurement data collected from a ToF-ERD
telescope. For physics calculations Potku uses external
analyzation components.
Copyright (C) 2018 Severi Jääskeläinen, Samuel Kaiponen, Heta Rekilä and
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
__author__ = "Severi Jääskeläinen \n Samuel Kaiponen \n Heta Rekilä \n " \
             "Sinikka Siironen"
__version__ = "2.0"

import modules.general_functions as general

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from dialogs.energy_spectrum import EnergySpectrumParamsDialog, \
    EnergySpectrumWidget
from dialogs.simulation.element_simulation_settings import \
    ElementSimulationSettingsDialog


class ElementWidget(QtWidgets.QWidget):
    """Class for creating an element widget for the recoil atom distribution.

    Args:
        parent: A SimulationTabWidget.
        """

    def __init__(self, parent, element, parent_tab, element_simulation):
        """
        Initializes the ElementWidget.

        Args:
            parent: A RecoilAtomDistributionWidget.
            element: An Element object.
            parent_tab: A SimulationTabWidget.
            element_simulation: ElementSimulation object.
        """
        super().__init__()

        self.parent = parent
        self.parent_tab = parent_tab
        self.element_simulation = element_simulation

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.radio_button = QtWidgets.QRadioButton()

        if element.isotope:
            isotope_superscript = general.to_superscript(str(element.isotope))
            button_text = isotope_superscript + " " + element.symbol
        else:
            button_text = element.symbol

        self.radio_button.setText(button_text)

        draw_spectrum_button = QtWidgets.QPushButton()
        draw_spectrum_button.setIcon(QIcon(
            "ui_icons/potku/energy_spectrum_icon.svg"))
        draw_spectrum_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        draw_spectrum_button.clicked.connect(self.plot_spectrum)

        horizontal_layout.addWidget(self.radio_button)
        horizontal_layout.addWidget(draw_spectrum_button)

        settings_button = QtWidgets.QPushButton()
        settings_button.setIcon(QIcon("ui_icons/reinhardt/gear.svg"))
        settings_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        settings_button.clicked.connect(
            self.open_element_simulation_settings)
        horizontal_layout.addWidget(settings_button)

        self.setLayout(horizontal_layout)

    def add_element_simulation_reference(self, element_simulation):
        """
        Add reference to an Element Simulation object.
        """
        self.element_simulation = element_simulation

    def open_element_simulation_settings(self):
        """
        Open element simulation settings.
        """
        ElementSimulationSettingsDialog(self.element_simulation)

    def plot_spectrum(self):
        """
        Plot an energy spectrum.
        """
        # self.element_simulation.calculate_espe()
        dialog = EnergySpectrumParamsDialog(
            self.parent, spectrum_type="simulation",
            element_simulation=self.element_simulation)
        if dialog.result_files:
            self.parent.energy_spectrum_widget = EnergySpectrumWidget(
                parent=self.parent, use_cuts=dialog.result_files,
                bin_width=dialog.bin_width, spectrum_type="simulation")
            self.parent.add_widget(self.parent.energy_spectrum_widget)
