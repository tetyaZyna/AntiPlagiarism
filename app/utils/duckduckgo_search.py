import random
import time

import requests
from bs4 import BeautifulSoup


class DuckDuckGoSearch:
    def __init__(self):
        self.headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Connection': 'keep-alive'
            },
            # {
            #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
            #                   '(KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            #     'Connection': 'keep-alive'
            # },
            # {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            #                   '(KHTML, like Gecko) Edge/95.0.1020.53 Safari/537.36',
            #     'Connection': 'keep-alive'
            # }
        ]
        self.session = requests.Session()

    def search(self, query, attempts=0):
        if attempts <= 5:
            # start_time = time.time()

            time.sleep(random.uniform(0, 1))

            url = f"https://duckduckgo.com/html/?q={query}"
            headers = self._generate_header()
            response = self.session.get(url, headers=headers, timeout=10, allow_redirects=True)

            if response.status_code == 202:
                response = self.search(query, attempts+1)

            # end_time = time.time()
            # execution_time = end_time - start_time
            # print(f"response execution time: {execution_time:.4f} seconds")
        else:
            return [{'title': '', 'link': '', 'snippet': ''}]

        return self._parce_response(response)

    @staticmethod
    def _parce_response(response):
        # start_time = time.time()

        soup = BeautifulSoup(response.text, 'lxml')
        result_divs = soup.find_all('div', class_='result')
        results = []
        for div in result_divs:
            title = div.find('a', class_='result__a').text
            link = div.find('a', class_='result__url').text
            snippet = div.find('a', class_='result__snippet').text
            results.append({'title': title, 'link': link, 'snippet': snippet})

        # end_time = time.time()
        # execution_time = end_time - start_time
        # print(f"parser execution time: {execution_time:.4f} seconds")

        return results

    @staticmethod
    def _generate_user_agent():
        windows_versions = ['Windows NT 10.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0']
        webkit_versions = ['AppleWebKit/' + str(random.randint(500, 600)) + '.' + str(random.randint(0, 99)) for _ in
                           range(3)]
        edge_versions = ['Edge/' + str(random.randint(80, 95)) + '.' + str(random.randint(0, 999)) + '.' + str(
            random.randint(0, 9999)) for _ in range(3)]
        return f'Mozilla/5.0 ({random.choice(windows_versions)}; Win64; x64) ' + \
            f"{' '.join(webkit_versions)} " + \
            f"{random.choice(edge_versions)} " + \
            f"Safari/{random.randint(500, 600)}.{random.randint(0, 99)}"

    def _generate_header(self):
        return \
            {
                'User-Agent': f'{self._generate_user_agent()}',
                'Connection': 'keep-alive'
            }
