import re
import random
from lxml.html import parse


PROPER_NAME_RE = re.compile(r'[A-Z][a-z]+(?: [A-Z][a-z]+)+')


def get_headlines():
    doc = parse('http://www.dailymail.co.uk/home/latest/index.html')
    SEL = '.link-bogr2 strong'
    return [el.text.strip() for el in doc.getroot().cssselect(SEL)]


def get_people(headlines):
    seen = set()
    for t in headlines:
        for name in PROPER_NAME_RE.findall(t):
            if name not in seen:
                yield name
                seen.add(name)


def build_headlines(headlines, topics):
    while True:
        h = random.choice(headlines)
        names = len(PROPER_NAME_RE.findall(h))
        if names > 1:
            break
    chosen_names = random.sample(topics, names)
    template = PROPER_NAME_RE.sub('%s', h.replace('%', '%%'))

    return template % tuple(chosen_names)


if __name__ == '__main__':
    headlines = list(get_headlines())
    topics = list(get_people(headlines))

    print build_headlines(headlines, topics)
