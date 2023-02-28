import csv
from transformers import GPT2TokenizerFast
import pandas as pd

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))

def process_csv(input_file, output_file):
    # data = pd.read_csv(input_file)
    data = pd.read_csv(input_file, encoding='ISO-8859-1')
    data['tokens'] = data['content'].apply(count_tokens)
    data.to_csv(output_file, index=False)

process_csv("merged_columns_file.csv", "finalwithtokens.csv")
