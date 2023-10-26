from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication

from helpers.PyInstallerHelper import resource_path as rp


class BaseWindow:
    def load_theme(self, modo_escuro_habilitado: bool, theme_name: str = None):
        self.settings = QSettings("theme", "modo_escuro")
        theme = theme_name or self.settings.value("theme")

        print("Tema carregado:", theme,
              "| modo_escuro_habilitado = ", modo_escuro_habilitado)

        def apply_theme(theme: str):
            try:
                stylesheet_path = rp("styles/") + theme
                with open(stylesheet_path, "r") as f:
                    css_content = f.read()                    
                # Substitui os caminhos relativos por absolutos
                css_content = css_content.replace("url(styles/", "url(" + rp(
                    "styles/"))
                # Muda o separador de caminhos para a formatação de URL
                css_content = css_content.replace("\\", "/")  
                self.setStyleSheet(css_content)
            except:
                QApplication.instance().setStyle("Fusion")
                self.settings.setValue("modo_escuro", False)
            self.settings.setValue("theme", theme)

        if isinstance(theme, int) or theme is None:
            theme = "RsPaper dark.css" if modo_escuro_habilitado else \
                "RsPaper light.css"
            apply_theme(theme)

        elif theme in ["Fusion", "Windows", "WindowsVista"]:
            QApplication.instance().setStyle(theme)
            self.settings.setValue("modo_escuro", False)

        elif isinstance(theme, str):
            if modo_escuro_habilitado:
                if not theme.endswith("dark.css"):
                    theme = theme.replace("light.css", "dark.css")
            else:
                if not theme.endswith("light.css"):
                    theme = theme.replace("dark.css", "light.css")

            apply_theme(theme)
