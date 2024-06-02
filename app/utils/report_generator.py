from docx import Document
import matplotlib.pyplot as plt
import io

from datetime import datetime


class ReportGenerator:

    def __init__(self):
        self.buffer = io.BytesIO()
        self.progression = {'excellent': ['#31C013', '#B5EFA9'],
                            'good': ['#68CC14', '#CCF2AB'],
                            'normal': ['#E6E317', '#F9F8B0'],
                            'bad': ['#E61C17', '#F9B2B0',]}
        self.template_path = "C:\\Киберхлам v.2.0\\Диплом\\Application\\app\\config\\template.docx" #todo

    def _load_template(self):
        doc = Document(self.template_path)
        return doc

    # def _generate_diagram(self, plagiarism_percentage):
    #     if plagiarism_percentage >= 90:
    #         colours = self.progression.get('excellent')
    #         short_result = 'excellent'
    #     elif plagiarism_percentage >= 80:
    #         colours = self.progression.get('good')
    #         short_result = 'good'
    #     elif plagiarism_percentage >= 70:
    #         colours = self.progression.get('normal')
    #         short_result = 'normal'
    #     else:
    #         colours = self.progression.get('bad')
    #         short_result = 'bad'
    #     fig = plt.figure(figsize=(5, 5), facecolor='#ffffff00')
    #     ax = fig.add_subplot(1, 1, 1)
    #     pie = ax.pie([plagiarism_percentage, 100 - plagiarism_percentage],
    #                  colors=colours,
    #                  startangle=90,
    #                  labeldistance=1.15,
    #                  counterclock=False)
    #     centre_circle = plt.Circle((0, 0), 0.6, fc='#ffffff')
    #     fig.gca().add_artist(centre_circle)
    #     centre_text = f' {plagiarism_percentage}%'
    #     centre_text_line_2 = f'{short_result}'
    #     ax.text(0, 0, centre_text, horizontalalignment='center',
    #             verticalalignment='center',
    #             fontsize=32, fontweight='bold',
    #             color='black')
    #     ax.text(0, -0.2, centre_text_line_2, horizontalalignment='center',
    #             verticalalignment='center',
    #             fontsize=12, fontweight='bold',
    #             color='grey')
    #     plt.savefig(self.buffer, format='png', bbox_inches='tight', pad_inches=0)
    #     plt.close()

    def _generate_progress_bar(self, plagiarism_percentage):
        if plagiarism_percentage >= 90:
            colors = self.progression.get('excellent')
            short_result = 'Excellent'
        elif plagiarism_percentage >= 80:
            colors = self.progression.get('good')
            short_result = 'Good'
        elif plagiarism_percentage >= 70:
            colors = self.progression.get('normal')
            short_result = 'Normal'
        else:
            colors = self.progression.get('bad')
            short_result = 'Bad'
        fig, ax = plt.subplots(figsize=(10, 1))
        ax.barh(0, 100, color=colors[1])
        ax.barh(0, plagiarism_percentage, color=colors[0])
        ax.text(50, 1, f'{plagiarism_percentage}% - {short_result}',
                ha='center', va='center', color='black', fontsize=14)
        ax.set_xlim(0, 100)
        ax.set_ylim(-1, 1)
        ax.axis('off')
        plt.savefig(self.buffer, format='png', bbox_inches='tight', pad_inches=0)
        plt.close()

    @staticmethod
    def _validate_percentage(plagiarism_percentage):
        if plagiarism_percentage < 0:
            return 0
        elif plagiarism_percentage > 100:
            return 100
        else:
            return round(plagiarism_percentage, 1)

    # def generate_document(self, plagiarism_percentage):
    #     valid_percentage = self.validate_percentage(plagiarism_percentage)
    #     self._generate_diagram(valid_percentage)
    #     self.buffer.seek(0)
    #     doc = Document()
    #
    #     section = doc.sections[0]
    #     section.left_margin = Inches(0.5)
    #     section.right_margin = Inches(0.5)
    #     section.different_first_page = True
    #
    #     self.add_header(section)
    #
    #
    #
    #
    #
    #
    #     heading = doc.add_heading('Results', level=1)
    #     heading.paragraph_format.left_indent = Inches(1.0)
    #
    #     doc.add_picture(self.buffer)
    #
    #     if len(doc.sections) > 1:
    #         section = doc.sections[1]
    #         for paragraph in section.header.paragraphs:
    #             paragraph.clear()
    #
    #     doc.save('document_with_progress_bar.docx')
    #     print("Ready")
    #

    #
    # @staticmethod
    # def add_header(section):
    #     header = section.header
    #
    #     section_width = section.page_width - section.left_margin - section.right_margin
    #
    #     table = header.add_table(rows=1, cols=2, width=section_width)
    #
    #     cell_left = table.cell(0, 0)
    #     cell_right = table.cell(0, 1)
    #
    #     left_paragraph = cell_left.paragraphs[0]
    #     left_run = left_paragraph.add_run("AntiPlagiarism")
    #     left_run.font.name = 'Arial'
    #     left_run.font.size = Pt(14)
    #     left_run.bold = True
    #     left_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    #
    #     right_paragraph = cell_right.paragraphs[0]
    #     right_run = right_paragraph.add_run(f"Generated:\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    #     right_run.font.name = 'Arial'
    #     right_run.font.size = Pt(10)
    #     right_run.bold = True
    #     right_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    #
    #     separator_paragraph = header.add_paragraph()
    #     separator_paragraph.add_run("__________________________________________________________________________________"
    #                                 "__________________________________________________")

    @staticmethod
    def _replace_text_in_paragraphs(paragraphs, old_text, new_text):
        for paragraph in paragraphs:
            if old_text in paragraph.text:
                paragraph.text = paragraph.text.replace(old_text, new_text)

    def _replace_text_in_tables(self, tables, old_text, new_text):
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    self._replace_text_in_paragraphs(cell.paragraphs, old_text, new_text)

    def _replace_text_in_headers(self, doc, old_text, new_text):
        for section in doc.sections:
            header = section.header
            footer = section.footer

            first_page_header = section.first_page_header
            first_page_footer = section.first_page_footer

            for hdr in [header, first_page_header]:
                self._replace_text_in_paragraphs(hdr.paragraphs, old_text, new_text)
                self._replace_text_in_tables(hdr.tables, old_text, new_text)

            for ftr in [footer, first_page_footer]:
                self._replace_text_in_paragraphs(ftr.paragraphs, old_text, new_text)
                self._replace_text_in_tables(ftr.tables, old_text, new_text)

    def _replace_text(self, doc, old_text, new_text, tables=False, headers=False):
        self._replace_text_in_paragraphs(doc.paragraphs, old_text, new_text)
        if tables:
            self._replace_text_in_tables(doc.tables, old_text, new_text)
        if headers:
            self._replace_text_in_headers(doc, old_text, new_text)

    def _add_diagram_image(self, doc):
        tables = doc.tables
        p = tables[0].rows[0].cells[0].add_paragraph()
        r = p.add_run()
        r.add_picture(self.buffer)

    def generate_document(self, plagiarism_percentage, filename):
        doc = self._load_template()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._replace_text(doc, '[time_generated]', current_time, True, True)
        self._replace_text(doc, '[filename]', f'"{filename}"')
        self._generate_progress_bar(self._validate_percentage(plagiarism_percentage))
        self._add_diagram_image(doc)
        doc.save("new_docx.docx")


gen = ReportGenerator()
gen.generate_document(100, "звіт.docx")


