import csv, types
import itertools
import pandas as pd
import time
from .clean_pubmed_data_frame import CleanPumedDataFrame
from servers.controllers.pymed.api import PubMed

from PyQt5.QtCore import QThread, pyqtSignal


class GetArticlesThreadPubmed(QThread):
    # cria sinal para valor que desejo enviar. Se for mais de 1 valor, basta declarar os tipos (int str dict), pe.
    update_progress = pyqtSignal(int)
    error_responses = pyqtSignal(dict)

    def __init__(self, query: str, articles_amount: int, batch: int, pubmed: PubMed, fname: str):
        super(QThread, self).__init__()
        self.query = query
        self.articles_amount = articles_amount
        self.batch = batch
        self.pubmed = pubmed
        self.fname = fname
        self.clean_pubmed_data_frame = CleanPumedDataFrame()

    def run(self):
        articles_ids = self.pubmed.getArticleIds(self.query, int(self.articles_amount))
        count_completed = 0
        articles = []
        for x in range(0, self.articles_amount, self.batch):
            result = self.pubmed.getArticles(articles_ids[x:  min(x + self.batch, self.articles_amount)])
            if not isinstance(result, types.GeneratorType):
                self.error_handling(len(articles))
                break
            iteravel = itertools.chain.from_iterable([result])
            articles_dict = [x.toDict() for x in iteravel]
            if len(articles_dict) > 0:
                articles += articles_dict
            count_completed += self.batch
            round_progress = int(count_completed * 100 / self.articles_amount) if int(
                count_completed * 100 / self.articles_amount) <= 100 else 100
            self.update_progress.emit(round_progress)  # emite o sinal desejado, que é recebido update_progress.connect
        
        #Alterado por Vagner
        print("pubmed thread:",articles)
        return self.get_articles(articles) # Neste caso o método run chama o método que retorna todos os artigos obtidos.
        #self._create_csv(articles) #No caso anterior, o valor era salvo em um arquivo csv.
    
    def get_articles(self,articles):
        return articles

    def _create_csv(self, articles: list) -> None:

        # iteravel = itertools.chain.from_iterable(articles)
        # articles_pymed = [article.toDict() for article in iteravel]
        try:

            df = self.clean_pubmed_data_frame.clean_pubmed(pd.DataFrame(articles))
            df.to_csv(self.fname, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
        except Exception as e:
            self.error_handling(0)

    def error_handling(self, downloaded_articles):
        error = {'error': 'Erro na obtenção dos artigos.', 'downloaded_articles': downloaded_articles}
        self.error_responses.emit(error)
