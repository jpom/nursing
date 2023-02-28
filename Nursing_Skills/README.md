# Nursing_Skills_and_Fundamentals

## Pre-Processing of Book in HTML

Step 1: Run python .\pdf_to_csv.py, it will take Nursing-Fundamentals.html and it will generate Nursing_Fundamentals_Raw_Data.csv

Step 2: Run python .\merge_similar_subsections.py, it will take Nursing_Fundamentals_Raw_Data.csv and it will generate Nursing_Fundamentals_Removed_Empty_Rows.csv

Step 3: Run python .\merge_columns.py, it will take Nursing_Fundamentals_Removed_Empty_Rows.csv and it will generate Nursing_Fundamentals_Merged_File.csv

Step 4: Run python add_tokens.py, it will take Nursing_Fundamentals_Merged_File.csv and it will generate nursing_fundamental_finalwithtokens.csv

## The OpenAI Embedding Fine-Tune For Nursings Skills

Run Jupyter Notebook create-embeddings.ipynb for create embeddings
Run Jupyter Notebook test-model.ipynb for testing embedding Q/A