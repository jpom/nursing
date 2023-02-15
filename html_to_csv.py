import csv
from bs4 import BeautifulSoup

def extract_data(html_file):
    with open(html_file, 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')
        # soup = BeautifulSoup(file.read(), 'html.parser', from_encoding='ISO-8859-1')

        parts = soup.find_all('div', {'class': 'part'})
        data = []

        for part in parts:
            part_title = part.find('h1', {'class': 'part-title'}).text
            chapters = part.find_all('section', {'class': 'chapter'})

            for chapter in chapters:
                chapter_title = chapter.find('h1', {'class': 'chapter-title'}).text
                elements = chapter.find_all(['h2', 'p', 'li', 'h3', 'h4'])
                heading = ""  # initialize heading to an empty string
                text = ""  # initialize text to an empty string
                for i in range(len(elements)):
                    element = elements[i]
                    if element.name == 'h2':
                        if text:  # if text is not empty, append the previous data to the `data` list
                            data.append([part_title, chapter_title, heading, text.strip()])
                        heading = element.text
                        text = ""  # reset the text to an empty string
                    else:
                        text += element.text + " "  # append the text

                # handle the case where the last element is a `p` tag
                if text:
                    data.append([part_title, chapter_title, heading, text.strip()])

        return data

def write_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Part Title', 'Chapter Title', 'Heading', 'Text'])
        writer.writerows(data)

if __name__ == '__main__':
    html_file = 'Nursing-Fundamentals.html'
    csv_file = 'Nursing_Fundamentals_Raw_Data.csv'

    data = extract_data(html_file)
    write_to_csv(data, csv_file)
