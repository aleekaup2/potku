# coding=utf-8
"""
Created on 5.4.2018
"""
__author__ = "Severi Jääskeläinen \n Samuel Kaiponen \n Heta Rekilä \n Sinikka Siironen"

import os
from PyQt5 import uic, QtWidgets


class DetectorSettingsWidget(QtWidgets.QWidget):
    """Class for creating a request wide simulation settings tab.
    """
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join("ui_files",
                                  "ui_request_detector_settings.ui"), self)