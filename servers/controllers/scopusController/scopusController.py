from requests import Response

from .get_articles_thread_scopus import GetArticlesThreadScopus

import requests
from .helpers_scopus import params, searchUrl
import datetime
from servers.controllers.pyscopus.api import Scopus


class ScopusController:
    # _articles = None

    #first_page = None
    scopus = Scopus()

    def get_total_results_count(self, query: str):
        total_count = self.scopus.get_total_results_count(query)
        #self.first_page = self.scopus.first_page

        return {"results": total_count['results'], "error_message": total_count['error_message']}

    def get_articles(self, articles_amount: int, fname: str) -> GetArticlesThreadScopus:
        escaped_fname = self._escape_fname(fname)
        return GetArticlesThreadScopus(articles_amount=articles_amount, fname=escaped_fname, scopus=self.scopus) #first_page=self.first_page,
                                            
        #if _articles.search:
         #   self._update_rates(_articles.search)
        #return _articles

    def _escape_fname(self, fname: str):
        return fname.replace('/', '\\')
