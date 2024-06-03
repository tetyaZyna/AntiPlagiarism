class SearchResultProcessor:
    def get_report_data(self, found_plagiarism, sentences_count):
        return self._analise_input_data(found_plagiarism, sentences_count)

    @staticmethod
    def _analise_input_data(found_plagiarism, sentences_count):
        general_plagiarism_rate = 0
        for case in found_plagiarism:
            if case.plagiarism_rate >= 0.8:
                general_plagiarism_rate += 1
            else:
                general_plagiarism_rate += case.plagiarism_rate
        if sentences_count == 0:
            return 0
        else:
            plagiarism_percentages = (general_plagiarism_rate / sentences_count) * 100
            return plagiarism_percentages
