from PyQt6.QtWidgets import QMessageBox
from views.base.BaseWindow import BaseWindow


def dialogo_marcar(artigo, modo_escuro: bool, parent=None):
    titulo = 'Marcar Interesse'
    texto = 'Deseja mover para Artigos de Interesse?'
    message = 'O artigo selecionado estará na aba Artigos de Interesse'
    msg_box = CustomMsgDialog(artigo, titulo, texto, message, modo_escuro,
                              parent, move_artigo_interesse, parent)
    return msg_box.exec()


def dialogo_desmarcar(artigo, modo_escuro: bool, parent=None):
    titulo = 'Desmarcar Interesse'
    texto = 'Deseja mover para Artigos Descartados?'
    message = 'O artigo selecionado estará na aba Artigos Descartados'
    msg_box = CustomMsgDialog(artigo, titulo, texto, message, modo_escuro,
                              parent, move_artigo_descartado, parent)
    return msg_box.exec()


class CustomMsgDialog(QMessageBox, BaseWindow):
    def __init__(self, artigo, titulo: str, texto: str, message: str,
                 modo_escuro: bool, parent=None, move_function=None,
                 main_window=None):
        super().__init__(parent)
        self.load_theme(modo_escuro)
        self.setWindowTitle(titulo)
        self.setText('<b>' + texto + '</b>')
        self.setInformativeText(message)
        self.setIcon(QMessageBox.Icon.Question)
        self.setStandardButtons(QMessageBox.StandardButton.Yes |
                                QMessageBox.StandardButton.No)
        ok_button = self.button(QMessageBox.StandardButton.Yes)
        ok_button.setText('Sim')
        cancel_button = self.button(QMessageBox.StandardButton.No)
        cancel_button.setText('Não')
        if move_function is not None and main_window is not None:
            ok_button.clicked.connect(
                lambda: move_function(artigo, main_window, modo_escuro))


class CustomOkDialog(QMessageBox, BaseWindow):
    def __init__(self, titulo: str, texto: str, modo_escuro: bool, parent=None):
        super().__init__(parent)
        self.load_theme(modo_escuro)
        self.setWindowTitle(titulo)
        self.setText('<b>' + texto + '</b>')
        self.setIcon(QMessageBox.Icon.Information)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        ok_button = self.button(QMessageBox.StandardButton.Ok)
        ok_button.setText('Ok')


def move_artigo_interesse(artigo, main_window, modo_escuro: bool):
    if artigo not in main_window.lista_artigos_interesse:
        artigo.interessante = 1
        main_window.lista_artigos_interesse.append(artigo)        
    # if artigo in main_window.lista_artigos_selecionados:
    #     main_window.lista_artigos_selecionados.remove(artigo)
    if artigo in main_window.lista_artigos_descartados:
        artigo.interessante = 1
        main_window.lista_artigos_descartados.remove(artigo)
    main_window.update_pesquisa()
    CustomOkDialog("Artigo Movido",
                   "O artigo foi movido para a aba Artigos de Interesse.",
                   modo_escuro, main_window).exec()


def move_artigo_descartado(artigo, main_window, modo_escuro: bool):
    if artigo not in main_window.lista_artigos_descartados:
        artigo.interessante = -1
        main_window.lista_artigos_descartados.append(artigo)
    # if artigo in main_window.lista_artigos_selecionados:
    #     main_window.lista_artigos_selecionados.remove(artigo)
    if artigo in main_window.lista_artigos_interesse:
        artigo.interessante = -1
        main_window.lista_artigos_interesse.remove(artigo)
    main_window.update_pesquisa()
    CustomOkDialog("Artigo Movido",
                   "O artigo foi movido para a aba Artigos Descartados.",
                   modo_escuro, main_window).exec()
