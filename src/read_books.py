# Methods for reading and tokenizing book text files.
import re



def read_book(filename: str):
    """ Read in a book text file and tokenize paragraphs in chapters.

    Params:
        filename: string containing path to book file

    Returns:
        tuple(header, chapters)
            header: List of header lines
            chapters: 2D List of text as [chapter][paragraph]
    """
    header = []
    chapters = []

    with open(filename, 'rt') as fin:
        # read the header
        for line in fin:
            if line.isspace():
                break
            header.append(line)

        # split the book into chapters of paragraph lines
        for c in re.split(r"(?:\n[^\S\r\n]*){4,}", fin.read()):
            chap = [p for p in re.split(r"(?:\n[^\S\r\n]*){2,3}", c) if len(p) and not p.isspace()]
            chapters.append(chap)

    # combine the paragraph lines
    re_subsp = re.compile(r'\r?\n|\s+')
    for i,c in enumerate(chapters):
        for j,p in enumerate(c):
            chapters[i][j] = re_subsp.sub(' ', p)

    return header, chapters
