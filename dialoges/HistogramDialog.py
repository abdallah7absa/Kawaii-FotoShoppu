
from PyQt5.QtWidgets import *


class HistogramDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atai daiarogu")
        self.setGeometry(200, 200, 300, 50)

        self.setStyleSheet("background-color: #ffffff;")

        self.left_spin = QDoubleSpinBox()
        self.right_spin = QDoubleSpinBox()

        self.left_spin.setStyleSheet(
            "background-color: #dd91b9; color: white; border-radius: 0px; border: 2px solid #983569; padding: 5px 10px; font-weight: bold;"
        )
        self.left_spin.setRange(0, 255)
        self.left_spin.setSingleStep(1)
        self.left_spin.setValue(0)

        self.right_spin.setStyleSheet(
            "background-color: #dd91b9; color: white; border-radius: 0px; border: 2px solid #983569; padding: 5px 10px; font-weight: bold;"
        )
        self.right_spin.setRange(0, 255)
        self.right_spin.setSingleStep(1)
        self.right_spin.setValue(255)

        label_style = "color: #983569; font-weight: bold; font-size: 16px"
        
        self.left_label = QLabel("Left value")
        self.left_label.setStyleSheet(label_style)
        
        self.right_label = QLabel("Right value")
        self.right_label.setStyleSheet(label_style)

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
        layout.addWidget(self.left_label)
        layout.addWidget(self.left_spin)
        layout.addWidget(self.right_label)
        layout.addWidget(self.right_spin)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def get_coefficients(self):
        return self.left_spin.value(), self.right_spin.value()
