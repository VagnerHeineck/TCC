from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices, QGuiApplication
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

import ui.ConfirmarDialog as Cd
from helpers.PyInstallerHelper import resource_path as rp
from models.Artigo import Artigo
from views.base.BaseWindow import BaseWindow


class AbstractWindow(QDialog, BaseWindow):
    def __init__(self, modo_escuro_habilitado: bool, artigo: Artigo,
                 main_window):
        super().__init__()
        loadUi(rp('ui/Abstract.ui'), self)
        self.load_theme(modo_escuro_habilitado)
        self.set_artigo_data(artigo)  # Preenche com os dados do artigo
        self.connect_buttons(artigo, modo_escuro_habilitado, main_window)
        self.set_window_size_and_position()

    def set_artigo_data(self, artigo: Artigo):
        self.titulo.setText(artigo.nome)
        self.autor.setText(artigo.autor)
        self.abstract_text.setText(artigo.abstract)

    def connect_buttons(self, artigo: Artigo, modo_escuro_habilitado: bool,
                        main_window):
        self.like.clicked.connect(
            lambda: Cd.dialogo_marcar(artigo, modo_escuro_habilitado,
                                      main_window))
        self.dislike.clicked.connect(
            lambda: Cd.dialogo_desmarcar(artigo, modo_escuro_habilitado,
                                         main_window))
        self.titulo.mousePressEvent = lambda event: self.open_link(artigo)

    def set_window_size_and_position(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        half_height = int(screen_geometry.height() / 2)

        if self.height() > half_height:
            self.resize(screen_geometry.width(), screen_geometry.height())

        self.move(int(screen_geometry.width() / 2 - self.width() / 2),
                  int(screen_geometry.height() / 2 - self.height() / 2))
        
    @staticmethod
    def open_link(artigo: Artigo):
        url = QUrl(artigo.link_scopus)
        QDesktopServices.openUrl(url)
