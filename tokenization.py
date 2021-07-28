import re
import six
import razdel


ACCENT = six.unichr(769)
WORD_TOKENIZATION_RULES = re.compile(r"""
[\w""" + ACCENT + """]+://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+
|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+
|[0-9]+-[а-яА-ЯіїІЇєЄґҐ'’`""" + ACCENT + """]+
|[+-]?[0-9](?:[0-9,.-]*[0-9])?
|[\w""" + ACCENT + """](?:[\w'’`-""" + ACCENT + """]?[\w""" + ACCENT + """]+)*
|[\w""" + ACCENT + """].(?:\[\w""" + ACCENT + """].)+[\w""" + ACCENT + """]?
|["#$%&*+,/:;<=>@^`~…\\(\\)⟨⟩{}\[\|\]‒–—―«»“”‘’'№]
|[.!?]+
|-+
""", re.X | re.U)


ABBRS = """
ім.
в.
о.
т.
п.
д.
под.
ін.
вул.
просп.
бул.
пров.
пл.
г.
р.
див.
п.
с.
м.
н.
е.
адмін.
к.
геогр.
обл.
смт.
авт.
адм.
акад.
англ.
арк.
арт.
археол.
арх.
архіт.
асист.
асоц.
б.
буд.
бух.
бюдж.
вет.
вид.
викл.
відкр.
дип.
діагр.
екол.
екон.
євр.
журн.
зобр.
іл.
інв.
інд.
інж.
іст.
каф.
кл.
коеф.
лаб.
лінгв.
літ.
мат.
мед.
мех.
міс.
муз.
нар.
наук.
нац.
орг.
офіц.
пед.
пр.
проф.
публ.
рис.
мал.
pp.
рос.
св.
сл.
ст.
студ.
табл.
тис.
укр.
упр.
фіз.
фін.
ц.
""".strip().split()


def tokenize_sents(string):
    string = six.text_type(string)
    spans = []
    for match in re.finditer('[^\s]+', string):
        spans.append(match)
    spans_count = len(spans)

    rez = []
    off = 0

    for i in range(spans_count):
        tok = string[spans[i].start():spans[i].end()]
        if i == spans_count - 1:
            rez.append(string[off:spans[i].end()])
        elif tok[-1] in ['.', '!', '?', '…', '»', "'", "\""]:
            # tok1 = tok[re.search('[.!?…»]', tok).start() - 1]
            next_tok = string[spans[i + 1].start():spans[i + 1].end()]
            if (next_tok[0].isupper() or next_tok[0] in ["'", "\"", "«"]) \
                    and not ((len(tok) == 2 and tok[0].isupper()) \
                             or tok[0] == '('
                             or tok in ABBRS):
                rez.append(string[off:spans[i].end()])
                off = spans[i + 1].start()

    return rez


def text_to_sent(text, lang):
    rez = []
    if lang == 'uk':
        for part in text.split('\n'):
            rez += tokenize_sents(part)
    elif lang=='ru':
        for part in text.split('\n'):
            rez += [s.text for s in razdel.sentenize(part)]
    return rez


def sent_to_words(text, lang):
    if lang == 'uk':
        return re.findall(WORD_TOKENIZATION_RULES, text)
    elif lang == 'ru':
        return [tkn.text for tkn in razdel.tokenize(text)]
    return None


def tokenize(text, lang):
    res = []
    for sent in text_to_sent(text, lang):
        tokens = []
        for word in sent_to_words(sent, lang):
            tokens.append(word)
        res.append(tokens)
    return res


def tokenize_to_sent_str(text, lang):
    res = []
    for sent in text_to_sent(text, lang):
        res.append(sent_to_words_str(sent, lang))
    return res