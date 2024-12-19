
from PyQt5.QtWidgets import *
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)
from theme import theme

class SaltNoiseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atai daiarogu")
        self.setGeometry(200, 200, 300, 50)

        self.setStyleSheet(f"background-color: {theme.dialog_bg}; border: 2px solid {theme.dialog_border}")

        self.amount_spin = QDoubleSpinBox()
        self.salt_vs_pepper_spin = QDoubleSpinBox()

        for spin_box in (self.amount_spin, self.salt_vs_pepper_spin):
            spin_box.setRange(0, 1)
            spin_box.setSingleStep(0.1)
            spin_box.setStyleSheet(
            f"background-color: {theme.spin_bg}; color: {theme.spin_text}; border-radius: 0px; border: 2px solid {theme.spin_border}; padding: 5px 10px; font-weight: bold;"
            )

        self.amount_spin.setValue(0.5)
        self.salt_vs_pepper_spin.setValue(0.5)

        label_style = f"color: {theme.label_color}; font-weight: bold; font-size: 16px; border-width: 0px;"
        
        self.amount_label = QLabel("Amount")
        self.amount_label.setStyleSheet(label_style)
        
        self.salt_vs_pepper_label = QLabel("Salt vs Pepper")
        self.salt_vs_pepper_label.setStyleSheet(label_style)

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
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_spin)
        layout.addWidget(self.salt_vs_pepper_label)
        layout.addWidget(self.salt_vs_pepper_spin)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

    def get_coefficients(self):
        return self.amount_spin.value(), self.salt_vs_pepper_spin.value()
