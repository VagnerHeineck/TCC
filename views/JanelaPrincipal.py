import codecs
import csv
import math
import chardet

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import QSettings, QThread, pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (QVBoxLayout, QMainWindow, QWidget, QSpacerItem,
                             QSizePolicy, QFileDialog, QToolButton, QLabel)
from PyQt6.uic import loadUi

import helpers.WinScheme as Ws
import ui.ConfirmarDialog as Confirm
import ui.ErroDialog as Erro
from helpers.PyInstallerHelper import resource_path as rp
from helpers.QCircularProgressBar import QCircularProgressBar
from helpers.QToggle import QToggle
from models.Artigo import Artigo
# ==================== IMPORTS DE CONTROLLERS ====================
from views.AbstractWindow import AbstractWindow
from views.DefinirFiltroWindow import DefinirFiltroWindow
from views.Preferencias import PreferencesWindow
from views.base.BaseWindow import BaseWindow


class MainWindow(QMainWindow, BaseWindow):
    def __init__(self):
        super().__init__()
        loadUi(rp("ui/MainWindow.ui"), self)

        self.thread = None
        self.apex=None

        self.pesquisa = []  # inicializa um array para guardar os artigos da
        # pesquisa
        self.lista_artigos_selecionados = []
        self.lista_artigos_interesse = []
        self.lista_artigos_descartados = []
        self.spacer = None  # inicializa um spacer para a barra de rolagem

        # substitui o QCheckBox "modo_escuro" por um Toggle
        self.modo_escuro.deleteLater()  # deleta o modo escuro anterior
        self.modo_escuro = QToggle()
        self.modo_escuro.setText("Modo escuro")
        self.modo_escuro.setObjectName("modo_escuro")  # mantém o nome do
        # objeto para o css
        self.modo_escuro.setFixedHeight(12)
        self.Header.addWidget(self.modo_escuro)

        # Carregar o estado de modo_escuro
        self.settings = QSettings("theme", "modo_escuro")
        modo_escuro_salvo = self.settings.value("modo_escuro", False, bool)
        theme_name = self.settings.value("theme")
        self.modo_escuro.setChecked(modo_escuro_salvo)
        print("Carregando Tema: ", theme_name)

        # Primeira utilização do programa
        if Ws.get_color_scheme() == 0:  # Carrega o esquema de cores do windows
            if not modo_escuro_salvo and (isinstance(theme_name, int) or
                                          theme_name is None):
                self.modo_escuro.setChecked(True)
                self.mudar_modo_escuro(True)

        # Carrega o tema apropriado
        self.load_theme(self.modo_escuro.isChecked())
        # Se o tema for Fusion, Windows ou WindowsVista, defina o checkbox de
        # modo escuro de MainWindow como desabilitado
        if theme_name in ["Fusion", "Windows", "WindowsVista"]:
            self.modo_escuro.setDisabled(True)
        else:
            self.modo_escuro.setDisabled(False)

        self.modo_escuro.stateChanged.connect(self.mudar_modo_escuro)

        # Ao clicar em preferencias, abre a janela de preferencias
        self.preferencias.clicked.connect(self.open_preferencias)

        # Limpa qualquer valor que esteja na tela antes de iniciar qualquer ação
        self.limpar_sessao()

        # Altera a quantidade de artigos por página
        self.artigos_por_pagina.editingFinished.connect(self.update_pesquisa)

        # conecta o botão novo_projeto à função open_definir_filtro
        self.novo_projeto.clicked.connect(self.open_definir_filtro)

        # Aciona a função para abrir um arquivo de pesquisa
        self.abrir.clicked.connect(self.abrir_pesquisa)

        # Ordena artigos de uma pesquisa
        self.ordenar.clicked.connect(self.ordenar_button)

        # Muda os artigos de acordo com a view específica
        self.artigos_selecionados.clicked.connect(
            self.artigo_selecionado_button)
        self.artigos_interesse.clicked.connect(self.artigo_interesse_button)
        self.artigos_descartados.clicked.connect(self.artigo_descartado_button)

        # Altera a página atual
        self.pag_atual.editingFinished.connect(self.go_to_page)

        # Vai para a primeira página
        self.pag_primeira.clicked.connect(self.go_to_first_page)

        # Vai para a página anterior
        self.pag_anterior.clicked.connect(self.go_to_previous_page)

        # Vai para a próxima página
        self.pag_prox.clicked.connect(self.go_to_next_page)

        # Vai para a última página
        self.pag_ultima.clicked.connect(self.go_to_last_page)

        # ==================== Fim dos connects ====================

    def open_preferencias(self):
        # Abre a janela de preferências
        preferences_window = PreferencesWindow(self.modo_escuro.isChecked(),
                                               self)
        preferences_window.exec()

    def mudar_modo_escuro(self, state):  # Adicione esta função
        # Aplica o tema
        theme_name = self.settings.value("theme")
        self.settings.setValue("theme", theme_name)
        self.settings.setValue("modo_escuro", bool(state))
        print("Aplicado tema: ", theme_name, "Modo escuro: ", bool(state))
        modo_escuro_habilitado = self.modo_escuro.isChecked()

        self.load_theme(modo_escuro_habilitado, theme_name)
        if bool(state):
            self.modo_escuro.setText("Modo claro")
        else:
            self.modo_escuro.setText("Modo escuro")

    def open_definir_filtro(self):
        # Abre a janela de definição de filtro
        definir_filtro_window = DefinirFiltroWindow(
            self.modo_escuro.isChecked(), self
            )
        definir_filtro_window.exec()
        self.pesquisa=definir_filtro_window.get_articles
        #self.pesquisa.start()
        #self.apex=self.pesquisa.search
        #print("resultado filtro:",self.pesquisa.get_article())
        #print("resultado filtro:",self.pesquisa)

    def limpar_sessao(self):
        # Limpa qualquer valor que esteja na tela antes de iniciar qualquer ação
        self.limpar_pesquisas()  # limpa qualquer mockup de pesquisa
        self.pesquisa = []
        self.lista_artigos_selecionados = []
        self.lista_artigos_interesse = []
        self.lista_artigos_descartados = []
        self.artigos_por_pagina.setText("10")
        self.artigos_por_pagina.setEnabled(False)
        self.pag_primeira.setEnabled(False)
        self.pag_anterior.setEnabled(False)
        self.pag_atual.setEnabled(False)
        self.pag_prox.setEnabled(False)
        self.pag_ultima.setEnabled(False)
        self.ordenar.setEnabled(False)
        self.artigos_selecionados.setEnabled(False)
        self.artigos_interesse.setEnabled(False)
        self.artigos_descartados.setEnabled(False)
        self.estatisticas.setEnabled(False)
        self.label_ordenados.setText("")
        self.artigos_selecionados.setText(" Seleção de Artigos\n Total: 0")
        self.artigos_interesse.setText(" Artigos de Interesse\n Total: 0")
        self.artigos_descartados.setText(" Artigos Descartados\n Total: 0")
        self.pag_atual.setText("1")
        self.total.setText("de 1")

    def limpar_pesquisas(self):
        for child in self.RolagemArtigos.findChildren(QWidget):
            child.deleteLater()
        if self.spacer:
            self.RolagemArtigos.layout().removeItem(self.spacer)

    def update_artigo_button(self):
        self.artigos_selecionados.setText(
            " Seleção de Artigos\n Total: " + str(
                len(self.lista_artigos_selecionados))
        )
        self.artigos_interesse.setText(
            " Artigos de Interesse\n Total: " + str(
                len(self.lista_artigos_interesse))
        )
        self.artigos_descartados.setText(
            " Artigos Descartados\n Total: " + str(
                len(self.lista_artigos_descartados))
        )
        self.label_ordenados.setText(
            '<p align="center"><span style=" font-weight:600;">Artigos '
            'Ordenados:</span></p><p align="center"> '
            + str(len(self.pesquisa))
            + "</p>"
        )
        if len(self.lista_artigos_interesse) > 0 or len(
                self.lista_artigos_descartados) > 0:
            self.ordenar.setEnabled(True)
        else:
            self.ordenar.setEnabled(False)

    def update_pesquisa(self):
        # Aguarda a finalização da Thread antes de atualizar a pesquisa
        if self.thread and self.thread.isRunning():
            self.thread.wait()
        # limpa o layout
        self.limpar_pesquisas()

        # adiciona os layouts dos artigos ao layout RolagemArtigos
        self.ordenar_artigos()
        current_page = int(self.pag_atual.text())
        rows_per_page_value = self.arts_por_pagina()
        start_index = (current_page - 1) * rows_per_page_value
        end_index = start_index + rows_per_page_value
        artigos = self.pesquisa[start_index:end_index]
        for artigo in artigos:
            article_layout = self.create_article_layout(artigo)
            self.RolagemArtigos.layout().addWidget(article_layout)
        self.spacer = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.RolagemArtigos.layout().addSpacerItem(self.spacer)

        # atualiza os botões dos artigos selecionados
        self.update_artigo_button()

        # atualiza o número máximo de páginas
        total_rows = len(self.pesquisa)
        global max_pages
        max_pages = math.ceil(total_rows / rows_per_page_value)
        # atualiza o número de páginas
        self.total.setText("de " + str(max_pages))

        # atualiza a página atual
        current_page = int(self.pag_atual.text())
        self.pag_atual.setText(str(min(current_page, max_pages)))

        # atualiza o estado dos botões de paginação
        self.pag_primeira.setEnabled(current_page > 1)
        self.pag_anterior.setEnabled(current_page > 1)
        self.pag_prox.setEnabled(current_page < max_pages)
        self.pag_ultima.setEnabled(current_page < max_pages)

        # Verifica se está nos artigos descartados ou de interesse
        if self.artigos_interesse.isChecked():
            self.ordenar.setEnabled(False)
            # Se estiver nos artigos de interesse, desabilita o botão de like
            for child in self.RolagemArtigos.findChildren(QToolButton):
                if child.objectName() == "like":
                    child.deleteLater()
            for child in self.RolagemArtigos.findChildren(QLabel):
                if child.objectName() == "ranking":
                    child.deleteLater()

        elif self.artigos_descartados.isChecked():
            self.ordenar.setEnabled(False)
            # Se estiver nos artigos descartados, desabilita o botão de dislike
            for child in self.RolagemArtigos.findChildren(QToolButton):
                if child.objectName() == "dislike":
                    child.deleteLater()
            for child in self.RolagemArtigos.findChildren(QLabel):
                if child.objectName() == "ranking":
                    child.deleteLater()

    def abrir_pesquisa(self):
        # Abre um arquivo de pesquisa
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Abrir Pesquisa", "", "Arquivos de pesquisa (*.csv)"
            )
            self.gerencia_abertura(file_name)
        except Exception as e:
            msg = "Um erro ao abrir o arquivo:\n" + str(e)
            Erro.dialogo_erro(msg, self.modo_escuro.isChecked(), self)
            self.limpar_sessao()

    def gerencia_abertura(self, file_name):
        # Abre um arquivo de pesquisa
        try:
            if file_name:  # Se o usuário selecionou um arquivo
                self.limpar_sessao()
                self.progressBar = QCircularProgressBar(self.RolagemArtigos)
                self.progressBar.setObjectName(u"progressBar")
                self.progressBar.setValue(0)
                # Define o tamanho da barra de progresso para metade da tela
                self.progressBar.setMinimumSize(
                    QtCore.QSize(int(self.width() / 2), int(self.height() / 2))
                )
                self.verticalLayout.addWidget(
                    self.progressBar, 0, Qt.AlignmentFlag.AlignCenter)
                self.progressBar.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter)
                self.progressBar.show()

                self.thread = LeitorArquivo(file_name, self.pesquisa, self)
                self.thread.progress.connect(self.atualizar_progresso)
                # Conecte o sinal error_signal
                self.thread.error_signal.connect(self.show_error_dialog)
                self.thread.start()

                # Atualiza a pesquisa
                self.lista_artigos_selecionados = self.pesquisa
                self.artigos_por_pagina.setEnabled(True)
                self.pag_atual.setEnabled(True)
                self.artigos_selecionados.setEnabled(True)
                self.artigos_interesse.setEnabled(True)
                self.artigos_descartados.setEnabled(True)
                self.estatisticas.setEnabled(True)
                self.check_artigos_buttons(selecionados=True)
                self.thread.finished.connect(self.update_pesquisa)
        except Exception as e:
            msg = "Ocorreu um erro ao construir a janela:\n" + str(e)
            Erro.dialogo_erro(msg, self.modo_escuro.isChecked(), self)
            self.limpar_sessao()

    # ==================== Funções de ordenação de artigos ====================
    def ordenar_artigos(self):
        if self.ordenar.isChecked():
            # Ordena por rank e interessante:False
            self.pesquisa.sort(key=lambda x: x.interessante, reverse=True)
        else:
            # Ordena por ordem de inserção
            self.pesquisa.sort(key=lambda x: x.rank, reverse=False)

    # ==========================================================================

    def ordenar_button(self):
        if self.pesquisa:
            self.update_pesquisa()

    def artigo_selecionado_button(self):
        self.check_artigos_buttons(selecionados=True)
        self.pesquisa = self.lista_artigos_selecionados
        self.go_to_first_page()

    def artigo_interesse_button(self):
        self.check_artigos_buttons(interesse=True)
        self.pesquisa = self.lista_artigos_interesse
        self.go_to_first_page()

    def artigo_descartado_button(self):
        self.check_artigos_buttons(descartados=True)
        self.pesquisa = self.lista_artigos_descartados
        self.go_to_first_page()

    def check_artigos_buttons(
            self, selecionados=False, interesse=False, descartados=False
    ):
        self.artigos_selecionados.setChecked(selecionados)
        self.artigos_interesse.setChecked(interesse)
        self.artigos_descartados.setChecked(descartados)

    def go_to_first_page(self):
        self.pag_atual.setText("1")
        self.update_pesquisa()

    def go_to_previous_page(self):
        if int(self.pag_atual.text()) > 1:
            self.pag_atual.setText(str(int(self.pag_atual.text()) - 1))
            self.update_pesquisa()
        else:
            self.pag_atual.setText("1")

    def go_to_next_page(self):
        if int(self.pag_atual.text()) < max_pages:
            self.pag_atual.setText(str(int(self.pag_atual.text()) + 1))
            self.update_pesquisa()
        else:
            self.pag_atual.setText(str(max_pages))

    def go_to_last_page(self):
        self.pag_atual.setText(str(max_pages))
        self.update_pesquisa()

    def go_to_page(self):
        page = self.pag_atual.text()
        if not page.isnumeric():
            page = 1
        page = max(min(int(page), max_pages), 1)
        self.pag_atual.setText(str(page))
        self.update_pesquisa()

    def arts_por_pagina(self):
        try:
            n_artigos = (
                int(self.artigos_por_pagina.text())
                if self.artigos_por_pagina.text()
                else 10
            )
            n_artigos = max(1, n_artigos)
            n_artigos = min(20, n_artigos)
            self.artigos_por_pagina.setText(str(n_artigos))
            return n_artigos
        except ValueError:
            Erro.dialogo_erro("Número inválido de artigos por página",
                              self.modo_escuro.isChecked(), self)
            self.artigos_por_pagina.setText("10")
            return 10

    def create_article_layout(self, artigo: Artigo):

        def create_icon(path: str) -> QtGui.QIcon:
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(path),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            return icon

        def create_tool_button(icon: QtGui.QIcon, obj_name: str) -> \
                QtWidgets.QToolButton:
            button = QtWidgets.QToolButton()
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(20, 20))
            button.setStyleSheet("border: none;")
            button.setObjectName(obj_name)
            return button

        # Cria funções para mostrar e ocultar os botões like e dislike
        def show_buttons():
            safe_call(like.show)
            safe_call(dislike.show)

        def hide_buttons():
            safe_call(like.hide)
            safe_call(dislike.hide)

        # evita erros caso esteja em selecionados/descartados
        def safe_call(method):
            try:
                method()
            except:
                pass

        # cria um QWidget para o artigo
        article_widget = QWidget()
        article_widget.setObjectName("Artigo")

        # cria um QVBoxLayout para o artigo
        article_layout = QVBoxLayout()
        article_layout.setSpacing(20)
        # article_layout.setObjectName("Artigo")

        # adiciona o título do artigo
        linha_titulo = QtWidgets.QHBoxLayout()
        linha_titulo.setSpacing(5)

        titulo = QtWidgets.QLabel(artigo.nome)
        titulo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        titulo.setObjectName("titulo_artigo")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(True)
        titulo.setFont(font)
        # titulo.setWordWrap(True)
        # tamanho da caixa de texto
        tam_titulo = QSizePolicy(QSizePolicy.Policy.Ignored,
                                 QSizePolicy.Policy.Preferred)
        titulo.setSizePolicy(tam_titulo)
        titulo.setMinimumHeight(23)

        linha_titulo.addWidget(titulo)

        article_widget.enterEvent = lambda event: show_buttons()
        article_widget.leaveEvent = lambda event: hide_buttons()

        icon_check = create_icon(rp("styles/light/aprovar.png"))
        icon_uncheck = create_icon(rp("styles/light/descartar.png"))

        like = create_tool_button(icon_check, "like")
        dislike = create_tool_button(icon_uncheck, "dislike")

        linha_titulo.addWidget(like)
        linha_titulo.addWidget(dislike)

        # Oculta os botões like e dislike por padrão
        hide_buttons()

        article_layout.addLayout(linha_titulo)

        # adiciona linha para autor ano e citações
        autor_ano_citacoes = QtWidgets.QHBoxLayout()
        autor_ano_citacoes.setSpacing(10)
        autor_ano_citacoes.setObjectName("autor_ano_citacoes")

        # adiciona o autor do artigo
        autor = QtWidgets.QLabel("Autor: " + artigo.autor)
        autor.setObjectName("autor_artigo")
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        autor.setFont(font)
        autor_ano_citacoes.addWidget(autor)

        # adiciona o ano do artigo
        ano = QtWidgets.QLabel("Ano: " + str(artigo.ano))
        ano.setObjectName("ano_artigo")
        ano.setFont(font)
        autor_ano_citacoes.addWidget(ano)

        # adiciona o número de citações do artigo
        citacoes = QtWidgets.QLabel("Citações: " + str(artigo.citacoes))
        citacoes.setObjectName("citacoes_artigo")
        citacoes.setFont(font)
        autor_ano_citacoes.addWidget(citacoes)

        # adiciona o ranking do artigo
        ranking_atual = artigo.rank - (self.pesquisa.index(artigo) + 1)
        if artigo.interessante == 1 and ranking_atual != 0:
            ranking = QtWidgets.QLabel("\u2B9D " + str(ranking_atual))
            ranking.setStyleSheet("color: green;")
        elif artigo.interessante == -1 and ranking_atual != 0:
            ranking = QtWidgets.QLabel("\u2B9F " + str(-ranking_atual))
            ranking.setStyleSheet("color: red;")
        else:
            ranking = QtWidgets.QLabel("")
        ranking.setObjectName("ranking")
        ranking.setFont(font)
        ranking.setAlignment(Qt.AlignmentFlag.AlignRight)
        autor_ano_citacoes.setContentsMargins(0, 0, 20, 0)
        autor_ano_citacoes.addWidget(ranking)

        article_layout.addLayout(autor_ano_citacoes)

        # adiciona o resumo do artigo
        abstract = QtWidgets.QLabel(artigo.abstract[:300] + "...")
        abstract.setObjectName("abstract_artigo")
        abstract.setWordWrap(True)
        article_layout.addWidget(abstract)

        # adiciona um separador entre artigos
        line = QtWidgets.QFrame(parent=self)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setObjectName("line")  # para o css
        article_layout.addWidget(line)

        titulo.mousePressEvent = lambda event: self.open_abstract(
            event, artigo)
        like.clicked.connect(lambda: Confirm.dialogo_marcar(
            artigo, self.modo_escuro.isChecked(), self))
        dislike.clicked.connect(lambda: Confirm.dialogo_desmarcar(
            artigo, self.modo_escuro.isChecked(), self))

        article_widget.setLayout(article_layout)
        return article_widget
        # return article_layout

    def open_abstract(self, event, artigo):
        # Abre a janela de abstract
        if event.button() == Qt.MouseButton.LeftButton:
            abstract_window = AbstractWindow(
                self.modo_escuro.isChecked(), artigo, self)
            abstract_window.exec()

    # Função para exibir a mensagem de erro
    def show_error_dialog(self, msg):
        Erro.dialogo_erro(msg, self.modo_escuro.isChecked(), self)

    # ==================== Chamada Thread ====================
    def atualizar_progresso(self, progress, text):
        self.progressBar.setValue(progress)
        self.progressBar.setFormat(text)


# ==================== Thread do leitor de arquivos ====================
class LeitorArquivo(QThread):
    progress = pyqtSignal(int, str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, file_name, pesquisa, main_window):
        super().__init__()
        self.file_name = file_name
        self.pesquisa = pesquisa
        self.main_window = main_window

    def run(self):
        with open(self.file_name, "rb") as f:
            self.progress.emit(1, "Detectando encoding...")
            result = chardet.detect(f.read(1024))
            encoding = result["encoding"]
            f.seek(0)
        # Obtém numero de linhas do arquivo
        with open(self.file_name, "r", encoding=encoding, errors="replace") as \
                f:
            self.progress.emit(2, "Contando linhas...")
            num_lines = sum(1 for _ in f)
        num_lines -= 1  # desconta a linha de cabeçalho
        try:
            with codecs.open(self.file_name, "r", encoding=encoding,
                             errors="replace") as f:
                for i, line in enumerate(csv.DictReader(f, delimiter=";")):
                    linha = i + 1
                    progresso = int(linha / num_lines * 100)
                    self.progress.emit(progresso, f"Lendo artigo {linha}")
                    # Imprime o número da linha e os 30 primeiro caracteres
                    # Usado apenas para retardar o processamento
                    # print(linha, line["dc:title"][:30])
                    #print(line["abstract"])#--alteração Vagner estudo
                    #parametros de article: self,doi: str, nome: str, autor: str, ano: int,citacoes: int, abstract: str, fator_impacto: float,link_scopus: str, link_source: str, rank: int, interessante: int= 0
                    
                    if not ("abstract" or "source-score-2019" or "link:scopus" or "view-in-source") in line:
                        op=line["link"]
                        op1=eval(op)
                        op2=op1[2]
                        op3=op2['@href']
                        print("op1:",type(op3))
                        self.pesquisa.append(Artigo(line["prism:doi"], line["dc:title"],
                                line["dc:creator"], line["prism:coverDate"],
                                int(line["citedby-count"]), 'line["abstract"]',
                                0.0,op3,
                                'line["view-in-source"]',
                                linha))#Artigo(line["prism:doi"], line["dc:title"],line["dc:creator"], line["prism:coverDate"],int(line["citedby-count"]), line["abstract"],float(line["source-score-2019"]),line["link:scopus"], line["view-in-source"],linha))
                    else:
                        self.pesquisa.append(Artigo(line["prism:doi"], line["dc:title"],
                                                    line["dc:creator"], line["prism:coverDate"],
                                                    int(line["citedby-count"]), line["abstract"],
                                                    float(line["source-score-2019"]),line["link:scopus"],
                                                      line["view-in-source"],linha))            
            self.progress.emit(100, "Concluído!")
            # sinaliza que a thread foi concluída
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit("Erro ao ler arquivo\n" + str(e))
