
class Theme:
    def __init__(self):
        self.switch_to_theme_2()
    def switch_to_theme_1(self):
        self.image_assets = "../assets/chad-assets/images"
        self.sound_assets = "../assets/chad-assets/sounds"
        self.gif_assets = "../assets/chad-assets/gifs"
        self.main_color = "#484848"
        self.main_color_darken = "#292929"
        self.fg_color = "#ffffff"
        self.border_color = "#b6b6b6"
        self.main_hover = "#656565"
        self.main_darken_hover = "#3F3F3F"
    def switch_to_theme_2(self):
        self.image_assets = "../assets/kawaii-assets/images"
        self.sound_assets = "../assets/kawaii-assets/sounds"
        self.gif_assets = "../assets/kawaii-assets/gifs"
        self.main_color = "#DD91B9"
        self.main_color_darken = "#983569"
        self.fg_color = "#ffffff"
        self.border_color = "#f1d3e3"
        self.main_hover = "#e5a1c1"
        self.main_darken_hover = "#a93b74"

theme = Theme()