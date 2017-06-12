def word_cloud(word_list, remove_list, title):

    for item in remove_list:
        try:
            while item in word_list:
                word_list.remove(item)
        except ValueError:
            pass  # in case it does not contain such word to be removed
    text = " ".join(word_list)

    from wordcloud import WordCloud
    wordcloud = WordCloud(background_color='white', max_font_size=50, mask=None).generate(text)
    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear', cmap=None)
    plt.title(title)
    plt.axis("off")
    plt.show()