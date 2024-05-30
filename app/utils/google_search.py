from googleapiclient.discovery import build


class GoogleSearch:
    def __init__(self):
        self.my_cse_id = "94fd014cd241f4580"
        self.dev_key = "AIzaSyCex7LeNnrCiqnwgKw7-EE6W0BPObtGGuA"

    def search(self, search_term, **kwargs):
        service = build("customsearch", "v1", developerKey=self.dev_key)
        res = service.cse().list(q=search_term, cx=self.my_cse_id, **kwargs).execute()
        if res['searchInformation'].get('totalResults') == '0':
            return 0
        return res['items']
