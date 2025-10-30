from lib.text import normalize, tokenize, count_freq, top_n

text = input("Введите текст: ")

normalized_text = normalize(text)
tokens = tokenize(normalized_text)

total_words = len(tokens)
unique_words = len(set(tokens))
freq = count_freq(tokens)
top_words = top_n(freq, 5)

print(f"Всего слов: {total_words}")
print(f"Уникальных слов: {unique_words}")
print("Топ-5 слов:")
for word, count in top_words:
    print(f"{word}: {count}")