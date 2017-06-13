# TextPreViz

### Created 2017-JUN-12
This package wraps nltk, matplotlib to aids text analysis and visualization.

### Two sub-packages to use:
#### TextProcessing
Generally speaking, do text processing <br>
notes: *series* as input is to indicates *pandas series*
* **pre_processing(series)**
    - remove urls
    - remove emoji and smileys (replace with $EMOJI$)
    - Specifically for social media data:
        - remove retweet
        - remove @user (replace with $NAME$)
        - remove \# in \#hashtag
        - remove numbers (replace with $NUM$)
    - use self-defined dictionaries to regularize unstructured expressions (e.g. hahaha.. -> ha; idk -> I do not know)

* **remove_symbols(series)**
    - if *pre-processing* is used ahead while tags as $EMOJI$ etc. seems redundant for subsequent analysis, use this module to clear it up.
* **remove_punc(series)**
    - remove puctuation remarks.
    - have to be implemented in tokenized manner, recommended to be used after *normalization*
* **normalizing(series, method)**
    - standard nltk text-normalization process
    - *method* to indicate "stem" or "lemma" as to represent desired process
    - tokenize -> lower case -> remove stopwords -> stemming/lemmatizing
* **detokenize(series)**
    - *normalizing* returns a series with tokenized text (e.g. ```>>>['i','like','python']```) 
    - using this module to join them together (e.g. ```>>>'i like python'```)

##### Use case

Modules can be cascaded together for concise programming:
```python
from TextProcessing import * 
# df.text is the pandas series storeing raw unprocessed text
detokenize(remove_punc(normalizing(remove_symbols(pre_processing(df.text)), 'lemma')))
```
Or you can distinctively store intermediate steps in DataFrame as well
```python
df['pre-processing'] = pre_processing(df.text)
df['normalized'] = normalizing(remove_symbols(df['pre-processing']),'stem')
df['detokenized'] = detokenize(remove_punc(df['normalized']))
```

#### TextVisuals
Provide high-level API to create histograms for stats and WordCloud to view keywords.
* **plot_barh(series, title, highest)**
    - horizontal bar plot to visualize how many counts in each categories 
    - Display will be given in sorted manner
    - specify *title* in the chart and top x categories (*highest*) to start with
* **word_cloud(input, remove_list, title)**
    - input can be given as both *pandas series* or *list* (words already tokenized) e.g.```>>>['apple','banana','car']```)
    - self-defind list as *remove_list* to get rid of undesired words displayed
    - *title*: give a title to the viz
* **find_neighbor(series, key, distance)**
    - a supplementary to aids plotting word cloud
    - finding the words distribution of *distance* x near a particular search word (*key*) 
    
##### Examples
```python
from TextVisuals import *
plot_barh(df[df.label!=0].label,"example barh_plot",3) # top 3 labels
```
![e-barhplot](https://github.com/yang0339/TextPreViz/blob/master/Visual%20examples/example_plot_barh.png)

```python
from TextVisuals import *
word_cloud(df[df.label.str.contains('Pet', na=False)].normalized, [], 'Word Cloud of Pet Category')
word_cloud(find_neighbor(df[df.label.str.contains('Pet', na=False)].normalized, ['cat','cats', 'dog', 'dogs'], 3),['pls'], '\"cat(s) & dog(s)\"\'s nearest 3 neighbors')
```
![e1](https://github.com/yang0339/TextPreViz/blob/master/Visual%20examples/word_cloud1.png)
![e2](https://github.com/yang0339/TextPreViz/blob/master/Visual%20examples/word_cloud2.png)