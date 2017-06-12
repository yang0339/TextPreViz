from TextProcessing import pre_processing, normalizing, detokenize,remove_symbols, remove_punc
import pandas as pd
header = ['timeStamp', 'user', 'text']
df = pd.read_csv("C:/Users/fredyang/Documents/GitHub/Python3-SMUMSO/MSO_Restart/atHDB_20170607.txt", sep='\t',
                 encoding='utf-8', names=header)

df['processed_text'] = pre_processing(df.text)
print(df.processed_text.head(3))

df['normalized'] = normalizing(remove_symbols(df.processed_text), 'lemma')
df['normalized'] = remove_punc(df.normalized)
df['normalized'] = detokenize(df['normalized'])
print(df.normalized)
