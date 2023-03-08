import csv
from bs4 import BeautifulSoup
import pandas as pd
import csv
from transformers import GPT2TokenizerFast
import pandas as pd

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def remove_empty_rows():
  # Load the CSV file into a Pandas DataFrame
  df = pd.read_csv("Nursing_Fundamentals_Raw_Data.csv")
  # Drop the rows where the third column is empty
  df = df.dropna(subset=[df.columns[2]])
  # Save the updated DataFrame to a new CSV file
  df.to_csv("Nursing_Fundamentals_Removed_Empty_Rows.csv", index=False)


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

def merge_columns():
  # Load the CSV file into a Pandas DataFrame
  df = pd.read_csv("Nursing_Fundamentals_Removed_Empty_Rows.csv")

  # Concatenate columns 1 and 2 into a single column
  df["title"] = df.iloc[:,0].astype(str) + " " + df.iloc[:,1].astype(str)

  # Concatenate columns 3 and 4 into a single column
  df["heading"] = df.iloc[:,2].astype(str) + " " + df.iloc[:,3].astype(str)

  # Concatenate columns 1, 2, 3, and 4 into a single column
  df["content"] = df.iloc[:,0].astype(str) + " " + df.iloc[:,1].astype(str) + " " + df.iloc[:,2].astype(str) + " " + df.iloc[:,3].astype(str)

  # Drop the first 4 columns
  df.drop(df.columns[0:4], axis=1, inplace=True)

  # Save the updated DataFrame to a new CSV file
  df.to_csv("Nursing_Fundamentals_Merged_File.csv", index=False)


def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))

def process_csv(input_file, output_file):
    # data = pd.read_csv(input_file)
    data = pd.read_csv(input_file, encoding='ISO-8859-1')
    data['tokens'] = data['content'].apply(count_tokens)
    data.to_csv(output_file, index=False)


if __name__ == '__main__':
    html_file = 'Nursing-Fundamentals.html'
    csv_file = 'Nursing_Fundamentals_Raw_Data.csv'

    data = extract_data(html_file)
    write_to_csv(data, csv_file)
    remove_empty_rows()
    merge_columns()
    process_csv("Nursing_Fundamentals_Merged_File.csv", "nursing_fundamental_finalwithtokens.csv")
