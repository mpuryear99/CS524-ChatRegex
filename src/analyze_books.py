import os
import re
from read_books import read_book, iter_book_content

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.abspath(os.path.join(FILE_DIR, '..', 'books'))


### The Murder on the Links
BOOK_AC_THE_MURDER_ON_THE_LINKS = {
    'Title':    'The Murder on the Links',
    'Author':   'Agatha Christie',

    'filepath': (fn := os.path.join(BOOKS_DIR, 'Agatha_Christie-The_Murder_on_the_Links.txt')),
    'content':  read_book(fn)[1],

    'detectives': {
        'Hercule Poirot':       r"(?:Mr\.)? (?:Hercule (?:\sPoirot)? | Poirot)",
        'Arthur Hastings':      r"(?:Captain\s)? (?:Arthur\s)? Hastings",
        'Monsieur Giraud':      r"(?:M\.\s|Monsieur\s)? Giraud",
        'Monsieur Hautet':      r"(?:M\.\s|Monsieur\s)? Hautet",
        'Japp':                 r"Japp",    # Only there 6 times...
    },
    'suspects': {
        "Madame Daubreuil (Jeanne Beroldy)": r"""
            (?:Madame\s|Mademoiselle\s) Daubreuil |
            (?:Madame\s|Mademoiselle\s)? (?:Jeanne (?:\sBeroldy)? | Beroldy)
        """,
        "Eloise Renauld":       r"Eloise (?:\sRenauld)?",
        "Jack Renauld":         r"Jack   (?:\sRenauld)?",
      # "Monsieur Lucien Bex":  r"(?:M\.\s)? (?:Lucien\s) Bex",
      # "Dulcie Duveen":        r"Dulcie (?:\sDuveen)? | Cinderella",
    },
    'perpetrators': {
        'Marthe Daubreuil':     r"Marthe (?:\sDaubreuil)?",
    },
    'victims': {
        "Paul Renauld":         r"Paul (?:\sRenauld)?",
    },
    'crime': r"grave | golf (?:\scourse)? | stabbed",
}


### The Mysterious Affair at Styles
BOOK_AC_THE_MYSTERIOUS_AFFAIR_AT_STYLES = {
    'Title':    'The Mysterious Affair at Styles',
    'Author':   'Agatha Christie',

    'filepath': (fn := os.path.join(BOOKS_DIR, 'Agatha_Christie-The_Mysterious_Affair_at_Styles.txt')),
    'content':  read_book(fn)[1],

    'detectives': {
        'Hercule Poirot':       r"(?:Mr\.)? (?:Hercule (?:\sPoirot)? | Poirot)",
        'Arthur Hastings':      r"(?:Captain\s)? (?:Arthur\s)? Hastings",
        'Japp':                 r"Japp",
    },
    'suspects': {
        'John Cavendish':       r"John (?:\sCavendish)?",
        'Mary Cavendish':       r"Mary (?:\sCavendish)?",
        'Lawrence Cavendish':   r"Lawrence (?:\sCavendish)?",
        'Cynthia Murdoch':      r"Cynthia (?:\sMurdoch)?",
        'Dr. Baurenstein':      r"(?:Dr\.\s)? Bauerstein",
    },
    'perpetrators': {
        'Alfred Inglethorp':    r"Alfred (?:\sInglethorp)?",
        'Evelyn Howard':        r"Evelyn (?:\sHoward)?",
    },
    'victims': {
        'Emily Inglethorp':     r"Emily (?:\sInglethorp)?",
    },
    'crime': r"strychnine | poison",
}


### The Hound of the Baskervilles
BOOK_CD_THE_HOUND_OF_THE_BASKERVILLES = {
    'Title':    'The Hound of the Baskervilles',
    'Author':   'Conan Doyle',

    'filepath': (fn := os.path.join(BOOKS_DIR, 'Conan_Doyle-The_Hound_of_the_Baskervilles.txt')),
    'content':  read_book(fn)[1],

    'detectives': {
        'Sherlock Holmes':      r"Sherlock (?:\sHolmes)? | Holmes",
        'Dr. John Watson':      r"(?:Dr\.\s) (?:John (?:\sWatson)? | Watson)",
    },
    'suspects': {
        'Henry Baskerville':    r"(?:Sir\s)? Henry (?:\sBaskerville)?",
        'James Mortimer':       r"(?:Dr\.\s)? (?:James (?:\sMortimer)? | Mortimer)",
        'Laura Lyons':          r"Laura (?:\sLyons)? | Lyons",
        'Beryl Stapleton':      r"(?:Miss\s|Mrs\.\s) Stapleton | Beryl (?:\sGarcia)",        # Tip: No 'Beryl Stapleton' in book
        'The Barrymores':       r"(?:Mr\.\s|Mrs\.\s)? Barrymores?"
    },
    'perpetrators': {
        'Jack Stapleton':       r"Jack (?:\sStapleton)? | (?<!Miss\s|Mrs\.\s) Stapleton",
    },
    'victims': {
        'Charles Baskerville':  r"(?:Sir\s)? Charles (?:\sBaskerville)?",
    },
    'crime': r"heart | cardiac | exhaustion | fatal",
}


BOOKS = [
    BOOK_AC_THE_MURDER_ON_THE_LINKS,
    BOOK_AC_THE_MYSTERIOUS_AFFAIR_AT_STYLES,
    BOOK_CD_THE_HOUND_OF_THE_BASKERVILLES,
]



# GENERIC_PATTERNS = {
#     'detective':    r"detective|investigator|inspector",
#     'perpetrator':  r"perpetrator|killer|criminal|murderer|culprit|evildoer|offender|villian",
#     'victim':       r"victim|casualty",
#     'crime':        r"crime|kill|murder|dead|offense|misdeed",
#     'suspect':      r"suspect|accused|defendant",
# }



# Prompts:
# 1) When does the investigator (or a pair) occur for the first time?
# 2) When is the crime first mentioned? - the type of the crime and the details
# 3) When is the perpetrator first mentioned?
# 4) What are the three words that occur around the perpetrator on each mention?
#    (i.e., the three words preceding and the three words following the mention of a perpetrator)
# 5) When and how the detective/detectives and the perpetrators co-occur?
# 6) When are other suspects first introduced?
# Need:
#   Every Match: {detectives, perpetrators}
#   First Match: {crime, suspects, victims}


def find_first_book_match(content: list[list[str]], pattern: re.Pattern):
    for idxs, st in iter_book_content(content):
        if (match := pattern.search(st)) is not None:
            return (idxs, match)
    return None


def find_all_book_matches(content: list[list[str]], pattern: re.Pattern):
    results = {}
    for idxs, st in iter_book_content(content):
        if (match := pattern.search(st)) is not None:
            results[idxs] = match
    return results


def process_book(book: dict):
    results = {}

    for category in ('detectives', 'perpetrators'):
        matches = results[category] = {}
        for k, re_k in book[category].items():
            re_k = re.compile(rf"\b(?:{re_k})\b", re.I | re.X)
            matches[k] = find_all_book_matches(book['content'], re_k)

    for category in ('suspects', 'victims'):
        matches = results[category] = {}
        for k, re_k in book[category].items():
            re_k = re.compile(rf"\b(?:{re_k})\b", re.I | re.X)
            matches[k] = find_first_book_match(book['content'], re_k)

    re_crime = re.compile(rf"\b(?:{book['crime']})\b", re.I | re.X)
    results['crime'] = find_first_book_match(book['content'], re_crime)

    return results


def get_next_sentence(content: list[list[str]], ch_idx: int, st_idx):
    if (st_idx := st_idx+1) >= len(content[ch_idx]):
        st_idx = 1
        if (ch_idx := ch_idx+1) >= len(content):
            return None
    return (ch_idx, st_idx), content[ch_idx][st_idx]


def get_prev_sentence(content: list[list[str]], ch_idx: int, st_idx):
    if (st_idx := st_idx-1) < 1:
        if (ch_idx := ch_idx-1) < 0:
            return None
        st_idx = len(content[ch_idx])-1
    return (ch_idx, st_idx), content[ch_idx][st_idx]


def get_surrounding_words(content: list[list[str]],
                          match:   re.Match,
                          loc:     tuple[int, int],
                          n:       int = 3):
    # In this implementation, surrounding words must be in the same chapter
    ch_idx, st_idx = loc
    chap = content[ch_idx]

    prev_words = chap[st_idx][:match.span()[0]].rsplit(maxsplit=n)[:-n-1:-1]
    for i in range(st_idx-1, 0, -1):        # skip sentence 0
        if (maxsplit := n-len(prev_words)) <= 0:
            break
        prev_words.extend(chap[i].rsplit(maxsplit=maxsplit)[:-maxsplit-1:-1])
    prev_words = prev_words[n-1::-1]

    next_words = chap[st_idx][match.span()[1]+1:].split(maxsplit=n)
    for i in range(st_idx+1, len(chap)):
        if (maxsplit := n-len(next_words)) <= 0:
            break
        next_words.extend(chap[i].split(maxsplit=maxsplit))
    next_words = next_words[:n]

    return prev_words, next_words




### Perform book processing at module import

for book in BOOKS:
    book['matches'] = process_book(book)