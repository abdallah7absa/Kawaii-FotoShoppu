import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QDialog
from PyQt5.QtGui import QMovie, QFont, QMouseEvent, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize
from theme import theme

class ErrorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        
        # self.theme = theme.Theme()

        self.offset = None

        self.gifs_folder = theme.gif_assets
        self.image_assets = theme.image_assets

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        
        self.frame = QFrame(self)
        self.frame.setStyleSheet("QFrame { background-color: #983569; border: 8px solid #652345; }")
        
        self.main_layout = QVBoxLayout(self.frame)
        
        self.close_button = QPushButton('x', self)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("QPushButton {"
                                   "border: none; "
                                   "color: white; "
                                   "font-size: 50px; "
                                   "padding: 0px; "
                                   "color: #f1d3e3"
                                   "}")
        
        self.top_layout = QHBoxLayout()
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.close_button)
        
        self.main_layout.addLayout(self.top_layout)
        
        self.gif_label = QLabel(self)
        self.gif_label.setStyleSheet("""
            QLabel{
                border: 0px solid #d6aec3;
                padding: 15;
            }
            """)
        self.gif = QMovie(self.get_random_gif())
        self.gif_label.setMovie(self.gif)
        # gif.setScaledSize(QSize(300, 300))
        self.gif.start()
        self.main_layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        
        self.error_message = QLabel("Error Message", self)
        self.font = QFont('Inter', 20)
        self.font.setBold(True)
        self.error_message.setFont(self.font)
        self.error_message.setStyleSheet("color: white; background: none; padding: 20px; border: none;")  # Add padding around the message
        self.error_message.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.error_message, alignment=Qt.AlignCenter)
        
        self.frame.setLayout(self.main_layout)
        
        self.outer_layout.addWidget(self.frame)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setFixedSize(500, 400)
        self.setWindowTitle("Bakaaaaaaa!")
        self.setWindowIcon(QIcon(f'{self.image_assets}/icon.png'))

    def get_random_gif(self):
        self.gifs = [os.path.join(self.gifs_folder, f) for f in os.listdir(self.gifs_folder) if f.endswith('.gif')]
        return random.choice(self.gifs)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset is not None:
            self.move(self.pos() + event.globalPos() - self.mapToGlobal(self.offset))
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.offset = None

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ErrorWindow()
    ex.show()
    sys.exit(app.exec_())
