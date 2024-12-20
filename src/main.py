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
import dialoges.SaltNoiseDialog
import dialoges.UniformNoiseDialog
import dialoges.GaussianNoiseDialog
import dialoges.OrderFiltersDialog
import dialoges.KernelSizeDialog
import dialoges.GrayToBinaryDialog
import dialoges.CutoffAndOrderDialog
import dialoges.CutoffDialog
from screeninfo import get_monitors
import error
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import info
from theme import theme


class KawaīFotoShoppu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("img_team", "KawaīFotoShoppu")
        theme.settings.setValue("filters", 0)

        monitors = get_monitors()
        for monitor in monitors:
            self.monitor_width = monitor.width
            self.monitor_height = monitor.height
        self.aspect_ratio = self.monitor_width / self.monitor_height

        self.setWindowTitle("Kawaī foto shoppu")
        self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))

        self.showFullScreen()

        self.bg_player = QMediaPlayer()

        self.player = QMediaPlayer()
        self.player2 = QMediaPlayer()

        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.monitor_width, self.monitor_height)

        self.bg_label.setScaledContents(True)
        self.bg_label.show()

        self.file_name = ""
        self.showing_image = ""
        self.current_filter = ""
        self.original_image = ""
        self.undo_stack = []
        self.redo_stack = []
        self.undo_active = False
        self.redo_active = False
        self.fft_image = None
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)

        left_layout = QVBoxLayout()
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_item_click)

        self.tree.setFixedSize(self.scale(550, 'w'), self.scale(1050, 'h'))
        left_layout.addWidget(self.tree)

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

        self.roots = ["Colors Conversions", "Point Processing", "Brightness", "Corrections", "Histogram Processing", "Noise Addition", "Local Processing", "Order Filters", "Blurring", "Edge Detection", "Sharpening", "Global Processing", "Fourier Transform", "Frequency Domain Filters"]
        self.brightness_childs = ["Add value", "Multiply value", "Subtract value", "Divide value"]
        self.corrections_childs = ["Log Corrections", "Inverse Log", "Complement"]
        self.noise_childs = ["Salt & Pepper Noise", "Uniform Noise", "Gaussian Noise"]

        self.point_processing_root = QTreeWidgetItem(self.tree)
        self.point_processing_root.setText(0, "Point Processing")
        self.point_processing_root.setFont(0, h1_font)

        self.colors_conversions_root = QTreeWidgetItem(self.point_processing_root)
        self.colors_conversions_root.setText(0, "Colors Conversions")
        self.colors_conversions_root.setFont(0, h2_font)

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

        self.noise_addition_root = QTreeWidgetItem(self.point_processing_root)
        self.noise_addition_root.setText(0, "Noise Addition")
        self.noise_addition_root.setFont(0, h2_font)

        salt_and_paper_child = QTreeWidgetItem(self.noise_addition_root)
        salt_and_paper_child.setText(0, "Salt & Pepper Noise")
        salt_and_paper_child.setFont(0, h3_font)

        uniform_noise_child = QTreeWidgetItem(self.noise_addition_root)
        uniform_noise_child.setText(0, "Uniform Noise")
        uniform_noise_child.setFont(0, h3_font)

        gaussian_noise_child = QTreeWidgetItem(self.noise_addition_root)
        gaussian_noise_child.setText(0, "Gaussian Noise")
        gaussian_noise_child.setFont(0, h3_font)

        self.local_processing_root = QTreeWidgetItem(self.tree)
        self.local_processing_root.setText(0, "Local Processing")
        self.local_processing_root.setFont(0, h1_font)

        self.order_filters_root = QTreeWidgetItem(self.local_processing_root)
        self.order_filters_root.setText(0, "Order Filters")
        self.order_filters_root.setFont(0, h2_font)

        min_filter_child = QTreeWidgetItem(self.order_filters_root)
        min_filter_child.setText(0, "Minimum Filter")
        min_filter_child.setFont(0, h3_font)

        max_filter_child = QTreeWidgetItem(self.order_filters_root)
        max_filter_child.setText(0, "Maximum Filter")
        max_filter_child.setFont(0, h3_font)

        median_filter_child = QTreeWidgetItem(self.order_filters_root)
        median_filter_child.setText(0, "Median Filter")
        median_filter_child.setFont(0, h3_font)

        mid_filter_child = QTreeWidgetItem(self.order_filters_root)
        mid_filter_child.setText(0, "Midpoint Filter")
        mid_filter_child.setFont(0, h3_font)

        self.blurring_root = QTreeWidgetItem(self.local_processing_root)
        self.blurring_root.setText(0, "Blurring")
        self.blurring_root.setFont(0, h2_font)

        blur_mean_filter_child = QTreeWidgetItem(self.blurring_root)
        blur_mean_filter_child.setText(0, "Mean Filter")
        blur_mean_filter_child.setFont(0, h3_font)

        blur_weighted_filter_child = QTreeWidgetItem(self.blurring_root)
        blur_weighted_filter_child.setText(0, "Weighted Filter")
        blur_weighted_filter_child.setFont(0, h3_font)

        self.edge_detection_root = QTreeWidgetItem(self.local_processing_root)
        self.edge_detection_root.setText(0, "Edge Detection")
        self.edge_detection_root.setFont(0, h2_font)

        point_edge_detection_child = QTreeWidgetItem(self.edge_detection_root)
        point_edge_detection_child.setText(0, "Point Detection")
        point_edge_detection_child.setFont(0, h3_font)

        horizontal_edge_detection_child = QTreeWidgetItem(self.edge_detection_root)
        horizontal_edge_detection_child.setText(0, "Horizontal Detection")
        horizontal_edge_detection_child.setFont(0, h3_font)

        vertical_edge_detection_child = QTreeWidgetItem(self.edge_detection_root)
        vertical_edge_detection_child.setText(0, "Vertical Detection")
        vertical_edge_detection_child.setFont(0, h3_font)

        diagonal_left_edge_detection_child = QTreeWidgetItem(self.edge_detection_root)
        diagonal_left_edge_detection_child.setText(0, "Diagonal Left Detection")
        diagonal_left_edge_detection_child.setFont(0, h3_font)

        diagonal_right_edge_detection_child = QTreeWidgetItem(self.edge_detection_root)
        diagonal_right_edge_detection_child.setText(0, "Diagonal Right Detection")
        diagonal_right_edge_detection_child.setFont(0, h3_font)

        self.sharpening_root = QTreeWidgetItem(self.local_processing_root)
        self.sharpening_root.setText(0, "Sharpening")
        self.sharpening_root.setFont(0, h2_font)

        point_sharpening_child = QTreeWidgetItem(self.sharpening_root)
        point_sharpening_child.setText(0, "Point Sharpening")
        point_sharpening_child.setFont(0, h3_font)

        horizontal_sharpening_child = QTreeWidgetItem(self.sharpening_root)
        horizontal_sharpening_child.setText(0, "Horizontal Sharpening")
        horizontal_sharpening_child.setFont(0, h3_font)

        vertical_sharpening_child = QTreeWidgetItem(self.sharpening_root)
        vertical_sharpening_child.setText(0, "Vertical Sharpening")
        vertical_sharpening_child.setFont(0, h3_font)

        diagonal_left_sharpening_child = QTreeWidgetItem(self.sharpening_root)
        diagonal_left_sharpening_child.setText(0, "Diagonal Left Sharpening")
        diagonal_left_sharpening_child.setFont(0, h3_font)

        diagonal_right_sharpening_child = QTreeWidgetItem(self.sharpening_root)
        diagonal_right_sharpening_child.setText(0, "Diagonal Right Sharpening")
        diagonal_right_sharpening_child.setFont(0, h3_font)

        self.global_processing_root = QTreeWidgetItem(self.tree)
        self.global_processing_root.setText(0, "Global Processing")
        self.global_processing_root.setFont(0, h1_font)

        self.fourier_transform_root = QTreeWidgetItem(self.global_processing_root)
        self.fourier_transform_root.setText(0, "Fourier Transform")
        self.fourier_transform_root.setFont(0, h2_font)

        fourier_transform_child = QTreeWidgetItem(self.fourier_transform_root)
        fourier_transform_child.setText(0, "Transform")
        fourier_transform_child.setFont(0, h3_font)

        inverse_fourier_transform_child = QTreeWidgetItem(self.fourier_transform_root)
        inverse_fourier_transform_child.setText(0, "Inverse Transform")
        inverse_fourier_transform_child.setFont(0, h3_font)

        self.frequency_domain_filters = QTreeWidgetItem(self.global_processing_root)
        self.frequency_domain_filters.setText(0, "Frequency Domain Filters")
        self.frequency_domain_filters.setFont(0, h2_font)

        ideal_low_pass_filter_child = QTreeWidgetItem(self.frequency_domain_filters)
        ideal_low_pass_filter_child.setText(0, "Ideal Low Pass Filter")
        ideal_low_pass_filter_child.setFont(0, h3_font)

        gaussian_low_pass_filter_child = QTreeWidgetItem(self.frequency_domain_filters)
        gaussian_low_pass_filter_child.setText(0, "Gaussian Low Pass Filter")
        gaussian_low_pass_filter_child.setFont(0, h3_font)

        butterworth_low_pass_filter_child = QTreeWidgetItem(self.frequency_domain_filters)
        butterworth_low_pass_filter_child.setText(0, "Butterworth Low Pass Filter")
        butterworth_low_pass_filter_child.setFont(0, h3_font)

        ideal_high_pass_filter_child = QTreeWidgetItem(self.frequency_domain_filters)
        ideal_high_pass_filter_child.setText(0, "Ideal High Pass Filter")
        ideal_high_pass_filter_child.setFont(0, h3_font)

        gaussian_high_pass_filter_child = QTreeWidgetItem(self.frequency_domain_filters)
        gaussian_high_pass_filter_child.setText(0, "Gaussian High Pass Filter")
        gaussian_high_pass_filter_child.setFont(0, h3_font)

        butterworth_high_pass_filter_child = QTreeWidgetItem(self.frequency_domain_filters)
        butterworth_high_pass_filter_child.setText(0, "Butterworth High Pass Filter")
        butterworth_high_pass_filter_child.setFont(0, h3_font)


        # self.tree.collapseAll()
        self.point_processing_root.setExpanded(False)
        self.local_processing_root.setExpanded(False)
        self.global_processing_root.setExpanded(False)

        main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(f"{theme.image_assets}/img.jpg")
        self.image_label.setPixmap(pixmap.scaled(self.scale(400, 'w'), self.scale(400, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        right_layout.addWidget(self.image_label)

        main_layout.addLayout(right_layout)

        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(self.scale(90, 'w'), self.scale(90, 'h'), self.scale(383, 'w'), self.scale(101, 'h'))
        self.logo_label.setScaledContents(True)
        self.logo_label.show()

        self.upload_label = QLabel(self)
        self.upload_label.setGeometry(self.scale(705, 'w'), self.scale(95, 'h'), self.scale(1027, 'w'), self.scale(806, 'h'))
        self.upload_label.setAlignment(Qt.AlignCenter)
        if self.aspect_ratio != 16/9:
            self.upload_label.setScaledContents(True)
        self.upload_label.show()
        self.upload_label.mousePressEvent = self.img_click

        self.apply_button = QPushButton("Export", self)
        self.apply_button.setGeometry(self.scale(709, 'w'), self.scale(914, 'h'), self.scale(225, 'w'), self.scale(81, 'h'))
        self.apply_button.show()
        self.apply_button.clicked.connect(self.export)

        self.show_figure_button = QPushButton("Show Figure", self)
        self.show_figure_button.setGeometry(self.scale(971, 'w'), self.scale(914, 'h'), self.scale(500, 'w'), self.scale(81, 'h'))
        self.show_figure_button.show()
        self.show_figure_button.clicked.connect(self.figure)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(self.scale(1507, 'w'), self.scale(914, 'h'), self.scale(225, 'w'), self.scale(81, 'h'))
        self.clear_button.show()
        self.clear_button.clicked.connect(self.clear)

        self.apply_shadow_effect(self.upload_label)
        self.apply_shadow_effect(self.apply_button)
        self.apply_shadow_effect(self.show_figure_button)
        self.apply_shadow_effect(self.clear_button)

        self.close_label = QLabel(self)
        self.close_label.setGeometry(self.scale(1650, 'w'), self.scale(123, 'h'), self.scale(60, 'w'), self.scale(60, 'h'))
        close_pixmap = QPixmap(f'{theme.image_assets}/close.png').scaled(self.scale(60, 'w'), self.scale(60, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.close_label.setPixmap(close_pixmap)
        self.close_label.setScaledContents(True)
        self.close_label.mousePressEvent = self.close_click

        self.info_label = QLabel(self)
        self.info_label.setGeometry(self.scale(435, 'w'), self.scale(951, 'h'), self.scale(40, 'w'), self.scale(40, 'h'))
        info_pixmap = QPixmap(f'{theme.image_assets}/info_button.png').scaled(self.scale(40, 'w'), self.scale(40, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.info_label.setPixmap(info_pixmap)
        self.info_label.setScaledContents(True)
        self.info_label.show()
        self.info_label.mousePressEvent = self.info_click

        self.undo_label = QLabel(self)
        self.undo_label.setGeometry(self.scale(735, 'w'), self.scale(134, 'h'), self.scale(40, 'w'), self.scale(38, 'h'))
        undo_pixmap = QPixmap(f'{theme.image_assets}/undo_inactive.png').scaled(self.scale(40, 'w'), self.scale(40, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.undo_label.setPixmap(undo_pixmap)
        self.undo_label.setScaledContents(True)
        self.undo_label.mousePressEvent = self.undo_click

        self.redo_label = QLabel(self)
        self.redo_label.setGeometry(self.scale(815, 'w'), self.scale(134, 'h'), self.scale(40, 'w'), self.scale(38, 'h'))
        redo_pixmap = QPixmap(f'{theme.image_assets}/redo_inactive.png').scaled(self.scale(40, 'w'), self.scale(40, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.redo_label.setPixmap(redo_pixmap)
        self.redo_label.setScaledContents(True)
        self.redo_label.mousePressEvent = self.redo_click

        self.undo_redo_splitter = QFrame(self)
        self.undo_redo_splitter.setGeometry(self.scale(795, 'w'), self.scale(128, 'w'), self.scale(3, 'w'), self.scale(50, 'w'))
        self.undo_redo_splitter.setFrameShape(QFrame.VLine)
        self.undo_redo_splitter.setFrameShadow(QFrame.Plain)
        self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.2)")

        fps = 15
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(1000//fps)
        self.timer.start()

        self.update_theme()


    def info_click(self, event):
        self.play_mp3(f"{theme.sound_assets}/button.mp3")
        info_window = info.Info()
        if not info_window.exec_(): self.play_mp3(f"{theme.sound_assets}/baa.mp3")

    def export(self, event):
        if self.showing_image:
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
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
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Export, no baaaka!")

    def figure(self, event):
        if self.showing_image:
            self.play_mp3(f"{theme.sound_assets}/figure.mp3")
            image = cv2.imread(self.showing_image)
            if (self.current_filter):
                window_name = f"figure_{self.showing_image.split("/")[-1].split('.')[0]}{self.current_filter}"
            else:
                window_name = f"figure_{self.showing_image.split("/")[-1].split('.')[0]}"
            cv2.namedWindow(window_name)
            cv2.imshow(window_name, image)
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Show, no baaaka!")

    def clear(self, event):
        if len(self.undo_stack) == 0:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("This is already the original image, no baaaka!")
            return
        if(self.showing_image):
            if self.current_filter == "":
                self.play_mp3(f"{theme.sound_assets}/boom.mp3")
                self.raise_error("No Filter to clear, Baaaka!")
            else:
                theme.settings.setValue("filters", 0)
                self.play_mp3(f"{theme.sound_assets}/clear.mp3")
            self.showing_image = self.original_image
            upload_pixmap = QPixmap(self.original_image).scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.upload_label.setPixmap(upload_pixmap)
            self.upload_label.setStyleSheet(f"""
                QLabel{{
                    background-color: {theme.main_color};
                    border: {self.scale(theme.border_width, 'h')}px solid {theme.border_color};
                    border-radius: {self.scale(theme.border_radius, 'h')}px;
                }}
            """)
            self.close_label.show()
            self.undo_label.show()
            self.redo_label.show()
            self.undo_redo_splitter.show()
            self.undo_stack = []
            self.redo_stack = []
            self.current_filter = ""
            self.undo_active = False
            self.redo_active = False
            redo_pixmap = QPixmap(f'{theme.image_assets}/redo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.redo_label.setPixmap(redo_pixmap)
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.undo_label.setPixmap(undo_pixmap)
            if self.redo_active or self.undo_active:
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")
            else:
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.2)")

        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to clear, Baaaka!")

    def close_click(self, event):

        theme.settings.setValue("filters", 0)

        if self.showing_image:
            self.play_mp3(f"{theme.sound_assets}/baa.mp3")

            if self.aspect_ratio != 16/9:
                self.upload_label.setScaledContents(True)

            self.showing_image = ""
            upload_pixmap = QPixmap(f'{theme.image_assets}/upload.png').scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.upload_label.setPixmap(upload_pixmap)
            self.upload_label.setStyleSheet(f"""
                QLabel{{
                    background-color: {theme.main_color};
                    border: 0px solid {theme.border_color};
                    border-radius: {self.scale(theme.border_radius, 'h')}px;
                }}
            """)
            self.close_label.close()
            self.undo_label.close()
            self.redo_label.close()
            self.undo_redo_splitter.close()
            self.undo_stack = []
            self.redo_stack = []
            self.undo_active = False
            self.redo_active = False
            redo_pixmap = QPixmap(f'{theme.image_assets}/redo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.redo_label.setPixmap(redo_pixmap)
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.undo_label.setPixmap(undo_pixmap)
            if self.redo_active or self.undo_active:
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")
            else:
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.2)")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Remove, no baaaka!")

    def img_click(self, event):
        self.play_mp3(f"{theme.sound_assets}/button.mp3")
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        old_filename = self.file_name
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "../test-images/", "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.bmp)")

        if self.file_name:
            
            theme.settings.setValue("filters", 0)

            self.original_image = self.file_name

            self.current_filter = ""

            self.upload_label.setScaledContents(False)
            self.showing_image = self.file_name
            upload_pixmap = QPixmap(self.file_name).scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.upload_label.setPixmap(upload_pixmap)
            self.upload_label.setStyleSheet(f"""
                QLabel{{
                    background-color: {theme.main_color};
                    border: {self.scale(theme.border_width, 'h')}px solid {theme.border_color};
                    border-radius: {self.scale(theme.border_radius, 'h')}px;
                }}
            """)
            self.close_label.show()
            self.undo_label.show()
            self.redo_label.show()
            self.undo_redo_splitter.show()
            self.undo_stack = []
            self.redo_stack = []
            self.undo_active = False
            self.redo_active = False
            redo_pixmap = QPixmap(f'{theme.image_assets}/redo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.redo_label.setPixmap(redo_pixmap)
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.undo_label.setPixmap(undo_pixmap)
            if self.redo_active or self.undo_active:
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")
            else:
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.2)")
            self.play_mp3(f"{theme.sound_assets}/waku.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/amongus.mp3")
            self.file_name = old_filename
            self.raise_error("no image selected, no baaaaaka!")

    def update(self):
        self.tree.clearFocus()
        self.tree.clearSelection()

    def loading(self):
        self.close_label.close()
        self.undo_label.close()
        self.redo_label.close()
        self.undo_redo_splitter.close()
        upload_pixmap = QPixmap(f'{theme.image_assets}/loading.png').scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.upload_label.setPixmap(upload_pixmap)
        self.upload_label.setStyleSheet(f"""
            QLabel{{
                background-color: {theme.main_color};
                border-radius: {self.scale(theme.border_radius, 'h')}px;
            }}
        """)
        QCoreApplication.processEvents()
        self.close_label.show()
        self.undo_label.show()
        self.redo_label.show()
        self.undo_redo_splitter.show()
    def showing_image_show(self):
        upload_pixmap = QPixmap(self.showing_image).scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.upload_label.setPixmap(upload_pixmap)
        self.upload_label.setStyleSheet(f"""
            QLabel{{
                background-color: {theme.main_color};
                border: {self.scale(theme.border_width, 'h')}px solid {theme.border_color};
                border-radius: {self.scale(theme.border_radius, 'h')}px;
            }}
        """)

    def plot_histogram(self, title, histogram, file_name):
        plt.figure()
        plt.title(title)
        plt.bar(np.arange(len(histogram)), histogram, width = 1, color = theme.main_color)
        plt.savefig(file_name)
        plt.close()

    def on_item_click(self, item):

        if (item.text(0) in self.roots):

                self.play_mp3(f"{theme.sound_assets}/button.mp3")

                if item.isExpanded():
                    item.setExpanded(False)
                else:
                    item.setExpanded(True)

        elif (item.text(0) == "RGB → Gray"):
            self.rgb_to_gray()

        elif (item.text(0) == "RGB → Binary"):
            self.rgb_to_binary()

        elif (item.text(0) == "Gray → Binary"):
            self.gray_to_binary()

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

        elif (item.text(0) == "Salt & Pepper Noise"):
            self.salt_and_pepper_noise()

        elif (item.text(0) == "Uniform Noise"):
            self.uniform_noise()

        elif (item.text(0) == "Gaussian Noise"):
            self.gaussian_noise()

        elif (item.text(0) == "Minimum Filter"):
            self.min_filter()

        elif (item.text(0) == "Maximum Filter"):
            self.max_filter()

        elif (item.text(0) == "Median Filter"):
            self.med_filter()

        elif (item.text(0) == "Midpoint Filter"):
            self.mid_filter()

        elif (item.text(0) == "Mean Filter"):
            self.blur_mean_filter()

        elif (item.text(0) == "Weighted Filter"):
            self.blur_weight_filter()

        elif (item.text(0) == "Point Detection"):
            self.point_detection()

        elif (item.text(0) == "Horizontal Detection"):
            self.horizontal_detection()

        elif (item.text(0) == "Vertical Detection"):
            self.vertical_detection()

        elif (item.text(0) == "Diagonal Left Detection"):
            self.diagonal_left_detection()

        elif (item.text(0) == "Diagonal Right Detection"):
            self.diagonal_right_detection()

        elif (item.text(0) == "Point Sharpening"):
            self.point_sharpening()

        elif (item.text(0) == "Horizontal Sharpening"):
            self.horizontal_sharpening()

        elif (item.text(0) == "Vertical Sharpening"):
            self.vertical_sharpening()

        elif (item.text(0) == "Diagonal Left Sharpening"):
            self.diagonal_left_sharpening()

        elif (item.text(0) == "Diagonal Right Sharpening"):
            self.diagonal_right_sharpening()

        elif (item.text(0) == "Transform"):
            self.fourier_transform()

        elif (item.text(0) == "Inverse Transform"):
            self.inverse_fourier_transform()

        elif (item.text(0) == "Ideal Low Pass Filter"):
            self.ideal_low_pass_filter()

        elif (item.text(0) == "Ideal High Pass Filter"):
            self.ideal_high_pass_filter()

        elif (item.text(0) == "Gaussian Low Pass Filter"):
            self.gaussian_low_pass_filter()

        elif (item.text(0) == "Gaussian High Pass Filter"):
            self.gaussian_high_pass_filter()

        elif (item.text(0) == "Butterworth Low Pass Filter"):
            self.butterworth_low_pass_filter()

        elif (item.text(0) == "Butterworth High Pass Filter"):
            self.butterworth_high_pass_filter()


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
        if not error_window.exec_(): self.play_mp3(f"{theme.sound_assets}/baa.mp3")

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
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-rgb-to-binary"

            dialog = dialoges.ColorConversionDialog.ColorConversionDialog(self)

            dialog.show()

            if dialog.exec_():

                red, green, blue, threshold = dialog.get_coefficients()

                if red + green + blue > 1:
                    self.play_mp3(f"{theme.sound_assets}/boom.mp3")
                    self.raise_error("Coefficients Sum must be <= 1, Baaaka!")

                else:
                    mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                    content = QMediaContent(mp3_url)
                    self.player2.setMedia(content)
                    self.player2.play()
                    # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                    self.loading()
                    self.play_mp3(f'{theme.sound_assets}/a41.mp3')

                    if self.settings.value("filters", 0) == 0:
                        self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                    else:
                        self.file_name = self.showing_image

                    img.rgb_to_binary_pixel_processing(self.file_name, self.showing_image, red, green, blue, threshold)
                    self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                    self.showing_image_show()
                    theme.settings.setValue("filters", 1)
                    self.new_image = cv2.imread(self.showing_image)
                    self.undo_stack.append(self.new_image)
                    self.undo_active = True
                    undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.undo_label.setPixmap(undo_pixmap)
                    self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def rgb_to_gray(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-rgb-to-gray"

            dialog = dialoges.ColorConversionDialog.ColorConversionDialog(self)

            dialog.threashhold_spin.close()
            dialog.threashhold_label.close()

            dialog.show()

            if dialog.exec_():

                red, green, blue, _ = dialog.get_coefficients()

                if red + green + blue > 1:
                    self.play_mp3(f"{theme.sound_assets}/boom.mp3")
                    self.raise_error("Coefficients Sum must be <= 1, Baaaka!")

                else:
                    mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                    content = QMediaContent(mp3_url)
                    self.player2.setMedia(content)
                    self.player2.play()
                    # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                    self.loading()
                    self.play_mp3(f'{theme.sound_assets}/a41.mp3')

                    if self.settings.value("filters", 0) == 0:
                        self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                    else:
                        self.file_name = self.showing_image

                    img.rgb_to_gray_pixel_processing(self.file_name, self.showing_image, red, green, blue)
                    self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                    self.showing_image_show()
                    theme.settings.setValue("filters", 1)
                    self.new_image = cv2.imread(self.showing_image)
                    self.undo_stack.append(self.new_image)
                    self.undo_active = True
                    undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.undo_label.setPixmap(undo_pixmap)
                    self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def gray_to_binary(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-gray-to-binary"

            dialog = dialoges.GrayToBinaryDialog.GrayToBinaryDialog(self)

            dialog.show()

            if dialog.exec_():

                threshold = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image

                img.gray_to_binary_pixel_processing(self.file_name, self.showing_image, threshold)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def apply_brightness(self, selection):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += f"-{selection.split(' ')[0].lower()}-brighness"

            dialog = dialoges.BrightnessDialog.BrightnessDialog(self)

            if selection == "Multiply value" or selection == "Divide value":
                dialog.brightness_spin.setValue(2)
            else:
                dialog.brightness_spin.setValue(128)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()

                brightness_value = dialog.get_coefficients()

                if brightness_value == 0:
                    self.showing_image_show()
                    theme.settings.setValue("filters", 1)
                    self.play_mp3(f'{theme.sound_assets}/boom.mp3')
                    self.raise_error("Can't Divide by Zero, no baaaka!")

                else:
                    self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                    if self.settings.value("filters", 0) == 0:
                        self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                    else:
                        self.file_name = self.showing_image
                    img.brightness_operations(self.file_name, self.showing_image, selectino, brightness_value)
                    self.stop_mp3()
                    self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                    self.showing_image_show()
                    theme.settings.setValue("filters", 1)
                    self.new_image = cv2.imread(self.showing_image)
                    self.undo_stack.append(self.new_image)
                    self.undo_active = True
                    undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.undo_label.setPixmap(undo_pixmap)
                    self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def gamma_correction(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-gamma-correction"

            dialog = dialoges.GammaCorrectionDialog.GammaCorrectionDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                gamma = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.gamma_correction(self.file_name, self.showing_image, gamma)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def apply_correction(self, selection):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += f"-{selection.lower()}"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            if(selection == "Log Corrections"):
                img.log_transform(self.file_name, self.showing_image)
            elif(selection == "Inverse Log"):
                img.inverse_log_transform(self.file_name, self.showing_image)
            elif(selection == "Complement"):
                img.complement(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def original_histogram(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            original_histogram = img.calculate_histogram(self.file_name)

            plot_file_name = f"{theme.image_assets}/histogram_plot.{self.file_name.split('.')[-1]}"

            self.plot_histogram("Original Histogram", original_histogram, plot_file_name)

            histogram_image = cv2.imread(plot_file_name)

            self.play_mp3(f'{theme.sound_assets}/a42.mp3')

            cv2.imshow("Original Histogram", histogram_image)

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def stretched_histogram(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-stretched-histogram"

            dialog = dialoges.HistogramDialog.HistogramDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                l, r = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image

                img.contrast_stretching(self.file_name, l, r, self.showing_image)

                stretched_histogram = img.calculate_histogram(self.showing_image)

                plot_file_name = f"{theme.image_assets}/histogram_plot.{self.file_name.split('.')[-1]}"

                self.plot_histogram("Stretched Histogram", stretched_histogram, plot_file_name)

                stretched_histogram_image = cv2.imread(plot_file_name)

                cv2.imshow("Stretched Histogram", stretched_histogram_image)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def equalized_histogram(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-equalized-histogram"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"

            img.histogram_equalization(self.file_name, self.showing_image)

            equalized_histogram = img.calculate_histogram(self.showing_image)

            plot_file_name = f"{theme.image_assets}/histogram_plot.{self.file_name.split('.')[-1]}"

            self.plot_histogram("Equalized Histogram", equalized_histogram, plot_file_name)

            equalized_histogram_image = cv2.imread(plot_file_name)

            cv2.imshow("Equalized Histogram", equalized_histogram_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def salt_and_pepper_noise(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-salt-and-pepper-noise"

            dialog = dialoges.SaltNoiseDialog.SaltNoiseDialog(self)

            dialog.show()

            if dialog.exec_():

                amount, salt_vs_pepper = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.salt_and_pepper_noise(self.file_name, self.showing_image, amount, salt_vs_pepper)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def uniform_noise(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-uniform-noise"

            dialog = dialoges.UniformNoiseDialog.UniformNoiseDialog(self)

            dialog.show()

            if dialog.exec_():

                noise_range = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.uniform_noise(self.file_name, self.showing_image, noise_range)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def gaussian_noise(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-gaussian-noise"

            dialog = dialoges.GaussianNoiseDialog.GaussianNoiseDialog(self)

            dialog.show()

            if dialog.exec_():

                mean, std_dev = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.gaussian_noise(self.file_name, self.showing_image, mean, std_dev)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def min_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-min-filter"

            dialog = dialoges.OrderFiltersDialog.OrderFiltersDialog(self)

            dialog.show()

            if dialog.exec_():

                ksize = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.min_filter(self.file_name, self.showing_image, ksize)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def max_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-max-filter"

            dialog = dialoges.OrderFiltersDialog.OrderFiltersDialog(self)

            dialog.show()

            if dialog.exec_():

                ksize = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.max_filter(self.file_name, self.showing_image, ksize)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def med_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-med-filter"

            dialog = dialoges.OrderFiltersDialog.OrderFiltersDialog(self)

            dialog.show()

            if dialog.exec_():

                ksize = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.median_filter(self.file_name, self.showing_image, ksize)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def mid_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-mid-filter"

            dialog = dialoges.OrderFiltersDialog.OrderFiltersDialog(self)

            dialog.show()

            if dialog.exec_():

                ksize = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.midpoint_filter(self.file_name, self.showing_image, ksize)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def blur_mean_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-blur-mean-filter"

            dialog = dialoges.KernelSizeDialog.KernelSizeDialog(self)

            dialog.show()

            if dialog.exec_():

                ksize = dialog.get_coefficients()
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")
                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.blurring_mean_filter(self.file_name, self.showing_image, (ksize, ksize))
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")

        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def blur_weight_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-blur-weight-filter"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.blurring_weight_filter(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def point_detection(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-point-detection"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.point_edge_detection(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def horizontal_detection(self):
        if self.showing_image:

            # TODO: MAKE NEW PLAYER FOR BUTTON CLICK
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-horizontal-detection"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.horizontal_edge_detection(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def vertical_detection(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-vertical-detection"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.vertical_edge_detection(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def diagonal_left_detection(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-diagonal-left-detection"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.diagonal_left_edge_detection(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def diagonal_right_detection(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-diagonal-right-detection"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.diagonal_right_edge_detection(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def point_sharpening(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-point-sharpening"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.point_sharpening(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def horizontal_sharpening(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-horizontal-sharpening"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.horizontl_sharpening(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def vertical_sharpening(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-vertical-sharpening"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.vertical_sharpening(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def diagonal_left_sharpening(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-diagonal-left-sharpening"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.diagonal_left_sharpening(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def diagonal_right_sharpening(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-diagonal-right-sharpening"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            img.diagonal_right_sharpening(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def fourier_transform(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-fourier-transform"

            self.loading()
            self.play_mp3(f'{theme.sound_assets}/a41.mp3')
            if self.settings.value("filters", 0) == 0:
                self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
            else:
                self.file_name = self.showing_image
            self.fft_image = img.fft_image(self.file_name, self.showing_image)
            self.play_mp3(f'{theme.sound_assets}/a42.mp3')
            self.showing_image_show()
            theme.settings.setValue("filters", 1)
            self.new_image = cv2.imread(self.showing_image)
            self.undo_stack.append(self.new_image)
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")


        else:

            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def inverse_fourier_transform(self):
        if self.fft_image is not None:
            if self.showing_image:
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.current_filter += "-inverse-fourier-transform"

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.ifft_image(self.fft_image, self.showing_image)
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else:

                self.play_mp3(f"{theme.sound_assets}/boom.mp3")
                self.raise_error("No Image to Apply Filter no, Baaaka!")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Fourier Transformed Image no, Baaaka!")

    def ideal_low_pass_filter(self):

        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-ideal-low-pass"

            dialog = dialoges.CutoffDialog.CutoffDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                cutoff = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.ideal_filter(self.file_name, self.showing_image, cutoff, "low")
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def ideal_high_pass_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-ideal-low-pass"

            dialog = dialoges.CutoffDialog.CutoffDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                cutoff = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.ideal_filter(self.file_name, self.showing_image, cutoff, "high")
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def gaussian_low_pass_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-ideal-low-pass"

            dialog = dialoges.CutoffDialog.CutoffDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                cutoff = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.gaussian_filter(self.file_name, self.showing_image, cutoff, "low")
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def gaussian_high_pass_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-ideal-low-pass"

            dialog = dialoges.CutoffDialog.CutoffDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                cutoff = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.gaussian_filter(self.file_name, self.showing_image, cutoff, "high")
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def butterworth_low_pass_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-ideal-low-pass"

            dialog = dialoges.CutoffAndOrderDialog.CutoffAndOrderDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                cutoff, order = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.butterworth_filter(self.file_name, self.showing_image, cutoff, order, "low")
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def butterworth_high_pass_filter(self):
        if self.showing_image:
            mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
            content = QMediaContent(mp3_url)
            self.player2.setMedia(content)
            self.player2.play()
            # self.play_mp3(f"{theme.sound_assets}/button.mp3")

            self.current_filter += "-ideal-low-pass"

            dialog = dialoges.CutoffAndOrderDialog.CutoffAndOrderDialog(self)

            dialog.show()

            if dialog.exec_():
                mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/button.mp3")
                content = QMediaContent(mp3_url)
                self.player2.setMedia(content)
                self.player2.play()
                # self.play_mp3(f"{theme.sound_assets}/button.mp3")

                self.loading()
                self.play_mp3(f'{theme.sound_assets}/a41.mp3')
                cutoff, order = dialog.get_coefficients()

                if self.settings.value("filters", 0) == 0:
                    self.showing_image = f"{theme.image_assets}/output.{self.file_name.split('.')[-1]}"
                else:
                    self.file_name = self.showing_image
                img.butterworth_filter(self.file_name, self.showing_image, cutoff, order, "high")
                self.play_mp3(f'{theme.sound_assets}/a42.mp3')
                self.showing_image_show()
                theme.settings.setValue("filters", 1)
                self.new_image = cv2.imread(self.showing_image)
                self.undo_stack.append(self.new_image)
                self.undo_active = True
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")

            else: self.play_mp3(f"{theme.sound_assets}/baa.mp3")
        else:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("No Image to Apply Filter no, Baaaka!")

    def update_theme(self):
        mp3_url = QUrl.fromLocalFile(f"{theme.sound_assets}/bg.mp3")
        content = QMediaContent(mp3_url)
        self.bg_player.setMedia(content)
        self.bg_player.play()

        if self.showing_image:
            self.showing_image_show()
        else:
            upload_pixmap = QPixmap(f'{theme.image_assets}/upload.png').scaled(self.scale(1027, 'w'), self.scale(806, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.upload_label.setPixmap(upload_pixmap)
            self.upload_label.setStyleSheet(f"""
            QLabel{{
                background-color: {theme.main_color};
                border-radius: {self.scale(theme.border_radius, 'h')}px;
            }}
        """)
        logo_pixmap = QPixmap(f'{theme.image_assets}/logo2.png').scaled(self.scale(383, 'w'), self.scale(101, 'h'), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)

        bg_pixmap = QPixmap(f'{theme.image_assets}/bg.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))

        if self.undo_active:
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)
        else:
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.undo_label.setPixmap(undo_pixmap)

        if self.redo_active:
            redo_pixmap = QPixmap(f'{theme.image_assets}/redo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.redo_label.setPixmap(redo_pixmap)
        else:
            redo_pixmap = QPixmap(f'{theme.image_assets}/redo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.redo_label.setPixmap(redo_pixmap)

        if self.redo_active or self.undo_active:
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")
        else:
            self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.2)")



        self.bg_label.setPixmap(bg_pixmap)
        self.apply_button.setStyleSheet(f"""
            QPushButton{{background-color: {theme.main_color};
                        color: {theme.fg_color};
                        font-size: {self.scale(25, 'w')}px;
                        font-weight: bold;
                        border: {self.scale(theme.border_width, 'h')}px solid {theme.border_color};
                        border-radius: {self.scale(theme.border_radius, 'h')}px;}}
            QPushButton:hover {{
                background-color: {theme.main_hover};
            }}
        """)
        cursor_image = QPixmap(f'{theme.image_assets}/cursor.png')
        custom_cursor = QCursor(cursor_image)
        QApplication.setOverrideCursor(custom_cursor)
        self.clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.clear_bg_color};
                color: {theme.clear_text_color};
                font-size: {self.scale(25, 'w')}px;
                font-weight: bold;
                border: {self.scale(theme.clear_border_width, 'h')}px solid {theme.clear_border_color};
                border-radius: {self.scale(theme.border_radius, 'h')}px;
            }}
            QPushButton:hover {{
                background-color: {theme.main_darken_hover};
            }}
        """)
        self.show_figure_button.setStyleSheet(f"""
            QPushButton {{background-color: {theme.main_color};
                        color: {theme.fg_color};
                        font-size: {self.scale(25, 'w')}px;
                        font-weight: bold;
                        border: {self.scale(theme.border_width, 'h')}px solid {theme.border_color};
                        border-radius: {self.scale(theme.border_radius, 'h')}px;}}
            QPushButton:hover {{
                background-color: {theme.main_hover};
            }}
        """)
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                margin: {self.scale(50, 'h')}px;
                background-color: {theme.main_color};
                color: {theme.fg_color};
                border: {self.scale(theme.border_width, 'h')}px solid {theme.border_color};
                border-radius: {self.scale(theme.border_radius, 'h')}px;
                padding-top: {self.scale(150, 'h')}px;
                padding-left: {self.scale(10, 'w')}px;
            }}
            QTreeWidget::item:hover {{
                background-color: {theme.fg_color};
                color: {theme.main_color};
            }}
            QScrollBar:vertical {{
                background-color: {theme.main_color};
                width: {self.scale(20, 'w')}px;
                margin: 0 {self.scale(9, 'h')}px {self.scale(25, 'w')}px 0;
                border-radius: {self.scale(theme.border_radius, 'h')}px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {theme.fg_color};
                min-height: {self.scale(20, 'h')}px;
                border-radius: {self.scale(theme.border_radius, 'h')}px;
            }}
            QScrollBar:horizontal {{
                background-color: {theme.main_color};
                height: {self.scale(12, 'h')}px;
                margin: 0px;
                border-radius: {self.scale(theme.border_radius, 'h')}px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {theme.fg_color};
                min-width: {self.scale(20, 'w')}px;
                border-radius: {self.scale(theme.border_radius, 'h')}px;
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
                color: {theme.fg_color};
                padding: 1px;
            }}
            QTreeWidget::item:selected {{
                background-color: {theme.main_color};
                color: {theme.fg_color};
                outline: none;
            }}
            QTreeWidget::item:selected:active {{
                background-color: {theme.main_color};
                color: {theme.fg_color};
            }}
            QTreeWidget::item:selected:!active {{
                background-color: {theme.main_color};
                color: {theme.fg_color};
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                image: url({theme.image_assets}/right.png);
                height: 20px;
                width: 20px;
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                image: url({theme.image_assets}/down.png);
                height: 20px;
                width: 20px;
            }}
        """)

    def undo_click(self, event):

        if len(self.undo_stack) == 0:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("Nothing to undo, no baaaka!")

        else:
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
            if len(self.undo_stack) == 1:
                theme.settings.setValue("filters", 0)
                self.redo_active = True
                self.undo_active = False
                redo_pixmap = QPixmap(f'{theme.image_assets}/redo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.redo_label.setPixmap(redo_pixmap)
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
                self.undo_label.setPixmap(undo_pixmap)
                if self.redo_active or self.undo_active:
                    self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")
                else:
                    self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.2)")
                self.redo_stack.append(self.undo_stack.pop())
                self.showing_image = self.original_image
                self.showing_image_show()
                return

            self.redo_active = True
            redo_pixmap = QPixmap(f'{theme.image_assets}/redo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.redo_label.setPixmap(redo_pixmap)
            self.redo_stack.append(self.undo_stack.pop())
            cv2.imwrite(f"{theme.image_assets}/stack.png", self.undo_stack[-1])
            self.showing_image = f"{theme.image_assets}/stack.png"
            self.showing_image_show()

    def redo_click(self, event):
        if len(self.redo_stack) == 0:
            self.play_mp3(f"{theme.sound_assets}/boom.mp3")
            self.raise_error("Nothing to redo, no baaaka!")
        else:
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
            if len(self.redo_stack) == 1:
                theme.settings.setValue("filters", 1)
                self.undo_active = True
                self.redo_active = False
                redo_pixmap = QPixmap(f'{theme.image_assets}/redo_inactive.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.redo_label.setPixmap(redo_pixmap)
                undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.undo_label.setPixmap(undo_pixmap)
                if self.redo_active or self.undo_active:
                    self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid rgba(255, 255, 255, 1)")
                else:
                    self.undo_redo_splitter.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.2)")
                self.undo_stack.append(self.redo_stack.pop())
                cv2.imwrite(f"{theme.image_assets}/stack.png", self.undo_stack[-1])
                self.showing_image = f"{theme.image_assets}/stack.png"
                self.showing_image_show()
                return
            self.undo_active = True
            undo_pixmap = QPixmap(f'{theme.image_assets}/undo_active.png').scaled(self.monitor_width, self.monitor_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(f'{theme.image_assets}/icon.png'))
            self.undo_label.setPixmap(undo_pixmap)
            self.undo_stack.append(self.redo_stack.pop())
            cv2.imwrite(f"{theme.image_assets}/stack.png", self.undo_stack[-1])
            self.showing_image = f"{theme.image_assets}/stack.png"
            self.showing_image_show()

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
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
            self.switch_item(self.colors_conversions_root)
        elif event.key() == Qt.Key_P:
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
            self.switch_item(self.point_processing_root)
        elif event.key() == Qt.Key_B:
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
            self.switch_item(self.brightness_root)
        elif event.key() == Qt.Key_N:
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
            self.switch_item(self.corrections_root)
        elif event.key() == Qt.Key_H:
            self.play_mp3(f"{theme.sound_assets}/button.mp3")
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
        # elif event.key() == Qt.Key_L:
        #     theme.settings.setValue("theme", 1)
        #     theme.switch_to_theme_1()
        #     self.update_theme()
        elif event.key() == Qt.Key_K:
            theme.settings.setValue("theme", 2)
            theme.switch_to_theme_2()
            self.update_theme()
        # elif event.key() == Qt.Key_J:
        #     theme.settings.setValue("theme", 3)
        #     theme.switch_to_theme_3()
        #     self.update_theme()
        elif event.key() == Qt.Key_L:
            theme.settings.setValue("theme", 4)
            theme.switch_to_theme_4()
            self.update_theme()
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
