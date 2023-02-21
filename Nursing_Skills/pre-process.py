import csv
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextLineHorizontal, LTTextBoxHorizontal
import pandas as pd
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

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

def merge_similar_subsections():
  # Load the data into a pandas DataFrame
  df = pd.read_csv('extracted_data.csv')

  # Initialize variables
  merged_rows = []
  current_row = df.loc[0]

  # Iterate through each row in the DataFrame
  for i in range(1, len(df)):
      # If the current row's subsection is the same as the next row's subsection
      if current_row['Subsection'] == df.loc[i, 'Subsection']:
          # Merge the two rows
          current_row['Text'] += '\n' + df.loc[i, 'Text']
      else:
          # Add the current row to the list of merged rows
          merged_rows.append(current_row)
          # Set the current row to the next row
          current_row = df.loc[i]

  # Add the final row to the list of merged rows
  merged_rows.append(current_row)

  # Create a new DataFrame from the merged rows
  merged_df = pd.DataFrame(merged_rows)

  # Save the merged DataFrame to a new CSV file
  merged_df.to_csv('merged_subsections_file.csv', index=False)

def merge_coloumn():
  # Load the CSV file into a Pandas DataFrame
  df = pd.read_csv("merged_subsections_file.csv")

  # Concatenate columns 1 and 2 into a single column
  df["title"] = df.iloc[:,0].astype(str) + " " + df.iloc[:,1].astype(str)

  # Concatenate columns 3 and 4 into a single column
  df["heading"] = df.iloc[:,2].astype(str) + " " + df.iloc[:,3].astype(str)

  # Concatenate columns 1, 2, 3, and 4 into a single column
  df["content"] = df.iloc[:,0].astype(str) + " " + df.iloc[:,1].astype(str) + " " + df.iloc[:,2].astype(str) + " " + df.iloc[:,3].astype(str)

  # Drop the first 4 columns
  df.drop(df.columns[0:4], axis=1, inplace=True)

  # Save the updated DataFrame to a new CSV file
  df.to_csv("merged_columns_file.csv", index=False)

def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))

def process_csv(input_file, output_file):
    # data = pd.read_csv(input_file)
    data = pd.read_csv(input_file, encoding='ISO-8859-1')
    data['tokens'] = data['content'].apply(count_tokens)
    data.to_csv(output_file, index=False)

filename = 'Nursing_Skills.pdf'
data = extract_text(filename)
write_csv('extracted_data.csv', data)
merge_similar_subsections()
merge_coloumn()
process_csv("merged_columns_file.csv", "finalwithtokens.csv")
