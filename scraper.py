import re
import random
from lxml.html import parse, tostring
from functools import partial

PROPER_NAME_RE = re.compile(r'[A-Z][a-z]+(?: [A-Z][a-z]+)+')
DAILY_MAIL_FRONTPAGE = 'http://www.dailymail.co.uk/home/latest/index.html'


def get_doc():
    doc = parse('mail-full.html')
    #doc.getroot().make_links_absolute(DAILY_MAIL_FRONTPAGE)
    return doc


def get_headline_elements(doc):
    SEL = '.link-bogr2 strong'
    return doc.getroot().cssselect(SEL)


def get_headlines(doc):
    return [el.text.strip() for el in get_headline_elements(doc)]


def modify_doc(doc, headline_gen):
    for el in get_headline_elements(doc):
        el.text = headline_gen()


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

    doc = get_doc()
    headlines = list(get_headlines(doc))
    topics = list(get_people(headlines))

    headline_gen = partial(build_headlines, headlines, topics)
    modify_doc(doc, headline_gen)

    s = tostring(doc)
    with open('./mail.html', 'w') as f:
	f.write(s)

