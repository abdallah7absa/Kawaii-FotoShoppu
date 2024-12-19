
from PyQt5.QtWidgets import *
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)
from theme import theme

class GaussianNoiseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atai daiarogu")
        self.setGeometry(200, 200, 300, 50)

        self.setStyleSheet(f"background-color: {theme.dialog_bg}; border: 2px solid {theme.dialog_border}")

        self.mean_spin = QDoubleSpinBox()
        self.std_dev_spin = QDoubleSpinBox()

        for spin_box in (self.mean_spin, self.std_dev_spin):
            spin_box.setRange(0, 255)
            spin_box.setSingleStep(1)
            spin_box.setStyleSheet(
                f"background-color: {theme.spin_bg}; color: {theme.spin_text}; border-radius: 0px; border: 2px solid {theme.spin_border}; padding: 5px 10px; font-weight: bold;"
            )

        self.mean_spin.setValue(128)
        self.std_dev_spin.setValue(128)

        label_style = f"color: {theme.label_color}; font-weight: bold; font-size: 16px; border-width: 0px;"
        
        self.mean_label = QLabel("Mean")
        self.mean_label.setStyleSheet(label_style)
        
        self.std_dev_label = QLabel("Standard Deviation")
        self.std_dev_label.setStyleSheet(label_style)

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
        layout.addWidget(self.mean_label)
        layout.addWidget(self.mean_spin)
        layout.addWidget(self.std_dev_label)
        layout.addWidget(self.std_dev_spin)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

    def get_coefficients(self):
        return self.mean_spin.value(), self.std_dev_spin.value()
