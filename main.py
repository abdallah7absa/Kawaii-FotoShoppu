from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon, QCursor
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import img
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import dialoges.ColorConversionDialog
import dialoges.GammaCorrectionDialog
import dialoges.HistogramDialog
import dialoges.BrightnessDialog
from screeninfo import get_monitors
import error
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import info


class KawaīFotoShoppu(QMainWindow):
    def __init__(self):
        super().__init__()

        monitors = get_monitors()
        for monitor in monitors:
            self.monitor_width = monitor.width
            self.monitor_height = monitor.height
        self.aspect_ratio = self.monitor_width / self.monitor_height

        self.setWindowTitle("Kawaī foto shoppu")
        self.setWindowIcon(QIcon('assets/icon.png'))

        self.showFullScreen()

        cursor_image = QPixmap('assets/cursor.png')
        custom_cursor = QCursor(cursor_image)
        QApplication.setOverrideCursor(custom_cursor)

        self.bg_player = QMediaPlayer()
        mp3_url = QUrl.fromLocalFile("sounds/bg.mp3")
        content = QMediaContent(mp3_url)
        self.bg_player.setMedia(content)
        self.bg_player.play()

        self.player = QMediaPlayer()

        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.monitor_width, self.monitor_height)

        bg_pixmap = QPixmap('assets/bg.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.bg_label.setPixmap(bg_pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.show()

        self.file_name = ""
        self.showing_image = ""
        self.current_filter = ""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_item_click)

        self.tree.setFixedSize(self.scale(550, 'w'), self.scale(1050, 'h'))
        left_layout.addWidget(self.tree)

        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                margin: {self.scale(50, 'h')}px;
                background-color: #DD91B9;
                color: #FFFFFF;
                border: {self.scale(8, 'h')}px solid #f1d3e3;
                border-radius: {self.scale(23, 'h')}px;
                padding-top: {self.scale(150, 'h')}px;
                padding-left: {self.scale(10, 'w')}px;
            }}
            QTreeWidget::item:hover {{
                background-color: #ffffff;
                color: #DD91B9;
            }}
            QScrollBar:vertical {{
                background-color: #DD91B9;
                width: {self.scale(20, 'w')}px;
                margin: 0 {self.scale(9, 'h')}px {self.scale(25, 'w')}px 0;
                border-radius: {self.scale(23, 'h')}px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #ffffff;
                min-height: {self.scale(20, 'h')}px;
                border-radius: {self.scale(23, 'h')}px;
            }}
            QScrollBar:horizontal {{
                background-color: #DD91B9;
                height: {self.scale(12, 'h')}px;
                margin: 0px;
                border-radius: {self.scale(23, 'h')}px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: #ffffff;
                min-width: {self.scale(20, 'w')}px;
                border-radius: {self.scale(23, 'h')}px;
            }}
            QScrollBar::add-line, QScrollBar::sub-line {{
                width: 0px;
                height: 0px;
            }}
            QScrollBar::up-arrow, QScrollBar::down-arrow, QScrollBar::left-arrow, QScrollBar::right-arrow {{
                background: none;
                width: 0;
                height: 0;
            }}
            QTreeWidget::item {{
                color: #FFFFFF;
                padding: 1px;
            }}
            QTreeWidget::item:selected {{
                background-color: #DD91B9;
                color: #FFFFFF;
                outline: none;
            }}
            QTreeWidget::item:selected:active {{
                background-color: #DD91B9;
                color: white;
            }}
            QTreeWidget::item:selected:!active {{
                background-color: #DD91B9;
                color: white;
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                image: url(assets/right.png);
                height: 20px;
                width: 20px;
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                image: url(assets/down.png);
                height: 20px;
                width: 20px;
            }}
        """)

        self.apply_shadow_effect(self.tree)

        h1_font = QFont()
        h1_font.setPointSize(self.scale(21, 'w'))
        h1_font.setWeight(QFont.Thin)

        h2_font = QFont()
        h2_font.setPointSize(self.scale(19, 'w'))
        h2_font.setWeight(QFont.Thin)
        
        h3_font = QFont()
        h3_font.setPointSize(self.scale(17, 'w'))
        h3_font.setWeight(QFont.Bold)

        self.tree.setLayoutDirection(Qt.LeftToRight)

        self.roots = ["Colors Conversions", "Point Processing", "Brightness", "Corrections", "Histogram Processing"]
        self.brightness_childs = ["Add value", "Multiply value", "Subtract value", "Divide value"]
        self.corrections_childs = ["Log Corrections", "Inverse Log", "Complement"]

        self.colors_conversions_root = QTreeWidgetItem(self.tree)
        self.colors_conversions_root.setText(0, "Colors Conversions")
        self.colors_conversions_root.setFont(0, h1_font)

        self.point_processing_root = QTreeWidgetItem(self.tree)
        self.point_processing_root.setText(0, "Point Processing")
        self.point_processing_root.setFont(0, h1_font)

        rgb_to_binary_child = QTreeWidgetItem(self.colors_conversions_root)
        rgb_to_binary_child.setText(0, "RGB → Binary")
        rgb_to_binary_child.setFont(0, h3_font)

        rgb_to_gray_child = QTreeWidgetItem(self.colors_conversions_root)
        rgb_to_gray_child.setText(0, "RGB → Gray")
        rgb_to_gray_child.setFont(0, h3_font)

        rgb_to_binary_child = QTreeWidgetItem(self.colors_conversions_root)
        rgb_to_binary_child.setText(0, "Gray → Binary")
        rgb_to_binary_child.setFont(0, h3_font)

        self.brightness_root = QTreeWidgetItem(self.point_processing_root)
        self.brightness_root.setText(0, "Brightness")
        self.brightness_root.setFont(0, h2_font)

        add_brightness_child = QTreeWidgetItem(self.brightness_root)
        add_brightness_child.setText(0, "Add value")
        add_brightness_child.setFont(0, h3_font)

        multiply_brightness_child = QTreeWidgetItem(self.brightness_root)
        multiply_brightness_child.setText(0, "Multiply value")
        multiply_brightness_child.setFont(0, h3_font)

        subtract_brightness_child = QTreeWidgetItem(self.brightness_root)
        subtract_brightness_child.setText(0, "Subtract value")
        subtract_brightness_child.setFont(0, h3_font)

        divide_brightness_child = QTreeWidgetItem(self.brightness_root)
        divide_brightness_child.setText(0, "Divide value")
        divide_brightness_child.setFont(0, h3_font)
        
        self.corrections_root = QTreeWidgetItem(self.point_processing_root)
        self.corrections_root.setText(0, "Corrections")
        self.corrections_root.setFont(0, h2_font)

        gamma_child = QTreeWidgetItem(self.corrections_root)
        gamma_child.setText(0, "Gamma Corrections")
        gamma_child.setFont(0, h3_font)

        log_child = QTreeWidgetItem(self.corrections_root)
        log_child.setText(0, "Log Corrections")
        log_child.setFont(0, h3_font)

        inverse_log_child = QTreeWidgetItem(self.corrections_root)
        inverse_log_child.setText(0, "Inverse Log")
        inverse_log_child.setFont(0, h3_font)

        complement_child = QTreeWidgetItem(self.corrections_root)
        complement_child.setText(0, "Complement")
        complement_child.setFont(0, h3_font)

        self.histogram_processing_root = QTreeWidgetItem(self.point_processing_root)
        self.histogram_processing_root.setText(0, "Histogram Processing")
        self.histogram_processing_root.setFont(0, h2_font)

        original_histogram_child = QTreeWidgetItem(self.histogram_processing_root)
        original_histogram_child.setText(0, "Original Histogram")
        original_histogram_child.setFont(0, h3_font)

        stretched_histogram_child = QTreeWidgetItem(self.histogram_processing_root)
        stretched_histogram_child.setText(0, "Stretched Histogram")
        stretched_histogram_child.setFont(0, h3_font)

        equalized_histogram_child = QTreeWidgetItem(self.histogram_processing_root)
        equalized_histogram_child.setText(0, "Equalized Histogram")
        equalized_histogram_child.setFont(0, h3_font)

        # self.tree.collapseAll()

        self.colors_conversions_root.setExpanded(False)
        self.point_processing_root.setExpanded(True)
        self.brightness_root.setExpanded(False)
        self.corrections_root.setExpanded(False)
        self.histogram_processing_root.setExpanded(False)

        main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/img.jpg")
        self.image_label.setPixmap(pixmap.scaled(self.scale(400, 'w'), self.scale(400, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        right_layout.addWidget(self.image_label)

        main_layout.addLayout(right_layout)

        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(self.scale(90, 'w'), self.scale(90, 'h'), self.scale(383, 'w'), self.scale(101, 'h'))
        logo_pixmap = QPixmap('assets/logo2.png').scaled(self.scale(383, 'w'), self.scale(101, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.show()

        self.upload_label = QLabel(self)
        self.upload_label.setGeometry(self.scale(705, 'w'), self.scale(95, 'h'), self.scale(1027, 'w'), self.scale(806, 'h'))
        upload_pixmap = QPixmap('assets/upload.png').scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.upload_label.setAlignment(Qt.AlignCenter)
        self.upload_label.setPixmap(upload_pixmap)
        if self.aspect_ratio != 16/9:
            self.upload_label.setScaledContents(True)
        self.upload_label.show()
        self.upload_label.mousePressEvent = self.img_click
        self.upload_label.setStyleSheet(f"""
            QLabel{{
                background-color: #dd91b9;
                border-radius: {self.scale(23, 'h')}px;
            }}
        """)

        self.apply_button = QPushButton("Export", self)
        self.apply_button.setGeometry(self.scale(709, 'w'), self.scale(914, 'h'), self.scale(225, 'w'), self.scale(81, 'h'))
        self.apply_button.setStyleSheet(f"""
            QPushButton{{background-color: #DD91B9;
                        color: white;
                        font-size: {self.scale(25, 'w')}px;
                        font-weight: bold;
                        border: {self.scale(8, 'h')}px solid #f1d3e3;
                        border-radius: {self.scale(23, 'h')}px;}}
            QPushButton:hover {{
                background-color: #e5a1c1;
            }}
        """)
        self.apply_button.show()
        self.apply_button.clicked.connect(self.export)


        self.show_figure_button = QPushButton("Show Figure", self)
        self.show_figure_button.setGeometry(self.scale(971, 'w'), self.scale(914, 'h'), self.scale(500, 'w'), self.scale(81, 'h'))
        self.show_figure_button.setStyleSheet(f"""
            QPushButton {{background-color: #DD91B9;
                        color: white;
                        font-size: {self.scale(25, 'w')}px;
                        font-weight: bold;
                        border: {self.scale(8, 'h')}px solid #f1d3e3;
                        border-radius: {self.scale(23, 'h')}px;}}
            QPushButton:hover {{
                background-color: #e5a1c1;
            }}
        """)
        self.show_figure_button.show()
        self.show_figure_button.clicked.connect(self.figure)


        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(self.scale(1507, 'w'), self.scale(914, 'h'), self.scale(225, 'w'), self.scale(81, 'h'))
        self.clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #983569;
                color: white;
                font-size: {self.scale(25, 'w')}px;
                font-weight: bold;
                /*border: {self.scale(8, 'h')}px solid #f1d3e3;*/
                border-radius: {self.scale(23, 'h')}px;
            }}
            QPushButton:hover {{
                background-color: #a93b74;
            }}
        """)
        self.clear_button.show()
        self.clear_button.clicked.connect(self.clear)

        self.apply_shadow_effect(self.upload_label)
        self.apply_shadow_effect(self.apply_button)
        self.apply_shadow_effect(self.show_figure_button)
        self.apply_shadow_effect(self.clear_button)

        self.close_label = QLabel(self)
        self.close_label.setGeometry(self.scale(1650, 'w'), self.scale(123, 'h'), self.scale(60, 'w'), self.scale(60, 'h'))
        close_pixmap = QPixmap('assets/close.png').scaled(self.scale(60, 'w'), self.scale(60, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.close_label.setPixmap(close_pixmap)
        self.close_label.setScaledContents(True)
        self.close_label.mousePressEvent = self.close_click

        self.info_label = QLabel(self)
        self.info_label.setGeometry(self.scale(435, 'w'), self.scale(951, 'h'), self.scale(40, 'w'), self.scale(40, 'h'))
        info_pixmap = QPixmap('assets/info_button.png').scaled(self.scale(40, 'w'), self.scale(40, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.info_label.setPixmap(info_pixmap)
        self.info_label.setScaledContents(True)
        self.info_label.show()
        self.info_label.mousePressEvent = self.info_click

        fps = 15
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(1000//fps)
        self.timer.start()

    def info_click(self, event):
        self.play_mp3("sounds/button.mp3")
        info_window = info.Info()
        if not info_window.exec_(): self.play_mp3("sounds/baa.mp3")




    def export(self, event):
        if self.showing_image:
            self.play_mp3("sounds/button.mp3")
            if isinstance(self.showing_image, str):
                image = QPixmap(self.showing_image).toImage()
            elif isinstance(self.showing_image, QImage):
                image = self.showing_image
            else:
                print("Error: showing_image is not a valid image format.")
                return
            
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Save Image",
                "",
                "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp);;GIF Files (*.gif);;All Files (*)",
                options=options
            )

            if file_path:
                file_extension = file_path.split('.')[-1].upper()
                if file_extension not in ['PNG', 'JPG', 'JPEG', 'BMP', 'GIF']:
                    print("Unsupported format, defaulting to PNG.")
                    file_extension = 'PNG'

                if not image.save(file_path, file_extension):
                    self.raise_error("Failed to save the image.")
        else:
            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Export, no baaaka!")

    def figure(self, event):
        if self.showing_image:
            self.play_mp3("sounds/figure.mp3")
            image = cv2.imread(self.showing_image)
            if (self.current_filter):
                window_name = f"figure_{self.showing_image.split("/")[-1].split('.')[0]}_{self.current_filter}"
            else:
                window_name = f"figure_{self.showing_image.split("/")[-1].split('.')[0]}"
            cv2.namedWindow(window_name)
            cv2.imshow(window_name, image)
        else:
            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Show, no baaaka!")

    def clear(self, event):
        if(self.showing_image):
            if self.current_filter == "":
                self.play_mp3("sounds/boom.mp3")
                self.raise_error("No Filter to clear, Baaaka!")
            else: self.play_mp3("sounds/clear.mp3")
            self.showing_image = self.file_name
            upload_pixmap = QPixmap(self.file_name).scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.upload_label.setPixmap(upload_pixmap)
            self.upload_label.setStyleSheet(f"""
                QLabel{{
                    background-color: #dd91b9;
                    border: {self.scale(8, 'h')}px solid #f1d3e3;
                    border-radius: {self.scale(23, 'h')}px;
                }}
            """)
            self.close_label.show()
            self.current_filter = ""

        else:
            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to clear, Baaaka!")

    def close_click(self, event):

        self.play_mp3("sounds/baa.mp3")

        if self.aspect_ratio != 16/9:
            self.upload_label.setScaledContents(True)

        self.showing_image = ""
        upload_pixmap = QPixmap('assets/upload.png').scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.upload_label.setPixmap(upload_pixmap)
        self.upload_label.setStyleSheet(f"""
            QLabel{{
                background-color: #dd91b9;
                border: 0px solid #f1d3e3;
                border-radius: {self.scale(23, 'h')}px;
            }}
        """)
        self.close_label.close()

    def img_click(self, event):
        self.play_mp3("sounds/button.mp3")
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        old_filename = self.file_name
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "./test-images/", "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.bmp)")

        if self.file_name:

            self.current_filter = ""

            self.upload_label.setScaledContents(False)
            self.showing_image = self.file_name
            upload_pixmap = QPixmap(self.file_name).scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.upload_label.setPixmap(upload_pixmap)
            self.upload_label.setStyleSheet(f"""
                QLabel{{
                    background-color: #dd91b9;
                    border: {self.scale(8, 'h')}px solid #f1d3e3;
                    border-radius: {self.scale(23, 'h')}px;
                }}
            """)
            self.close_label.show()
            self.play_mp3("sounds/waku.mp3")
        else:
            self.play_mp3("sounds/amongus.mp3")
            self.file_name = old_filename
            self.raise_error("no image selected, no baaaaaka!")

    def update(self):
        self.tree.clearFocus()
        self.tree.clearSelection()

    def loading(self):
        self.close_label.close()
        upload_pixmap = QPixmap('assets/loading.png').scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.upload_label.setPixmap(upload_pixmap)
        self.upload_label.setStyleSheet(f"""
            QLabel{{
                background-color: #dd91b9;
                border-radius: {self.scale(23, 'h')}px;
            }}
        """)
        QCoreApplication.processEvents()
        self.close_label.show()

    def showing_image_show(self):
        upload_pixmap = QPixmap(self.showing_image).scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.upload_label.setPixmap(upload_pixmap)
        self.upload_label.setStyleSheet(f"""
            QLabel{{
                background-color: #dd91b9;
                border: {self.scale(8, 'h')}px solid #f1d3e3;
                border-radius: {self.scale(23, 'h')}px;
            }}
        """)

    def plot_histogram(self, title, histogram, file_name):
        plt.figure()
        plt.title(title)
        plt.bar(np.arange(len(histogram)), histogram, width=1, color="#dd91b9")
        plt.savefig(file_name)
        plt.close()

    def on_item_click(self, item):

        if (item.text(0) in self.roots):

                self.play_mp3("sounds/button.mp3")

                if item.isExpanded():
                    item.setExpanded(False)
                else:
                    item.setExpanded(True)

        elif (item.text(0) == "RGB → Gray"):
            self.rgb_to_gray()

        elif (item.text(0) == "RGB → Binary"):
            self.rgb_to_binary()

        elif (item.text(0) in self.brightness_childs):
            self.apply_brightness(item.text(0))

        elif (item.text(0) == "Gamma Corrections"):
            self.gamma_correction()

        elif (item.text(0) in self.corrections_childs):
            self.apply_correction(item.text(0))

        elif (item.text(0) == "Original Histogram"):
            self.original_histogram()

        elif (item.text(0) == "Stretched Histogram"):
            self.stretched_histogram()

        elif (item.text(0) == "Equalized Histogram"):
            self.equalized_histogram()

        # QMessageBox.information(self, "Item Clicked", f"You clicked: {item.text(0)}")

    def apply_shadow_effect(self, button):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(0, 0, 0, 70))
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        button.setGraphicsEffect(shadow)

    def scale(self, size, dim):
        if dim in ['W', 'w']:
            return int(size / 1920 * self.monitor_width)
        elif dim in ['H', 'h']:
            return int(size / 1080 * self.monitor_height)
        else:
            raise ValueError("What is this dimention no baaaka!!!")

    def raise_error(self, message):
        error_window = error.ErrorWindow(self)
        error_window.error_message.setText(message)
        if not error_window.exec_(): self.play_mp3("sounds/baa.mp3")

    def play_mp3(self, path):
        mp3_url = QUrl.fromLocalFile(path)
        content = QMediaContent(mp3_url)
        self.player.setMedia(content)
        self.player.play()

    def stop_mp3(self):
        self.player.stop()

    def switch_item(self, item):
        if item.isExpanded():
            item.setExpanded(False)
        else:
            item.setExpanded(True)

    def rgb_to_binary(self):

        if self.showing_image:
            
            self.play_mp3("sounds/button.mp3")

            self.current_filter = "rgb-to-binary"

            dialog = dialoges.ColorConversionDialog.ColorConversionDialog(self)

            dialog.show()

            if dialog.exec_():
                self.play_mp3("sounds/button.mp3")
                self.loading()
                self.play_mp3('sounds/a41.mp3')

                red, green, blue, threshold = dialog.get_coefficients()
                self.showing_image = f"assets/output.{self.file_name.split('.')[-1]}"
                img.rgb_to_binary_pixel_processing(self.file_name, self.showing_image, red, green, blue, threshold)

                self.play_mp3('sounds/a42.mp3')


                self.showing_image_show()
            else: self.play_mp3("sounds/baa.mp3")

        else:

            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    def rgb_to_gray(self):

        if self.showing_image:

            self.play_mp3("sounds/button.mp3")

            self.current_filter = "rgb-to-gray"

            dialog = dialoges.ColorConversionDialog.ColorConversionDialog(self)

            dialog.threashhold_spin.close()
            dialog.threashhold_label.close()

            dialog.show()

            if dialog.exec_():
                self.play_mp3("sounds/button.mp3")
                self.loading()
                self.play_mp3('sounds/a41.mp3')
                red, green, blue, _ = dialog.get_coefficients()
                self.showing_image = f"assets/output.{self.file_name.split('.')[-1]}"
                img.rgb_to_gray_pixel_processing(self.file_name, self.showing_image, red, green, blue)
                self.play_mp3('sounds/a42.mp3')
                self.showing_image_show()
            else: self.play_mp3("sounds/baa.mp3")

        else:

            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    def apply_brightness(self, selection):

        if self.showing_image:

            self.play_mp3("sounds/button.mp3")

            self.current_filter = f"{selection.split(' ')[0].lower()}-brighness"

            dialog = dialoges.BrightnessDialog.BrightnessDialog(self)

            if selection == "Multiply value" or selection == "Divide value":
                dialog.brightness_spin.setValue(2)
            else:
                dialog.brightness_spin.setValue(128)

            dialog.show()

            if dialog.exec_():

                self.play_mp3("sounds/button.mp3")

                self.loading()

                brightness_value = dialog.get_coefficients()

                if brightness_value == 0:
                    self.raise_error("Can't Divide by Zero, no baaaka!")
                    self.showing_image_show()

                else:
                    self.play_mp3('sounds/a41.mp3')
                    self.showing_image = f"assets/output.{self.file_name.split('.')[-1]}"
                    img.brightness_operations(self.file_name, self.showing_image, selection, brightness_value)
                    self.stop_mp3()
                    self.play_mp3('sounds/a42.mp3')
                    self.showing_image_show()
            else: self.play_mp3("sounds/baa.mp3")

        else:

            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    def gamma_correction(self):

        if self.showing_image:

            self.play_mp3("sounds/button.mp3")

            self.current_filter = "gamma-correction"

            dialog = dialoges.GammaCorrectionDialog.GammaCorrectionDialog(self)

            dialog.show()

            if dialog.exec_():

                self.play_mp3("sounds/button.mp3")

                self.loading()
                self.play_mp3('sounds/a41.mp3')
                gamma = dialog.get_coefficients()

                self.showing_image = f"assets/output.{self.file_name.split('.')[-1]}"
                img.gamma_correction(self.file_name, self.showing_image, gamma)
                self.play_mp3('sounds/a42.mp3')
                self.showing_image_show()
            else: self.play_mp3("sounds/baa.mp3")
        else:
            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    def apply_correction(self, selection):

        if self.showing_image:

            self.play_mp3("sounds/button.mp3")

            self.current_filter = f"{selection.lower()}"

            self.loading()
            self.play_mp3('sounds/a41.mp3')
            self.showing_image = f"assets/output.{self.file_name.split('.')[-1]}"
            if(selection == "Log Corrections"):
                img.log_transform(self.file_name, self.showing_image)
            elif(selection == "Inverse Log"):
                img.inverse_log_transform(self.file_name, self.showing_image)
            elif(selection == "Complement"):
                img.complement(self.file_name, self.showing_image)
            self.play_mp3('sounds/a42.mp3')
            self.showing_image_show()
        else:
            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    def original_histogram(self):

        if self.showing_image:

            self.play_mp3("sounds/button.mp3")

            original_histogram = img.calculate_histogram(self.file_name)

            plot_file_name = f"assets/histogram_plot.{self.file_name.split('.')[-1]}"

            self.plot_histogram("Original Histogram", original_histogram, plot_file_name)

            histogram_image = cv2.imread(plot_file_name)

            self.play_mp3('sounds/a42.mp3')

            cv2.imshow("Original Histogram", histogram_image)

        else:

            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    def stretched_histogram(self):

        if self.showing_image:

            self.play_mp3("sounds/button.mp3")

            self.current_filter = "stretched-histogram"

            dialog = dialoges.HistogramDialog.HistogramDialog(self)

            dialog.show()

            if dialog.exec_():
                
                self.play_mp3("sounds/button.mp3")

                self.loading()
                self.play_mp3('sounds/a41.mp3')
                l, r = dialog.get_coefficients()

                self.showing_image = f"assets/output.{self.file_name.split('.')[-1]}"

                img.contrast_stretching(self.file_name, l, r, self.showing_image)

                stretched_histogram = img.calculate_histogram(self.showing_image)

                plot_file_name = f"assets/histogram_plot.{self.file_name.split('.')[-1]}"

                self.plot_histogram("Stretched Histogram", stretched_histogram, plot_file_name)

                stretched_histogram_image = cv2.imread(plot_file_name)

                cv2.imshow("Stretched Histogram", stretched_histogram_image)
                self.play_mp3('sounds/a42.mp3')
                self.showing_image_show()

            else: self.play_mp3("sounds/baa.mp3")

        else:

            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    def equalized_histogram(self):

        if self.showing_image:

            self.play_mp3("sounds/button.mp3")

            self.current_filter = "equalized-histogram"

            self.loading()
            self.play_mp3('sounds/a41.mp3')
            self.showing_image = f"assets/output.{self.file_name.split('.')[-1]}"

            img.histogram_equalization(self.file_name, self.showing_image)

            equalized_histogram = img.calculate_histogram(self.showing_image)

            plot_file_name = f"assets/histogram_plot.{self.file_name.split('.')[-1]}"

            self.plot_histogram("Equalized Histogram", equalized_histogram, plot_file_name)

            equalized_histogram_image = cv2.imread(plot_file_name)

            cv2.imshow("Equalized Histogram", equalized_histogram_image)
            self.play_mp3('sounds/a42.mp3')
            self.showing_image_show()

        else:

            self.play_mp3("sounds/boom.mp3")
            self.raise_error("No Image to Apply Filter on, Baaaka!")

    """   KawaīM —— o(*￣▽￣*)ブ   """
    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Escape:
        #     self.close()
        if event.key() == Qt.Key_I:
            self.info_click(self)
        elif event.key() == Qt.Key_C:
            self.clear(self)
        elif event.key() == Qt.Key_F:
            self.figure(self)
        elif event.key() == Qt.Key_X:
            self.export(self)
        elif event.key() == Qt.Key_A:
            self.img_click(self)
        elif event.key() == Qt.Key_R:
            self.close_click(self)
        elif event.key() == Qt.Key_V:
            self.play_mp3("sounds/button.mp3")
            self.switch_item(self.colors_conversions_root)
        elif event.key() == Qt.Key_P:
            self.play_mp3("sounds/button.mp3")
            self.switch_item(self.point_processing_root)
        elif event.key() == Qt.Key_B:
            self.play_mp3("sounds/button.mp3")
            self.switch_item(self.brightness_root)
        elif event.key() == Qt.Key_N:
            self.play_mp3("sounds/button.mp3")
            self.switch_item(self.corrections_root)
        elif event.key() == Qt.Key_H:
            self.play_mp3("sounds/button.mp3")
            self.switch_item(self.histogram_processing_root)
        elif event.key() == Qt.Key_F1:
            self.rgb_to_binary()
        elif event.key() == Qt.Key_F2:
            self.rgb_to_gray()
        elif event.key() == Qt.Key_F3:
            pass
        elif event.key() == Qt.Key_F4:
            self.apply_brightness("Add value")
        elif event.key() == Qt.Key_F5:
            self.apply_brightness("Multiply value")
        elif event.key() == Qt.Key_F5:
            self.apply_brightness("Subtract value")
        elif event.key() == Qt.Key_F6:
            self.apply_brightness("Divide value")
        elif event.key() == Qt.Key_F7:
            self.gamma_correction()
        elif event.key() == Qt.Key_F8:
            self.apply_correction("Log Corrections")
        elif event.key() == Qt.Key_F9:
            self.apply_correction("Inverse Log")
        elif event.key() == Qt.Key_F10:
            self.apply_correction("Complement")
        elif event.key() == Qt.Key_F11:
            self.original_histogram()
        elif event.key() == Qt.Key_F12:
            self.stretched_histogram()
        if event.key() == Qt.Key_1:
            self.equalized_histogram()
        elif event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_W:
                self.close()
            if event.key() == Qt.Key_M:
                self.showMinimized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KawaīFotoShoppu()
    window.show()
    sys.exit(app.exec_())
