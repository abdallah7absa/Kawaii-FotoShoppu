
from PyQt5.QtWidgets import *
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)
from theme import theme

class HistogramDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atai daiarogu")
        self.setGeometry(200, 200, 300, 50)

        self.setStyleSheet(f"background-color: {theme.dialog_bg}; border: 2px solid {theme.dialog_border}")

        self.left_spin = QDoubleSpinBox()
        self.right_spin = QDoubleSpinBox()

        self.left_spin.setStyleSheet(
            f"background-color: {theme.spin_bg}; color: {theme.spin_text}; border-radius: 0px; border: 2px solid {theme.spin_border}; padding: 5px 10px; font-weight: bold;"
        )
        self.left_spin.setRange(0, 255)
        self.left_spin.setSingleStep(1)
        self.left_spin.setValue(0)

        self.right_spin.setStyleSheet(
            f"background-color: {theme.spin_bg}; color: {theme.spin_text}; border-radius: 0px; border: 2px solid {theme.spin_border}; padding: 5px 10px; font-weight: bold;"
        )
        self.right_spin.setRange(0, 255)
        self.right_spin.setSingleStep(1)
        self.right_spin.setValue(255)

        label_style = f"color: {theme.label_color}; font-weight: bold; font-size: 16px; border-width: 0px;"
        
        self.left_label = QLabel("Left value")
        self.left_label.setStyleSheet(label_style)
        
        self.right_label = QLabel("Right value")
        self.right_label.setStyleSheet(label_style)

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
        layout.addWidget(self.left_label)
        layout.addWidget(self.left_spin)
        layout.addWidget(self.right_label)
        layout.addWidget(self.right_spin)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def get_coefficients(self):
        return self.left_spin.value(), self.right_spin.value()
