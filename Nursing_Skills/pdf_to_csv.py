import csv
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextLineHorizontal, LTTextBoxHorizontal

def get_fontname(element):
    font = element.font
    if hasattr(font, 'fontname'):
        return font.fontname
    elif hasattr(font, 'basefont'):
        return font.basefont
    else:
        return 'Unknown'

def extract_text(filename):
    data = []
    chapter = ''
    section = ''
    subsection = ''
    text = ''
    with open(filename, 'rb') as f:
        for page_layout in extract_pages(f):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    for text_line in element:
                        if isinstance(text_line, LTTextLineHorizontal):
                            font_size = text_line.height
                            if font_size == 15:
                                chapter = text_line.get_text().strip()
                                section = ''
                                subsection = ''
                            elif font_size == 16:
                                section = text_line.get_text().strip()
                                subsection = ''
                            elif font_size == 21:
                                subsection = text_line.get_text().strip()
                            elif font_size >= 13.5 and subsection != '':
                                text += text_line.get_text().strip()
                    if text:
                        data.append([chapter, section, subsection, text])
                        text = ''
    return data

def write_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Chapter', 'Section', 'Subsection', 'Text'])
        writer.writerows(data)

filename = 'Nursing_Skills.pdf'
data = extract_text(filename)
write_csv('extracted_data.csv', data)

