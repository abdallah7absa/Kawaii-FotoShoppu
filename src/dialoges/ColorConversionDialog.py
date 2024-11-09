
from PyQt5.QtWidgets import *


class ColorConversionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atai daiarogu")
        self.setGeometry(200, 200, 300, 50)

        self.setStyleSheet("background-color: #ffffff;")

        self.red_spin = QDoubleSpinBox()
        self.green_spin = QDoubleSpinBox()
        self.blue_spin = QDoubleSpinBox()
        self.threashhold_spin = QDoubleSpinBox()

        for spin_box in (self.red_spin, self.green_spin, self.blue_spin, self.threashhold_spin):
            spin_box.setRange(0, 1)
            spin_box.setSingleStep(0.01)
            spin_box.setStyleSheet(
                "background-color: #dd91b9; color: white; border-radius: 0px; border: 2px solid #983569; padding: 5px 10px; font-weight: bold;"
            )

        self.red_spin.setValue(0.299)
        self.green_spin.setValue(0.587)
        self.blue_spin.setValue(0.114)
        self.threashhold_spin.setValue(0.5)

        label_style = "color: #983569; font-weight: bold; font-size: 16px"
        
        self.red_label = QLabel("Red Coefficient")
        self.red_label.setStyleSheet(label_style)
        
        self.green_label = QLabel("Green Coefficient")
        self.green_label.setStyleSheet(label_style)
        
        self.blue_label = QLabel("Blue Coefficient")
        self.blue_label.setStyleSheet(label_style)

        self.threashhold_label = QLabel("Threashhold")
        self.threashhold_label.setStyleSheet(label_style)

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
        layout.addWidget(self.red_label)
        layout.addWidget(self.red_spin)
        layout.addWidget(self.green_label)
        layout.addWidget(self.green_spin)
        layout.addWidget(self.blue_label)
        layout.addWidget(self.blue_spin)
        layout.addWidget(self.threashhold_label)
        layout.addWidget(self.threashhold_spin)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

    def get_coefficients(self):
        return self.red_spin.value(), self.green_spin.value(), self.blue_spin.value(), self.threashhold_spin.value()*255
