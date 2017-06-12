def word_cloud(input, remove_list, title): # series is TOKENIZED
    # which type of input
    import pandas
    if isinstance(input, pandas.core.series.Series):
        word_list = [w for sublist in input for w in sublist] # flatten nested list
    if isinstance(input, list):
        word_list = input

    # add some default removable _s
    remove_list += ['...','\'s','n\'t']
    for _ in remove_list:
        try:
            while _ in word_list:
                word_list.remove(_)
        except ValueError:
            pass  # in case it does not contain such word to be removed

    from collections import Counter
    cnt = Counter(word_list)

    def grey_color_func(word, font_size, position, orientation,
                        **kwargs):
        return "hsl(219, 100%%, %d%%)" % cnt_lumin[word]

    # scaling count: luminance suitable range 35-85
    cnt_lumin = cnt.copy()
    min_v = 1 / cnt[max(cnt, key=cnt.get)]
    max_v = 1 / cnt[min(cnt, key=cnt.get)]
    multiplier = 60 / (max_v - min_v)
    bias = 35 - min_v * multiplier
    for _ in cnt.keys():
        cnt_lumin[_] = 1 / cnt[_] * multiplier + bias

    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    wordcloud = WordCloud(background_color='white', max_font_size=50, mask=None)
    wc = wordcloud.generate_from_frequencies(frequencies=cnt)
    plt.figure()
    wc.recolor(color_func=grey_color_func, random_state=3)
    # interpolation check: https://matplotlib.org/devdocs/gallery/images_contours_and_fields/interpolation_methods.html
    plt.imshow(wc, interpolation="sinc")
    plt.axis("off")
    plt.title(title)
    plt.show()

    return


def find_neighbor(series, key, distance):
    neighbor_word = []
    for text_list in series:
        num = 0
        index_list = []
        for _ in text_list:
            if _==key:
                index_list.append(num)
            num+=1

        for num in index_list:
            for c in range(1,distance+1):
                if c <= num: # if reached the start
                    neighbor_word.append(text_list[num-c])
                if c+num <=len(text_list)-1: # if reached the end
                    neighbor_word.append(text_list[num+c])

    # print("\n",neighbor_word[:3])
    # print("\nlength: ",len(neighbor_word))
    return neighbor_word