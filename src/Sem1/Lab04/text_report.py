import sys
#from ...lib.text import *
#from .io_txt_csv import read_text, write_csv

if __name__ == "__main__":

    sys.path.append("./src")
    sys.path.append("./src/Sem1/Lab04")
    from io_txt_csv import read_text, write_csv
    from lib.text import *

    path = "./data/Lab04/input.txt"
    text = read_text(path)
    normalized = normalize(text)
    tokens = tokenize(normalized)
    counted = count_freq(tokens)

    header = ("word", "count")
    rows = [[word, count] for word, count in counted.items()]
    write_csv(rows, "./data/report.csv", header)

    total_words = len(tokens)
    unique_words = len(set(tokens))
    freq = count_freq(tokens)
    top_words = top_n(freq, 5)

    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5 слов:")
    for word, count in top_words:
        print(f"{word}: {count}")