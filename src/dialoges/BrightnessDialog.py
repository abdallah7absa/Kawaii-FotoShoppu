
from PyQt5.QtWidgets import *
import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QDialog
from PyQt5.QtGui import QMovie, QFont, QMouseEvent, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize

class BrightnessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Atai daiarogu")
        self.setStyleSheet("background-color: #ffffff;")


        self.brightness_spin = QDoubleSpinBox()

        self.brightness_spin.setRange(0, 255)
        self.brightness_spin.setSingleStep(1)
        self.brightness_spin.setValue(128)
        self.brightness_spin.setStyleSheet(
            "background-color: #dd91b9; color: white; border-radius: 0px; border: 2px solid #983569; padding: 5px 10px; font-weight: bold;"
        )

        label_style = "color: #983569; font-weight: bold; font-size: 16px"

        self.brightness_label = QLabel("Brightness value")
        self.brightness_label.setStyleSheet(label_style)        

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.accept)
        self.apply_button.setStyleSheet(
            """
            QPushButton {
                background-color: #dd91b9;
                color: white;
                border: 2px solid #983569;
                border-radius: 0px;
                padding: 5px 10px;
                font-weight: bold;
                margin: 20px 0px 10px 0px;
            }
            QPushButton:hover {
                background-color: #e5a1c1;
            }
            QPushButton:pressed {
                background-color: #c57b9a;
            }
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(self.brightness_label)
        layout.addWidget(self.brightness_spin)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)
        self.setGeometry(200, 200, 300, 50)


    def get_coefficients(self):
        return self.brightness_spin.value()
