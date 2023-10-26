import os

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QTabWidget, QWidget, \
    QVBoxLayout, QComboBox, QLabel, QGridLayout, QApplication, QPushButton

from views.base.BaseWindow import BaseWindow
from helpers.PyInstallerHelper import resource_path as rp


class PreferencesWindow(QDialog, BaseWindow):
    def __init__(self, modo_escuro: bool, parent=None):
        super().__init__(parent)
        self.load_theme(modo_escuro)
        self.setWindowTitle("Preferências")
        self.setFixedSize(420, 350)

        self.settings = QSettings("theme", "modo_escuro")
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Apply |
            QDialogButtonBox.StandardButton.Cancel)
        # Adiciona nomes aos botões
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Ok")
        self.button_box.button(QDialogButtonBox.StandardButton.Apply). \
            setText("Aplicar")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel). \
            setText("Cancelar")
        # Seta o nome do botão para ajudar no CSS
        self.button_box.button(QDialogButtonBox.StandardButton.Ok). \
            setObjectName("ok_button")
        self.button_box.button(QDialogButtonBox.StandardButton.Apply). \
            setObjectName("apply_button")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel). \
            setObjectName("cancel_button")

        # Conecta os botões aos métodos
        self.button_box.accepted.connect(self.salvar_preferencias)
        self.button_box.rejected.connect(self.rejeitar_preferencias)
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked. \
            connect(self.aplicar_preferencias)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Opções")
        self.tabs.addTab(self.tab2, "Sobre")
        # Seta o nome do tab para ajudar no CSS
        self.tabs.setObjectName("tabs")

        self.tab1.layout = QVBoxLayout(self.tab1)

        # Crie um combobox para selecionar o tema
        self.theme_combobox = QComboBox()
        self.theme_combobox.setObjectName("theme_combobox")
        self.tab1.layout.addWidget(self.theme_combobox)

        # Adiciona os temas "Fusion", "Windows" e "Windows Vista"
        self.theme_combobox.addItem("Fusion", "Fusion")
        self.theme_combobox.addItem("Windows", "Windows")
        self.theme_combobox.addItem("Windows Vista", "WindowsVista")
        self.theme_combobox.insertSeparator(4)

        # Obtenha a lista de temas disponíveis na pasta "themes"
        themes_folder = rp("styles/")
        themes_light = []
        themes_dark = []
        with os.scandir(themes_folder) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(".css"):
                    with open(entry.path, "r") as f:
                        first_line = f.readline().strip("/*\n").strip()
                        if "dark" in first_line.lower():
                            themes_dark.append((first_line.replace(" Dark", "")
                                                .strip(), entry.name))
                        else:
                            themes_light.append((first_line.
                                                 replace(" Light", "").strip(),
                                                 entry.name))

        # Adiciona os temas claros ao combobox
        self.theme_combobox.addItem("Claro", themes_light)
        # Deixe o item "Claro" não clicável e alinhado à direita
        self.theme_combobox.model().item(4).setEnabled(False)
        self.theme_combobox.model().item(4).setTextAlignment(Qt.AlignmentFlag.
                                                             AlignRight)
        for theme in themes_light:
            self.theme_combobox.addItem(theme[0], theme[1])

        # Adiciona um separador
        self.theme_combobox.insertSeparator(5 + len(themes_light))

        # Adiciona os temas escuros ao combobox
        self.theme_combobox.addItem("Escuro", themes_dark)
        # Não clicável e a direita
        self.theme_combobox.model().item(6 + len(themes_light)). \
            setEnabled(False)
        self.theme_combobox.model().item(6 + len(themes_light)). \
            setTextAlignment(Qt.AlignmentFlag.AlignRight)

        for theme in themes_dark:
            self.theme_combobox.addItem(theme[0], theme[1])

        # Adicionando o botão 'Restaurar Padrões'
        self.default_button = QPushButton('Restaurar Padrões')
        self.default_button.setObjectName("default_button")
        self.default_button.setToolTip("Restaura as configurações padrões e "
                                       "fecha todas as janelas abertas.")
        self.default_button.setFixedSize(125, 30)  # Define o tamanho do botão
        # Conecta o botão ao método
        self.default_button.clicked.connect(self.restore_defaults)

        # Incluindo o botão no tab1
        self.tab1.layout.addWidget(self.default_button,
                                   alignment=Qt.AlignmentFlag.AlignHCenter)

        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout(self.tab2)

        self.developers_label = QLabel(
            "<p>Este é um programa desenvolvido como trabalho de conclusão de "
            "curso na Universidade Federal Fluminense, na área de Ciências da "
            "Computação. O objetivo do projeto foi criar uma interface para o "
            "software RsPaper, utilizando o framework QT6. O trabalho foi "
            "realizado pelos orientandos Amanda Miquilini e Luan Bernardo Dias,"
            " sob a supervisão do professor Altobelli de Brito Mantuan.</p><p"
            "align='justify'><span style='font-weight:700;'>2023:<br/></span"
            ">Altobelli de Brito Mantuan: <a href='https://github.com/altobelli"
            "bm'><span style='text-decoration: underline; color:hsl(195, 75%,"
            "50%);'>https://github.com/altobellibm<br/></span></a>Amanda "
            "Miquilini: <a href='https://github.com/amiquilini'><span style='"
            "text-decoration: underline;color:hsl(195, 75%, 50%);'>https://gith"
            "ub.com/amiquilini</span></a><br/>Luan Bernardo Dias: <a href='"
            "https://github.com/luandiasrj'><span style='text-decoration: "
            "underline;color:hsl(195, 75%, 50%);'>https://github.com/luandiasrj"
            "</span></a><br/></p>")
        self.developers_label.setWordWrap(True)
        self.developers_label.setOpenExternalLinks(True)
        self.tab2.layout.addWidget(self.developers_label)
        self.developers_label.setStyleSheet(
            "font-size: 11pt; font-family: " "Calibri;")
        self.tab2.setLayout(self.tab2.layout)

        self.layout = QGridLayout()
        self.layout.addWidget(self.tabs, 0, 0, 1, 2)
        self.layout.addWidget(self.button_box, 1, 1)
        self.setLayout(self.layout)

        self.carregar_preferencias()

    def carregar_preferencias(self):
        # Carrega o tema selecionado
        theme = self.settings.value("theme")
        self.settings.value("modo_escuro")

        # Definido o tema, seleciona o tema no combobox
        if theme is None or not isinstance(theme, str):
            # Caso contrário, defina o tema como RsPaper Light
            theme = "RsPaper light.css"

        # Encontre o índice do tema
        index = self.theme_combobox.findData(theme)

        # Se o índice for válido, defina o tema
        if index >= 0:
            self.theme_combobox.setCurrentIndex(index)

    def salvar_preferencias(self):
        self.aplicar_preferencias()
        self.parent().modo_escuro.setChecked(
            self.parent().modo_escuro.isChecked())
        self.close()

    def aplicar_preferencias(self):
        def update_theme(theme_path):
            with open(theme_path, "r") as f:
                self.parent().setStyleSheet(f.read())
                self.setStyleSheet(f.read())

        # Salva o tema selecionado
        self.settings.setValue("theme", self.theme_combobox.currentData())
        # Aplica o tema selecionado
        theme = self.theme_combobox.currentData()
        if theme in ["Fusion", "Windows", "WindowsVista"]:
            QApplication.instance().setStyle(theme)
            self.setStyle(QApplication.instance().style())
            self.parent().setStyleSheet("")
            self.setStyleSheet("")
            self.parent().modo_escuro.setDisabled(True)
            self.settings.setValue("modo_escuro", False)
        else:
            modo_escuro = "dark" in theme.lower()
            self.parent().modo_escuro.setChecked(modo_escuro)
            self.parent().modo_escuro.setDisabled(False)
            self.settings.setValue("modo_escuro", modo_escuro)
            stylesheet_path = rp("styles/") + theme
            update_theme(stylesheet_path)

    def rejeitar_preferencias(self):
        self.close()

        # Função para restaurar os padrões

    def restore_defaults(self):
        # Limpar as configurações
        self.settings.clear()
        # Fechar todas as janelas
        QApplication.closeAllWindows()
