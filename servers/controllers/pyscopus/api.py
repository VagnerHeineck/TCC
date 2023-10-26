import requests
from requests import Response
import datetime
from .helpers_scopus import params, searchUrl, headers


class Scopus:
    #first_page = None

    #api_key = params_api_key = params['apiKey']

    def _update_rates(self, resp: Response):
        self.rateLimit = resp.headers['X-RateLimit-Limit']
        self.remaining_rate = resp.headers['X-RateLimit-Remaining']
        rate_reset_epoch = float(resp.headers['X-RateLimit-Reset']) / 1000
        self.rate_reset = datetime.datetime.fromtimestamp(rate_reset_epoch).strftime('%d/%m/%Y %H:%M:%S')

    def get_rates(self):
        return {'rate_limit': self.rateLimit, 'remaining_rate': self.remaining_rate, 'rate_reset': self.rate_reset}

    def error_handling(self, status_code: int):
        code = status_code
        if code == 400:
            return {"results": None, "error_message": 'Erro: problema na requisição.'}
        elif code == 401:
            return {"results": None, "error_message": 'Erro: problema na autenticação da API Key.'}
        elif code == 403:
            return {"results": None, "error_message": 'Erro: problema na autorização da API Key.'}
        elif code == 429:
            return {"results": None,
                    "error_message": f'Erro: quota excedida. Quota será reiniciada em {self.rate_reset}'}
        else:
            return {"results": None, "error_message": 'Erro na obtenção do resultado.'}

    def get_total_results_count(self, query: str):
        _params = params.copy()
        _params['query'] = query
        search = requests.get(url=searchUrl, params=_params, headers=headers)

        if search.status_code not in range(200, 299):
            _params.pop('cursor')
            _params['view'] = 'STANDARD'
            search = requests.get(url=searchUrl, params=_params, headers=headers)
            if search.status_code not in range(200, 299):
                return self.error_handling(status_code=search.status_code)
        self._update_rates(search)
        resp_json = search.json()
        results = resp_json['search-results']['opensearch:totalResults']
        self.first_page: dict = resp_json
        return {"results": results, "error_message": None}

    def get_next_url(self, resp_json: dict) -> str or None:
        for item in resp_json['search-results']['link']:
            if item['@ref'] == 'next':
                return item['@href']
        return None

    def process_results(self, resp_json: dict) -> list:
        return resp_json['search-results']['entry']

    def getArticles(self, url: str):
        #headers = {"X-ELS-APIKey": self.api_key, "Accept": 'application/json'}

        search = requests.get(url, headers=headers)
        resp_json = search.json()
        articles = self.process_results(resp_json)
        next_url = self.get_next_url(resp_json)
        self._update_rates(search)

        return {"articles": articles, "next_url": next_url, "error": None}
