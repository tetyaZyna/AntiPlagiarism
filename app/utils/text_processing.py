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
        return self._validate_short_sentences(sentences)

    @staticmethod
    def _validate_short_sentences(sentences, min_sentence_length=40, max_sentence_length=250):
        filtered_sentences = []

        for sentence in sentences:
            if len(sentence) < min_sentence_length:
                continue
            elif len(sentence) > max_sentence_length:
                num_parts = (len(sentence) + max_sentence_length - 1) // max_sentence_length
                part_length = len(sentence) // num_parts

                for i in range(num_parts):
                    start = i * part_length
                    if i == num_parts - 1:
                        part = sentence[start:]
                    else:
                        part = sentence[start:start + part_length]

                    if len(part) >= min_sentence_length:
                        filtered_sentences.append(part)
            else:
                filtered_sentences.append(sentence)

        return filtered_sentences
