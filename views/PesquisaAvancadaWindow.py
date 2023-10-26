from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, \
    QHBoxLayout
from PyQt6.uic import loadUi

from helpers.PyInstallerHelper import resource_path as rp
from views.base.BaseWindow import BaseWindow


class PesquisaAvancadaWindow(QDialog, BaseWindow):
    def __init__(self, definir_filtro_window, modo_escuro_habilitado: bool):
        super().__init__()
        loadUi(rp('ui/Pesquisa_Avancada.ui'), self)
        self.load_theme(modo_escuro_habilitado)
        self.definir_filtro_window = definir_filtro_window

        self.lineEdit.setPlaceholderText('"treatment as prevention"')

        self.layouts = [self.horizontalLayout]
        # Mapeia o lineEdit original para o layout original
        self.lineEdit_map = {self.lineEdit: self.horizontalLayout}

        self.lineEdit.textChanged.connect(
            lambda: self.add_or_delete(self.lineEdit))
        self.PalavrasChave.clicked.connect(self.on_palavras_chave_clicked)

    def add_or_delete(self, line_edit):
        text = line_edit.text()
        if text != "":
            # Verifica se há um layout em branco antes de criar um novo
            if any(line_edit.text() == "" for line_edit in
                   self.lineEdit_map.keys()):
                return
            # Cria um novo horizontal layout
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 6)
            new_line_edit = QLineEdit()
            combo_box = QComboBox()
            combo_box.addItem("E")
            combo_box.addItem("OU")
            combo_box.addItem("NÃO")
            layout.addWidget(new_line_edit)
            layout.addWidget(combo_box)

            new_line_edit.textChanged.connect(
                lambda: self.add_or_delete(new_line_edit))

            # Adiciona o novo layout à lista e ao layout vertical principal
            self.layouts.append(layout)
            self.lineEdit_map[new_line_edit] = layout
            self.verticalLayout.insertLayout(self.verticalLayout.count() - 1,
                                             layout)
        else:
            # Verifica se há layouts para remover
            if line_edit in self.lineEdit_map:
                layout_to_remove = self.lineEdit_map[line_edit]
                if layout_to_remove in self.layouts:  # remove apenas se o
                    # layout estiver na lista
                    self.layouts.remove(layout_to_remove)
                    # Limpa todos os widgets do layout
                    while layout_to_remove.count():
                        child = layout_to_remove.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()

                    # Remove o layout da interface gráfica
                    self.verticalLayout.removeItem(layout_to_remove)
                    del self.lineEdit_map[line_edit]  # remove a entrada do mapa
            # Reajusta o altura da janela
            largura = self.width()
            self.adjustSize()
            self.resize(largura, self.height())

    def get_keywords(self):
        keywords = []
        items = list(self.lineEdit_map.items())
        for line_edit, layout in items[:-1]:  # Ignora o último layout
            combo_box = layout.itemAt(1).widget()  # assume que o QComboBox é
            # o segundo widget no layout
            combo_box_text = combo_box.currentText().upper()  # Converte o
            # texto para maiúsculas para fazer a substituição
            combo_box_text = combo_box_text.replace('E', 'AND').replace(
                'OU', 'OR').replace('NÃO', 'NOT')
            line_edit_text = line_edit.text()
            keywords.append((combo_box_text, line_edit_text))  # Grava o
            # valor do combo_box antes do line_edit
        
        keywords_text = ' '.join(f'TITLE-ABS-KEY (*{k[1]}*) {k[0]}' for k
                                 in keywords)
        keywords_text = f'(({keywords_text}))'  # Envolva o texto final com
        # parênteses adicionais
        self.definir_filtro_window.textEdit.setText(keywords_text)

    def on_palavras_chave_clicked(self):
        self.get_keywords()
        self.close()
