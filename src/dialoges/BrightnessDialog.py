
from PyQt5.QtWidgets import *
import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QDialog
from PyQt5.QtGui import QMovie, QFont, QMouseEvent, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)
from theme import theme

class BrightnessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Atai daiarogu")
        self.setStyleSheet(f"background-color: {theme.dialog_bg}; border: 2px solid {theme.dialog_border}")


        self.brightness_spin = QDoubleSpinBox()

        self.brightness_spin.setRange(0, 255)
        self.brightness_spin.setSingleStep(1)
        self.brightness_spin.setValue(128)
        self.brightness_spin.setStyleSheet(
            f"background-color: {theme.spin_bg}; color: {theme.spin_text}; border-radius: 0px; border: 2px solid {theme.spin_border}; padding: 5px 10px; font-weight: bold;"
        )

        label_style = f"color: {theme.label_color}; font-weight: bold; font-size: 16px; border-width: 0px;"

        self.brightness_label = QLabel("Brightness value")
        self.brightness_label.setStyleSheet(label_style)        

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.accept)
        self.apply_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {theme.button_bg};
                color: white;
                border: 2px solid {theme.button_border};
                border-radius: 0px;
                padding: 5px 10px;
                font-weight: bold;
                margin: 20px 0px 10px 0px;
            }}
            QPushButton:hover {{
                background-color: {theme.button_hover};
            }}
            QPushButton:pressed {{
                background-color: {theme.button_pressed};
            }}
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
