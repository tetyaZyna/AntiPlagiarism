import requests
from bs4 import BeautifulSoup


class NoSearchResultsError(Exception):
    """No search results found."""
    pass


class ScrapGoogleSearch:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                        }

    @staticmethod
    def reject_cookies(soup):
        form_action = None
        data = {}

        forms = soup.find_all('form')
        for form in forms:
            for input_field in form.find_all('input', type="submit"):
                value = input_field.get('value')
                if value != "Reject all":
                    continue
            form_action = form['action']
            for input_field in form.find_all('input'):
                name = input_field.get('name')
                if name:
                    data[name] = input_field.get('value')

        response = requests.post(form_action, data=data)
        return response

    def search(self, query):
        url = 'https://www.google.com/search?&q=' + query
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('div', class_='saveButtonContainer'):
            response = self.reject_cookies(soup)
            soup = BeautifulSoup(response.text, 'html.parser')

        result_divs = soup.find_all('div', class_='Gx5Zad fP1Qef xpd EtOod pkphOe')
        results = []
        for div in result_divs:
            if div.find('div', class_='egMi0 kCrYT') is None:
                continue
            title = div.find('h3').text
            link = div.find('a')['href']
            snippet = div.find('div', class_='BNeawe s3v9rd AP7Wnd').text

            results.append({'title': title, 'link': link, 'snippet': snippet})

        return results
        # todo: развести на отдельній поток, ускорить

        # if len(results) > 0:
        #     return results
        # else:
        #     raise NoSearchResultsError
