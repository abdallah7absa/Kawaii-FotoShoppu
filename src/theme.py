from PyQt5.QtCore import QSettings

class Theme:
    def __init__(self):
        self.settings = QSettings("img_team", "KawaīFotoShoppu")
        match self.settings.value("theme", 2):
            case 1:
                # self.switch_to_theme_1()
                pass
            case 2:
                self.switch_to_theme_2()
            case 3:
                # self.switch_to_theme_3()
                pass
            case 4:
                self.switch_to_theme_4()
            case _:
                print("Unreacheble")


    # def switch_to_theme_1(self):
    #     self.image_assets = "../assets/chad-assets/images"
    #     self.sound_assets = "../assets/chad-assets/sounds"
    #     self.gif_assets = "../assets/chad-assets/gifs"
    #     self.main_color = "#484848"
    #     self.main_color_darken = "#292929"
    #     self.fg_color = "#ffffff"
    #     self.border_color = "#b6b6b6"
    #     self.main_hover = "#656565"
    #     self.main_darken_hover = "#3F3F3F"
    #     self.close_info_color = "#ffffff"
    #     self.error_bg_color = "#0000ff"
    #     self.error_border_color = "#0000ff"
    #     self.close_error_color = "#0000ff"
    #     self.error_message_color = "#0000ff"
    #     self.border_width = 8
    #     self.border_radius = 23

    def switch_to_theme_2(self):
        self.image_assets = "../assets/kawaii-assets/images"
        self.sound_assets = "../assets/kawaii-assets/sounds"
        self.gif_assets = "../assets/kawaii-assets/gifs"
        self.main_color = "#DD91B9"
        self.main_color_darken = "#983569"
        self.fg_color = "#FFFFFF"
        self.border_color = "#f1d3e3"
        self.main_hover = "#e5a1c1"
        self.main_darken_hover = "#a93b74"
        self.close_info_color = "#000000"
        self.error_bg_color = "#983569"
        self.error_border_color = "#652345"
        self.close_error_color = "#f1d3e3"
        self.error_message_color = "#FFFFFF"
        self.border_width = 8
        self.border_radius = 23
        self.clear_border_width = 0
        self.clear_border_color = "#f1d3e3"
        self.clear_bg_color = "#983569"
        self.clear_text_color = "#FFFFFF"
        self.dialog_bg = "#FFFFFF"
        self.spin_bg = "#dd91b9"
        self.spin_text = "#FFFFFF"
        self.spin_border = "#983569"
        self.label_color = "#983569"
        self.button_bg = "#dd91b9"
        self.button_border = "#983569"
        self.button_hover = "#e5a1c1"
        self.button_pressed = "#c57b9a"
        self.dialog_border = "#FFFFFF"

    # def switch_to_theme_3(self):
    #     self.image_assets = "../assets/naruto-assets/images"
    #     self.sound_assets = "../assets/naruto-assets/sounds"
    #     self.gif_assets = "../assets/naruto-assets/gifs"
    #     self.main_color = "#C16839"
    #     self.main_color_darken = "#093C7D"
    #     self.fg_color = "#FFFFFF"
    #     self.border_color = "#093C7D"
    #     self.main_hover = "#E57B44"
    #     self.main_darken_hover = "#135DBC"
    #     self.close_info_color = "#D6D6D6"
    #     self.error_bg_color = "#104A95"
    #     self.error_border_color = "#0C2F5C"
    #     self.close_error_color = "#FFFFFF"
    #     self.error_message_color = "#FFFFFF"
    #     self.border_width = 8
    #     self.border_radius = 23

    def switch_to_theme_4(self):
        self.image_assets = "../assets/modern-assets/images"
        self.sound_assets = "../assets/modern-assets/sounds"
        self.gif_assets = "../assets/modern-assets/gifs"
        self.main_color = "#000000"
        self.main_color_darken = "#531111"
        self.fg_color = "#FFFFFF"
        self.border_color = "#FFFFFF"
        self.main_hover = "#151515"
        self.main_darken_hover = "#000000"
        self.close_info_color = "#FFFFFF"
        self.error_bg_color = "#040205"
        self.error_border_color = "#FFFFFF"
        self.close_error_color = "#FFFFFF"
        self.error_message_color = "#FFFFFF"
        self.border_width = 4
        self.border_radius = 7
        self.clear_border_width = 4
        self.clear_border_color = "#AA0000"
        self.clear_bg_color = "#000000"
        self.clear_text_color = "#AA0000"
        self.dialog_bg = "#000000"
        self.spin_bg = "#000000"
        self.spin_text = "#FFFFFF"
        self.spin_border = "#FFFFFF"
        self.label_color = "#FFFFFF"
        self.button_bg = "#000000"
        self.button_border = "#FFFFFF"
        self.button_hover = "#222222"
        self.button_pressed = "#000000"
        self.dialog_border = "#FFFFFF"

theme = Theme()
