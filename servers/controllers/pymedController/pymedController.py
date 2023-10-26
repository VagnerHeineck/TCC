from servers.controllers.pymed.api import PubMed
from .get_articles_thread_pubmed import GetArticlesThreadPubmed
from dotenv import load_dotenv
import os

load_dotenv()

tool = os.getenv('PUBMED_TOOL_NAME')
email = os.getenv('PUBMED_EMAIL')


class PymedController:
    pubmed = PubMed(tool=tool, email=email)

    _articles = None

    def get_total_results_count(self, query: str):
        results = self.pubmed.getTotalResultsCount(query)
        try:
            results = int(results)
            return {"results": results, "error_message": None}
        except:
            return {"results": None, "error_message": "Erro na obtenção do resultado."}

    def get_articles(self, query: str, articles_amount: int, batch: int,
                                   fname: str) -> GetArticlesThreadPubmed:
        escaped_fname = self._escape_fname(fname)
        total_articles_amount = self._get_articles_amount(articles_amount, query)
        self._articles = GetArticlesThreadPubmed(query=query, articles_amount=total_articles_amount, batch=batch,
                                                 pubmed=self.pubmed,
                                                 fname=escaped_fname)
        return self._articles

    def _get_articles_amount(self, articles_amount: int, query: str) -> int:
        total_results_count = self.get_total_results_count(query)["results"]
        
        if total_results_count is None:
            return 0
        if articles_amount >= total_results_count:
            return total_results_count
        return articles_amount

    def _escape_fname(self, fname: str) -> str:
        return fname.replace('/', '\\')
