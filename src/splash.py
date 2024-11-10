import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt, QRect
import main
import time
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import *
from theme import theme

def show_splash_screen():
    app = QApplication(sys.argv)

    image_assets = theme.image_assets
    sound_assets = theme.sound_assets

    bg_player = QMediaPlayer()
    mp3_url = QUrl.fromLocalFile(f"{sound_assets}/windows.mp3")
    content = QMediaContent(mp3_url)
    bg_player.setMedia(content)
    bg_player.play()

    splash_pix = QPixmap(f'{image_assets}/splash.png')
    splash_pix = splash_pix.scaled(461, 676, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    splash = QSplashScreen(splash_pix)

    screen_geometry = app.primaryScreen().geometry()
    splash_x = (screen_geometry.width() - splash.width()) // 2
    splash_y = (screen_geometry.height() - splash.height()) // 2
    splash.setGeometry(QRect(splash_x, splash_y, splash.width(), splash.height()))


    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    splash.show()

    QTimer.singleShot(2, splash.close)
    time.sleep(2)

    window = main.KawaīFotoShoppu()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    show_splash_screen()
