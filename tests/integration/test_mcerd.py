# coding=utf-8
"""
Created on 8.2.2020

Potku is a graphical user interface for analyzation and
visualization of measurement data collected from a ToF-ERD
telescope. For physics calculations Potku uses external
analyzation components.
Copyright (C) 2020 TODO

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

__author__ = "Juhani Sundell"
__version__ = ""  # TODO

import unittest
import tempfile
import tests.mock_objects as mo

from string import Template
from tests.utils import get_resource_dir
from tests.utils import PlatformSwitcher
from modules.mcerd import MCERD
from pathlib import Path


class TestMCERD(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.directory = Path(tempfile.gettempdir())
        cls.mcerd = MCERD({
            "recoil_element": mo.get_recoil_element(),
            "sim_dir": tempfile.gettempdir(),
            "simulation_type": "ERD",
            "seed_number": 101,
            "target": mo.get_target(),
            "detector": mo.get_detector(),
            "beam": mo.get_beam(),
            "minimum_scattering_angle": 5.5,
            "minimum_main_scattering_angle": 6.5,
            "minimum_energy_of_ions": 8.15,
            "number_of_recoils": 15,
            "simulation_mode": "narrow",
            "number_of_scaling_ions": 14,
            "number_of_ions_in_presimu": 100,
            "number_of_ions": 1000
        }, mo.get_element_simulation())

    def test_get_command(self):
        """Tests the get_command function on different platforms.
        """
        # PlatformSwitcher cannot change the separator char in file paths.
        # Therefore the same bin_path and file_path is used for each system
        bin_path = Path("external/Potku-bin/mcerd")
        file_path = self.directory / "He-Default"

        with PlatformSwitcher("Windows"):
            cmd = f"{bin_path}.exe {file_path}"
            self.assertEqual(cmd, self.mcerd.get_command())

        with PlatformSwitcher("Linux"):
            cmd = f"ulimit -s 64000; exec {bin_path} {file_path}"
            self.assertEqual(cmd, self.mcerd.get_command())

        with PlatformSwitcher("Darwin"):
            # file_path and command stay same
            self.assertEqual(cmd, self.mcerd.get_command())

    def test_paths(self):
        """Testing various file paths that MCERD uses."""
        self.assertEqual(
            str(self.directory / "He-Default.recoil"),
            self.mcerd.recoil_file)
        self.assertEqual(
            str(self.directory / "He-Default.101.erd"),
            self.mcerd.result_file)
        self.assertEqual(
            str(self.directory / "He-Default"),
            self.mcerd._MCERD__command_file)

        # These use the parent prefix, therefore they do not start with 'He'
        self.assertEqual(
            str(self.directory / "-Default.erd_target"),
            self.mcerd._MCERD__target_file)
        self.assertEqual(
            str(self.directory / "-Default.erd_detector"),
            self.mcerd._MCERD__detector_file)
        self.assertEqual(
            str(self.directory / "-Default.foils"),
            self.mcerd._MCERD__foils_file)
        self.assertEqual(
            str(self.directory / "-Default.pre"),
            self.mcerd._MCERD__presimulation_file)

    def test_get_command_file_contents(self):
        detector_file = Path(get_resource_dir()) / "mcerd_command.txt"
        temp_dict = {
            "tgt_file": self.directory / "-Default.erd_target",
            "det_file": self.directory / "-Default.erd_detector",
            "rec_file": self.directory / "He-Default.recoil",
            "pre_file": self.directory / "-Default.pre"
        }

        with open(detector_file) as file:
            temp = Template(file.read())

        expected = temp.substitute(temp_dict)
        output = self.mcerd.get_command_file_contents()

        self.assertEqual(expected, output)

    def test_get_detector_file_contents(self):
        detector_file = Path(get_resource_dir()) / "detector_file.txt"
        temp_dict = {
            "foils_file": Path(tempfile.gettempdir()) / "-Default.foils"
        }

        with open(detector_file) as file:
            temp = Template(file.read())

        expected = temp.substitute(temp_dict)
        output = self.mcerd.get_detector_file_contents()

        self.assertEqual(expected, output)

    def test_get_target_file_contents(self):
        pass

    def test_get_foils_file_contents(self):
        pass