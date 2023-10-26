from dotenv import load_dotenv
import os

load_dotenv()

apiKey = os.getenv('SCOPUS_API_KEY')
searchUrl = 'https://api.elsevier.com/content/search/scopus'
params = {
    'apiKey': apiKey,
    'view': 'COMPLETE',
    'count': '25',
    'cursor': '*'
}

headers = {"Accept": "application/json"}
