from PyQt6.QtWidgets import QDialog,QLabel
from PyQt6.QtWidgets import * 
from PyQt6.uic import loadUi

from views.PesquisaAvancadaWindow import PesquisaAvancadaWindow
from views.base.BaseWindow import BaseWindow
from helpers.PyInstallerHelper import resource_path as rp

#Atualização Vagner 16/10/2023

#Importação de arquivos que contém as Apis para busca no Scopus e Pubmed
from servers.controllers.pymed.api import PubMed
from servers.controllers.pymedController import PymedController

from servers.controllers.scopusController import ScopusController
from servers.controllers.pyscopus.helpers_scopus import params, searchUrl, headers

#Importação das libs que carregam dados de ambiente virtual(dotenv) e adquirem dados por meio do OS
from dotenv import load_dotenv
import os

#Importação da JanelaPrincipal
#from views.JanelaPrincipal import LeitorArquivo


def open_pesquisa_avancada(definir_filtro_window, modo_escuro_habilitado: bool):
    pesquisa_avancada_window = PesquisaAvancadaWindow(definir_filtro_window,
                                                      modo_escuro_habilitado)
    pesquisa_avancada_window.exec()


class DefinirFiltroWindow(QDialog, BaseWindow):

    def __init__(self, modo_escuro_habilitado: bool, main_window):
        super().__init__()
        loadUi(rp('ui/Definir_Filtro.ui'), self)
        self.load_theme(modo_escuro_habilitado)
        #self.main_window = main_window

        # Conecta a label PesquisaAvancada à função open_pesquisa_avancada
        self.PesquisaAvancada.clicked.connect(lambda: open_pesquisa_avancada(
            self, modo_escuro_habilitado)) #CHAMA JANELA DA LABEL 'PESQUISA AVANÇADA' 

        # Adicione um place holder ao textEdit
        self.textEdit.setPlaceholderText("Exemplo: ((TITLE-ABS-KEY (*tenofovir*"
                                         ") AND TITLE-ABS-KEY (*lamivudine*) AN"
                                         "D TITLE-ABS-KEY(*efavirenz*)) OR (TIT"
                                         "LE-ABS-KEY(*fixed-dose* AND *combin* "
                                         ") OR TITLE-ABS-KEY(*fdc*))")
        self.Scopus.setChecked(True)
        #Mudanças Vagner
        #Fontes desabilitadas
        self.Merk.setEnabled(False)
        self.Drugbank.setEnabled(False)
        self.Fonte.setEnabled(False)

        # Conecta o botão Pesquisar à função abrir_pesquisa_avancada
        self.Pesquisar.clicked.connect(self.abrir_pesquisa_avancada)

        #MUDANÇAS VAGNER
        self.pubmed = PubMed()
        self.pymed_controller = PymedController()

        self.scopus_controller = ScopusController()
        
        self.classe_dict={'scopus':self.scopus_controller,'pubmed':self.pymed_controller,'Merk':None,'Drugbank':None,'Fonte':None}
        self.get_articles=None
        self.scopus_artigos=[]
        self.pubmed_artigos=[]
        self.merk_artigos=None
        self.drugbank_artigos=None
        self.fonte_artigos=None
        self.artigos_dict={'scopus':self.scopus_artigos,'pubmed':self.pubmed_artigos,'Merk':None,'Drugbank':None,'Fonte':None}

    def abrir_pesquisa_avancada(self):
        # Arquivos solos são gravados na raíz da pasta pelo autopytoexe
        #self.main_window.gerencia_abertura(rp('resultados\\''resultado-scopus ''22.csv')) #RESPONSAVEL POR ABRIR ARQUIVO CSV NO BOTÃO 'PESQUISAR' EM 'NOVO PROJETO' 

        #MUDANÇAS FEITAS POR VAGNER
        #salva query de busca
        selecoes_dict=self.verificar_selecao()
        self.query=self.textEdit.toPlainText()
        _params=params.copy()
        _params['query']= self.query
        print(selecoes_dict)
        valorscopus=self.acessa_fonte(selecoes_dict['scopus'],self.query,self.scopus_controller)
        valorpymed=self.acessa_fonte(selecoes_dict['pubmed'],self.query,self.pymed_controller)
        dados_dict={'scopus':valorscopus,'pubmed':valorpymed,'Merk':None,'Drugbank':None,'Fonte':None}
        print(dados_dict['scopus'])
        print(dados_dict['pubmed'])
        valorscopus['results']=1
        valorpymed['results']=1
        #dados_dict={'scopus':valorscopus,'pubmed':valorpymed,'Merk':None,'Drugbank':None,'Fonte':None}
        print('scopus:',dados_dict['scopus'])
        self.obter_artigos(selecoes_dict,dados_dict)
        #valorpymed['results']=100
        #valorpymed=self.obter_artigos(selecoes[1],valorscopus,self.scopus_controller)
        #valormerk=self.acessa_fonte(selecoes[2],self.query,'')
        #valordrugbank=self.acessa_fonte(selecoes[3],self.query,'')
        #valorfonte=self.acessa_fonte(selecoes[4],self.query,'')
        print(dados_dict['scopus'])
        print(dados_dict['pubmed'])
        print("Artigos Scopus:")
        print(self.scopus_artigos)
        print("Artigos Pubmed:")
        print(self.pubmed_artigos)
        
        #valorpubmed=acessa_fonte(selecoes[1],self.Pubmed)
        
            
        #resultados=self.scopus_controller.get_total_results_count(self.query)
        #total_articles=resultados["results"]
        
        #self.get_articles=self.scopus_controller.get_articles(100,'dontcare')
        #self.get_articles.start()
        
        
        # Fecha a janela 'Novo Projeto'
        self.close()
        
    def verificar_selecao(self):
        selecoes_dict={'scopus':self.Scopus.isChecked(),'pubmed':self.Pubmed.isChecked(),'merk':self.Merk.isChecked(),
                  'drugbank':self.Drugbank.isChecked(),'fonte':self.Fonte.isChecked()}
        return selecoes_dict
    
    def acessa_fonte(self, selecao, query, classe=''):
        if selecao:
            try:
                return classe.get_total_results_count(query)
            except Exception as e:
                self.mensagem_erro("Erro ao tentar o site. \n Verifique o acesso a internet.")
                print("Erro: No método acessa_fonte da classe DefinirFiltroWindow")
                return {"results": 0, "error_message": "Não foi possível acessar a fonte"}
    
    def obter_artigos(self,selecao_dict,dados_dict):
        for fonte, selecao in selecao_dict.items():
            if selecao:
                fonte_dict=dados_dict[fonte]
                if fonte_dict['error_message'] is None:
                    self.adquirir_artigos(fonte,fonte_dict)
                else:
                    print(fonte_dict['error_message'])
                    self.mensagem_erro(fonte_dict['error_message'])
                    self.artigos_dict[fonte]=None
                    
    def adquirir_artigos(self,fonte,fonte_dict):
        if (fonte=='scopus'):
                if fonte_dict['error_message'] is None:
                    self.classe_dict[fonte]=self.classe_dict[fonte].get_articles(int(fonte_dict['results']),'')
                    self.scopus_artigos=self.classe_dict[fonte].run()
                else:
                    print(fonte_dict['error_message'])
                    mensagem_erro(fonte_dict['error_message'])
        if (fonte=='pubmed'):
                if fonte_dict['error_message'] is None:
                    self.classe_dict[fonte]=self.classe_dict[fonte].get_articles(self.query, int(fonte_dict['results']), 100,
                                   '')
                    self.pubmed_artigos=self.classe_dict[fonte].run()
                else:
                    print(fonte_dict['error_message'])
                    mensagem_erro(fonte_dict['error_message'])
            
            
                    

    def mensagem_erro(self,mensagem):
        dlg=QMessageBox(self)
        dlg.setText(mensagem)
        dlg.exec()
                
            
        
    
