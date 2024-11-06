
from PyQt5.QtWidgets import *


class GammaCorrectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atai daiarogu")
        self.setGeometry(200, 200, 300, 50)

        self.setStyleSheet("background-color: #ffffff;")

        self.gamma_spin = QDoubleSpinBox()

        self.gamma_spin.setStyleSheet(
            "background-color: #dd91b9; color: white; border-radius: 0px; border: 2px solid #983569; padding: 5px 10px; font-weight: bold;"
        )
        self.gamma_spin.setRange(0.1, float('inf'))
        self.gamma_spin.setSingleStep(0.1)
        self.gamma_spin.setValue(1.0)

        label_style = "color: #983569; font-weight: bold; font-size: 16px"
        
        self.gamma_label = QLabel("Gamma value")
        self.gamma_label.setStyleSheet(label_style)
      
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
        layout.addWidget(self.gamma_label)
        layout.addWidget(self.gamma_spin)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def get_coefficients(self):
        return self.gamma_spin.value()
