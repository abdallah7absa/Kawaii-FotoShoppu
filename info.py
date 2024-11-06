import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QDialog
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

class Info(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Info')
        self.setFixedSize(970, 581)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.centerWindow()

        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("assets/info.png").scaled(970, 581))
        self.image_label.setGeometry(0, 0, 970, 581)

        self.close_button = QPushButton('x', self)
        self.close_button.setGeometry(920, 10, 40, 40)
        self.close_button.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: black; border: none; font-size: 40px; font-weight: 50%;")
        self.close_button.clicked.connect(self.close)

        self.dragging = False
        self.offset = QPoint()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def centerWindow(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        x = (screen_width - self.width()) // 2
        y = (screen_height - self.height()) // 2

        self.move(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Info()
    window.show()
    sys.exit(app.exec_())
