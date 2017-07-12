# -*- encoding: utf-8 -*-
"""
Pre-Processing of series text to:
    - remove urls
    - remove emoji & smileys (replace with $EMOJI$)
    - Specifically for social media data:
        - remove retweet
        - remove @user (replace with $NAME$)
        - remove # in #hashtag
        - remove numbers (replace with $NUM$)
    - use self-defined dictionaries to regularize unstructured expressions (e.g. hahaha.. -> ha; idk -> I do not know)

Normalize text to:
    - tokenize -> lowercase -> remove stopwords
    - Stemming or Lemmatization depends on choice
"""
# INPUT: DataFrame series
# OUTPUT: DataFrame series

def pre_processing(series, remove_retweet):

    import pandas as pd
    import re
    import warnings
    warnings.filterwarnings("ignore")

    # Define Regex
    URL_PATTERN = re.compile(r'https?:\/\/. *[\r\n\S]*')
    MENTION_PATTERN = re.compile(r'@\w*')
    EMOJI_PATTERN = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\u2600-\u27BF"          # Other USC-2
                               "]+", flags=re.UNICODE)
    SMILEYS_PATTERN = re.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}", re.IGNORECASE)
    NUMBERS_PATTERN = re.compile(r"(| )\d+(\S|\w)+")


    # 1. remove url
    series.replace(to_replace=URL_PATTERN, value='', regex=True, inplace=True)
    # 2. remove emoji
    series.replace(to_replace=EMOJI_PATTERN, value='$EMOJI$', regex=True, inplace=True)
    series.replace(to_replace=SMILEYS_PATTERN, value='$EMOJI$', regex=True, inplace=True)
    # 3. Remove retweets
    if remove_retweet==True:
        series = series[~series.str.startswith('RT', na=False)] # have to use na=False to stop ErrorMessage
        series.reset_index(drop=True, inplace=True)
    else:
        series.replace(to_replace='^RT', value='', regex=True, inplace=True)
    # 4. userMention '@': replace with $NAME$
    series.replace(to_replace=MENTION_PATTERN, value='$NAME$', regex=True, inplace=True)
    # 5. Hashtag: replace with $HASH$
    series.replace(to_replace='#', value=' ', regex=True, inplace=True)
    # 6. remove numbers
    series.replace(to_replace=NUMBERS_PATTERN, value='$NUM$', regex=True, inplace=True)

    # Regularize Unstructured Text
    import pkg_resources
    DATA_PATH = pkg_resources.resource_filename('TextPreViz','self_constructed_dict.csv')
    df_dict = pd.read_csv(DATA_PATH, sep=",", names=['original','normalized'])
    df_dict.fillna(value='', inplace=True)

    # output as dictionary (hash table) to speed up process
    dict = df_dict.set_index('original')['normalized'].to_dict()
    text_normalized_list = []

    for items in series:
        text_normalized = items  # make a copy to change
        for key,val in dict.items():
            # skip if-search regex condition to speed up
            text_normalized = re.compile(r'(^|([,.!? ]))%s(([,.!? ])|$)'%key, re.IGNORECASE)\
                            .sub(' %s '%val, text_normalized) # make sure it is a separate word

        # last step: remove extra space
        text_normalized = re.sub(r'\s+', r' ', text_normalized)
        text_normalized = re.sub(r'^\s+', r'', text_normalized)

        text_normalized_list.append(text_normalized)

    return text_normalized_list


def remove_symbols(series):

    l = ["\$NAME\$","\$NUM\$","\$EMOJI\$"]
    for _ in l:
        series.replace(to_replace=_, value=' ', regex=True, inplace=True)
    return series



def remove_punc(series):
    import string
    series = series.apply(lambda x:
                    [item for item in x if item not in string.punctuation])
    return series



def normalizing(series, method):

    import nltk # if corpus not downloaded use: nltk.download()
    import re
    series = series.apply(lambda x: re.sub(r'[^\x00-\x7F]+', ' ', x))  # remove non-ASCII characters
    # tokenize
    from nltk import word_tokenize
    series = series.apply(lambda x: word_tokenize(x))
    # to lowercase
    series = series.apply(lambda x: [item.lower() for item in x])
    # remove stopwords
    from nltk.corpus import stopwords
    series = series.apply(lambda x: [item for item in x if item not in stopwords.words('english')])
    # Stemming or Lemmatization
    if method == 'stem':
        from nltk.stem.snowball import SnowballStemmer
        stemmer = SnowballStemmer("english")
        series = [[stemmer.stem(w) for w in wordlist] for wordlist in series]
    if method == 'lemma':
        from nltk.stem.wordnet import WordNetLemmatizer
        lem = WordNetLemmatizer()
        series = [[lem.lemmatize(w) for w in wordlist] for wordlist in series]

    return series

def detokenize(series):
    return [' '.join(item) for item in series]