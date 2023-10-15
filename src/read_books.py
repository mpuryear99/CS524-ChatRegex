# Methods for reading and tokenizing book text files.
import re


# _re_quotes = re.compile(r"\"|'(?!\S)|(?<!\S)'")
_re_quotes = re.compile(r"[\"']")
_re_puncts = re.compile(r'(?<![MDF]r|Ms|St)(?<!Mrs)(?<![A-Z])\.|[,?!:;]')
_re_sentence_delim = re.compile(r"""
    (?:(?<=\S[.?!])|(?<=\S[.?!]["']))
    (?<!Mrs\.)(?<![MDF]r\.|Ms\.|St\.)(?<![A-Z]\.)  \s  (?=[A-Z])
""", re.VERBOSE)

def split_sentences(pg: str):
    ss = _re_sentence_delim.split(pg)
    ss = [_re_quotes.sub('', s) for s in ss]    # remove quotes around text (and after plural possessives)
    ss = [_re_puncts.sub('', s) for s in ss]    # remove punctuation
    return ss


def read_book(filename: str):
    """ Read in a book file and tokenize text as chapters of sentences.

    Returns: Tuple[header, chapters]
        header:   List of header lines
        chapters: 2D List of [chapters][sentences] (first sentence is chapter header)
    """
    header = []
    chapters = []

    with open(filename, 'rt', encoding='utf-8') as fin:
        # read the header
        while not (line := next(fin)).isspace():
            header.append(line)

        # split the book into chapters of paragraph lines
        for c in re.split(r"(?:\n[^\S\r\n]*){4,}", fin.read()):
            chap = [p for p in re.split(r"(?:\n[^\S\r\n]*){2,3}", c) if len(p) and not p.isspace()]
            chapters.append(chap)

    # Combine the paragraph lines. Then, split into sentences
    re_garbage = re.compile(r'[\[\]{}()]')
    re_dashes  = re.compile(r'(?<![^\s-])-|-(?![^\s-])')
    re_subsp   = re.compile(r'[—_\r\n\s]+')
    re_dquotes = re.compile(r"[“”]")
    re_squotes = re.compile("[‘’]")
    for i,c in enumerate(chapters):
        for j,p in enumerate(c):
            p = re_garbage.sub('',  p)
            p = re_dashes .sub(' ', p)
            p = re_subsp  .sub(' ', p)
            p = re_dquotes.sub('"', p)
            p = re_squotes.sub("'", p)
            chapters[i][j] = split_sentences(p) if (j > 0) else [p]

    # flatten chapter paragraphs to sentences
    chapters = [[st for pg in ch for st in pg] for ch in chapters]

    return header, chapters


def iter_book_content(content: list[list[str]]):
    """ Return generator for book content 3D list.
        First sentence is skipped to ignore header.

    Yields: Tuple[index, sencence]
        index: Tuple[i_chapter, i_sentence]
        sentence: str
    """
    for ch_idx, ch in enumerate(content):
        st_iter = iter(ch)
        ch_title = next(st_iter)
        for st_idx, st in enumerate(st_iter, 1):
            yield ((ch_idx, st_idx), st)
