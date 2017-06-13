from TextProcessing import pre_processing, normalizing, detokenize,remove_symbols, remove_punc
import pandas as pd
df = pd.read_excel("C:/Users/fredyang/Documents/GitHub/Python3-SMUMSO/MSO_Restart/HDB_annotated.xlsx")
df['processed_text'] = pre_processing(df.text)
print(df.processed_text.head(3))

df['normalized'] = normalizing(remove_symbols(df.processed_text), 'lemma')
df['normalized'] = remove_punc(df.normalized)
# df['normalized'] = detokenize(df['normalized'])
print(df.normalized.head(3))

from TextVisuals import word_cloud, find_neighbor, plot_hist
word_cloud(df[df.label.str.contains('Pet', na=False)].normalized, [], 'test')
word_cloud(find_neighbor(df[df.label.str.contains('Pet', na=False)].normalized, 'dog',3),[],'neightbor')


plot_hist(df.label,"haha")