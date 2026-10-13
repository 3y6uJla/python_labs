import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.text import normalize, tokenize, count_freq, top_n

TOP_COUNT = 5


def main() -> None:
    text = sys.stdin.read()
    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, TOP_COUNT)

    print(f'Всего слов: {len(tokens)}')
    print(f'Уникальных слов: {len(freq)}')
    print(f'Топ-{TOP_COUNT}:')
    for word, count in top:
        print(f'{word}:{count}')


if __name__ == '__main__':
    main()