import csv
import pandas as pd

from PyQt6.QtCore import QThread, pyqtSignal

import requests

from .helpers_scopus import params
from servers.controllers.pyscopus.api import Scopus
from models.Artigo import Artigo

class GetArticlesThreadScopus(QThread):
    # cria sinal para valor que desejo enviar. Se for mais de 1 valor, basta declarar os tipos (int str dict), pe.
    update_progress = pyqtSignal(int)
    error_responses = pyqtSignal(dict)

    def __init__(self, articles_amount: int, fname: str, scopus: Scopus): # first_page: dict, 
        super(QThread, self).__init__()
        self.articles_amount = articles_amount
        self.fname = fname
        self.list_EIDs = []
        #self.first_page = first_page
        self.search = []
        self.scopus = scopus
        self.round_progress=None #Alteração Vagner
        self.article=None #Alteração Vagner

    def run(self):
        # processa a primeira pagina obtida na pesquisa que retorna qtdades
        articles = self.scopus.process_results(self.scopus.first_page ) #self.first_page)
        next_url = self.scopus.get_next_url(self.scopus.first_page) #self.first_page)

        while len(articles) < self.articles_amount:
            if next_url is None:
                break

            scopus_response = self.scopus.getArticles(url=next_url)
            if scopus_response["error"] is not None:
                break
            articles += scopus_response["articles"]
            next_url = scopus_response["next_url"]
            round_progress = int(len(articles) * 100 / self.articles_amount) if int(
                   len(articles) * 100 / self.articles_amount) <= 100 else 100
            #print(round_progress)
            self.round_progress=round_progress
            self.article=articles
            #print(articles)
            #self.update_progress.emit(round_progress)  # emite o sinal desejado, que é recebido update_progress.connect
        print(articles)
        print("self.article")
        print(self.article)
        return self.get_article(articles) #Mudança vagner Salva Artigos em uma variável
       # return articles #criado por Vagner
        #self._create_csv(articles[0:self.articles_amount])

    def get_article(self,articles):
        return articles
    
    def _create_csv(self, articles: dict):
        try:
            # df = clean_scopus(pd.DataFrame(articles))
            df = pd.DataFrame(articles)
            df.to_csv(self.fname, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
        except Exception as e:
            print('Erro na geracao do dataframe scopus')
            print(e)

    def error_handling(self, status_code: int, reason: str, downloaded_articles: int):
        code = int(status_code)
        if code == 400:
            error = {'error': 'Problema na requisição', 'downloaded_articles': downloaded_articles}
        elif code == 401:
            error = {'error': 'Problema na autenticação.', 'downloaded_articles': downloaded_articles}
        elif code == 403:
            error = {'error': 'Problema na autorização.', 'downloaded_articles': downloaded_articles}
        elif code == 429:
            error = {'error': 'Quota excedida.', 'downloaded_articles': downloaded_articles}
        else:
            error = {'error': 'Erro na obtenção dos artigos.', 'downloaded_articles': downloaded_articles}
        self.error_responses.emit(error)
