
from PyQt5.QtWidgets import *
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, parent_dir)
from theme import theme

class CutoffAndOrderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atai daiarogu")
        self.setGeometry(200, 200, 300, 50)

        self.setStyleSheet(f"background-color: {theme.dialog_bg}; border: 2px solid {theme.dialog_border}")

        self.cutoff_spin = QDoubleSpinBox()
        self.cutoff_spin.setRange(1, 256)
        self.cutoff_spin.setSingleStep(1)

        self.order_spin = QDoubleSpinBox()
        self.cutoff_spin.setRange(1, 10)
        self.cutoff_spin.setSingleStep(1)

        for spin_box in (self.cutoff_spin, self.order_spin):
            spin_box.setStyleSheet(
                f"background-color: {theme.spin_bg}; color: {theme.spin_text}; border-radius: 0px; border: 2px solid {theme.spin_border}; padding: 5px 10px; font-weight: bold;"
            )

        self.cutoff_spin.setValue(50)
        self.order_spin.setValue(2)

        label_style = f"color: {theme.label_color}; font-weight: bold; font-size: 16px; border-width: 0px;"
        
        self.cutoff_label = QLabel("cutoff")
        self.cutoff_label.setStyleSheet(label_style)
        
        self.order_label = QLabel("Standard Deviation")
        self.order_label.setStyleSheet(label_style)

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
        layout.addWidget(self.cutoff_label)
        layout.addWidget(self.cutoff_spin)
        layout.addWidget(self.order_label)
        layout.addWidget(self.order_spin)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

    def get_coefficients(self):
        return self.cutoff_spin.value(), self.order_spin.value()
