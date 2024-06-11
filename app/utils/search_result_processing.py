import re
from difflib import SequenceMatcher

# from models.plagiarism_case import PlagiarismCase


class SearchResultProcessor:
    def get_report_data(self, found_plagiarism, sentences_count):
        return self._analise_input_data(found_plagiarism, sentences_count)

    def get_plagiarism_case(self, sentences, search_text):
        max_percentage = 0
        max_result = {}
        for sentence in sentences:
            if sentence.get('snippet'):
                sentence_found = self._clean_text(sentence.get('snippet'))
                percentage = SequenceMatcher(None, search_text, sentence_found).ratio()
                if max_percentage < percentage:
                    max_percentage = percentage
                    max_result = sentence
        if max_percentage > 0.5:
            return {'sentence': max_result.get('snippet'),
                    'plagiarism_rate': max_percentage,
                    'link': max_result.get('link')}
            # return PlagiarismCase(max_result.get('snippet'), max_percentage, max_result.get('link'))
        else:
            return None

    @staticmethod
    def _analise_input_data(found_plagiarism, sentences_count):
        general_plagiarism_rate = 0
        for case in found_plagiarism:
            if case.get('plagiarism_rate') >= 0.8:
                general_plagiarism_rate += 1
            else:
                general_plagiarism_rate += case.get('plagiarism_rate')
        if sentences_count == 0:
            return 0
        else:
            plagiarism_percentages = (general_plagiarism_rate / sentences_count) * 100
            return plagiarism_percentages

    @staticmethod
    def _clean_text(text):
        cleaned_text = re.sub(r'[^\w\s.]', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text.strip()
        return cleaned_text.strip()
