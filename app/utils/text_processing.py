import re


class TextProcessor:
    def get_sentences(self, text):
        return self._split_into_sentences(text)

    def get_cleaned_text(self, text):
        return self._clean_text(text)

    @staticmethod
    def _clean_text(text):
        cleaned_text = re.sub(r'[^\w\s.]', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text.strip()
        return cleaned_text.strip()

    def _split_into_sentences(self, text):
        sentence_endings = r"[.!?]\s+"
        text = self._clean_text(text)
        sentences = re.split(sentence_endings, text)
        return self._remove_short_sentences(sentences)

    @staticmethod
    def _remove_short_sentences(sentences, min_sentence_length=40):
        filtered_sentences = []
        for sentence in sentences:
            if len(sentence) >= min_sentence_length:
                filtered_sentences.append(sentence)
        return filtered_sentences
