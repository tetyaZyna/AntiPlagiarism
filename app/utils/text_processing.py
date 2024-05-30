import re


class TextProcessor:
    def __init__(self, text):
        self.text = text
        self._clean_text()

    def get_sentences(self):
        return self._split_into_sentences()

    def get_cleaned_text(self):
        return self.text

    def _clean_text(self):
        cleaned_text = re.sub(r'[^\w\s.]', '', self.text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text.strip()
        # print("\n\n\n===================Cleaned===================\n\n\n")
        # print(cleaned_text)
        self.text = cleaned_text

    def _split_into_sentences(self):
        sentence_endings = r"[.!?]\s+"
        sentences = re.split(sentence_endings, self.text)
        # print("\n\n\n===================Split===================\n\n\n")
        # print(sentences)
        return self._remove_short_sentences(sentences)

    @staticmethod
    def _remove_short_sentences(sentences, min_sentence_length=40):
        filtered_sentences = []
        for sentence in sentences:
            if len(sentence) >= min_sentence_length:
                filtered_sentences.append(sentence)
        # print("\n\n\n===================Cleaned sentences===================\n\n\n")
        # print(filtered_sentences)
        return filtered_sentences
