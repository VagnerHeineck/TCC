from PyQt6.QtWidgets import QMessageBox
from views.base.BaseWindow import BaseWindow


def dialogo_erro(msg: str, modo_escuro: bool, parent=None):
    msg_box = CustomErrorDialog(msg, modo_escuro, parent)
    return msg_box.exec()


class CustomErrorDialog(QMessageBox, BaseWindow):
    def __init__(self, msg: str, modo_escuro: bool, parent=None):
        super().__init__(parent)
        self.load_theme(modo_escuro)
        self.setText('<b>' + msg + '</b>')
        self.setWindowTitle('Ops, algo deu errado')
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Warning)
