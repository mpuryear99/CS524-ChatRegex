import re
import sys
import itertools
from typing import Iterable

from analyze_books import BOOKS
import prompt_response_core as resp_core



def print_category_person_count(label: str, count: int):
    print(f"The '{label}' classification identifies {count}",
          "person." if (count == 1) else "people.")


# Prompts:
# 1) When does the investigator (or a pair) occur for the first time?
# 2) When is the crime first mentioned? - the type of the crime and the details
# 3) When is the perpetrator first mentioned?
# 4) What are the three words that occur around the perpetrator on each mention?
#    (i.e., the three words preceding and the three words following the mention of a perpetrator)
# 5) When and how the detective/detectives and the perpetrators co-occur?
# 6) When are other suspects first introduced?
#
# Generalized:
# 1) When does _____ occur for the first time?       1,2,3,6
#    - NAME         1       *
#    - CATEGORY             *
#      - NAMES      N       *
#      - CRIME      1       *
# 2) What are the three words that occur around ____ on each mention?
#    - NAME         1       *
#    - CATEGORY             *       perpetrator     4
#      - NAMES      N       *
#      - CRIME      1
#    - This could also be used to print all occurrences if asked, though not required
# 3) When and how ____ and ____ co-occur?            5
#    - NAME(S)              *
#    - CATEGORY(S)          *
#      - NAMES      N       *
#      - CRIME      1
#    - Don't print overlap (or at least ask first...)


## Generalized Response 1: First Match

def resp_name_first_match(name: str,
                          matches: Iterable[tuple[tuple[int, int], re.Match]]):
    resp_core.output_first_match(name, matches)


def resp_category_first_match(book: dict,
                              category: str):
    if 'crime' in category:
        name = 'The crime'
        matches = book['matches']['crime'].items()
        resp_core.output_first_match(name, matches)

    else:
        # Category /w names
        cat_matches = book['matches'][category]
        print_category_person_count(category, len(cat_matches))

        for name, matches in cat_matches.items():
            matches = matches.items()
            resp_core.output_first_match(name, matches)


## Generalized Response 2: Nearby Words

def resp_name_nearby_words(book: str,
                           name: str,
                           matches: Iterable[tuple[tuple[int, int], re.Match]]):
    resp_core.output_nearby_words(
        content=book['content'], name=name, matches=matches, n=3)


def resp_category_nearby_words(book: str,
                               category: str):
    content = book['content']

    if 'crime' in category:
        name = 'The crime'
        matches = book['matches']['crime'].items()
        resp_core.output_nearby_words(
            content, name=name, matches=matches, n=3)

    else:
        # Category /w names
        cat_matches = book['matches'][category]
        print_category_person_count(category, len(cat_matches))

        for name, matches in cat_matches.items():
            matches = matches.items()
            resp_core.output_nearby_words(
                content, name=name, matches=matches, n=3)


## Generalized Response 3: co-occurence

def resp_co_occur(book: dict,
                  name1: str | None, category1: str,
                  name2: str | None, category2: str):
    """
    Handle responses for co-occurence given any combination of name/category.

    Params:
        book : dict
            Analyzed book dictionaty.
        name* : str | None
            If str, must be a key (name) in category.
            If None, loop through all names in category.
        category* : str
            The category name of the matches.
    """
    # safety first...
    if 'crime' in category1:  name1 = None
    if 'crime' in category2:  name2 = None

    # Keep the named person in name1
    if (name1 is None) and (name2 is not None):
        temp = name1, category1
        name1, category1 = name2, category2
        name2, category2 = temp

    cat_count_printed = False

    if 'crime' in category1:
        # crime category
        locs1 = book['matches']['crime'].keys()
        iter1 = (('The crime', locs1),)
    elif name1 is None:
        # category of names
        cat1_matches = book['matches'][category1]
        iter1 = ((k,v.keys()) for (k,v) in cat1_matches.items())
        print_category_person_count(category1, len(cat1_matches))
        cat_count_printed = True
    else:
        # name in category
        locs1 = book['matches'][category1][name1].keys()
        iter1 = ((name1, locs1),)


    if 'crime' in category2:
        # crime category
        locs2 = book['matches']['crime'].keys()
        iter2 = (('the crime', locs2),)
    elif name2 is None:
        # category of names
        cat2_matches = book['matches'][category2]
        iter2 = ((k,v.keys()) for (k,v) in cat2_matches.items())
        if category1 != category2 or not cat_count_printed:
            print_category_person_count(category2, len(cat2_matches))
            cat_count_printed = True
    else:
        # name in category
        locs2 = book['matches'][category2][name2].keys()
        iter2 = ((name2, locs2),)


    if cat_count_printed and (name1 is not None) and (category1 == category2):
        print(f"{name1} falls under of this classification.")

    add_sep = cat_count_printed
    for (p1, l1), (p2, l2) in itertools.product(iter1, iter2):
        # Don't print co-occurances of the same person
        if (p1 == p2) and (category1 == category2):
            continue
        if add_sep: print("---")
        add_sep = True
        resp_core.output_name_cooccurence(book=book, name1=p1, locs1=l1,
                                                     name2=p2, locs2=l2)






def prompt_select_book():
    """
    Create a prompt to select a book for analysys.

    Returns: dict
        Dictionary of selected book
    """
    re_books = [r'|'.join([w for w in b['Title'].split() if len(w)>3]) for b in BOOKS]
    re_books[0] = r'|'.join([re_books[0], r"1|one|first"])
    re_books[1] = r'|'.join([re_books[1], r"2|two|second"])
    re_books[2] = r'|'.join([re_books[2], r"3|three|third"])
    re_books = r'|'.join(fr"({b})" for b in re_books)
    re_books = re.compile(fr"\b(?:{re_books})\b", re.I|re.X)

    print("Here are the books we have on file:")
    for i, book in enumerate(BOOKS, 1):
        print(f" {i}) {book['Title']:<31}  -  {book['Author']}")
    print()

    book = None
    while book is None:
        print("Which book would you like to analyze?   ('q' to quit)", flush=True)
        if (prompt_in := input("> ").strip()) == 'q':
            sys.exit()

        matches = [*re_books.finditer(prompt_in)]
        for i in range(len(BOOKS)):
            if any((m.group(i+1) is not None) for m in matches):
                if book is not None:
                    break
                book = BOOKS[i]

        if book is None:
            print("Sorry, I'm not sure which book you are referring to.",
                  "Let's try that again!")

    print(f"Analyzing '{book['Title']}' by {book['Author']}. Great choice!")
    return book




RE_CATEGORY = {
    'detectives':   r"detective|investigator|inspector",
    'perpetrators': r"perpetrator|killer|criminal|murderer|culprit|evildoer|offender|villian",
    'victims':      r"victim|casualty",
    'suspects':     r"suspect|criminal",
    'crime':        r"crime|kill|murder|dead|offense|misdeed",
}




def pro_get_name_matches(book: dict, prompt_in: str):

    name_results = {}
    for cat, re_cat in RE_CATEGORY.items():
        if 'crime' in cat:
            continue
        for name, re_name in book[cat].items():
            re_name = rf"\b(?:(?:{re_cat})\s)?(?:{re_name})\b"
            match = re.search(re_name, prompt_in, re.I|re.X)

            if match is not None:
                name_results.setdefault(cat, {})[name] = match

    return name_results


def prompt_qa(book: dict, prompt_in: str):
    """
    The heart of the beast.
    """

    # replace unknown/unused characters with spaces
    prompt_in = re.sub(r'[^-\w]+', ' ', prompt_in)

    # Determine question type (what/when/how)
    # q_who    = bool(re.search(r"who\s(?:is|are)", prompt_in, re.I))
    q_first    = bool(re.search(r"first|introduced", prompt_in, re.I))
    q_co_occur = bool(re.search(r"co-occur|together", prompt_in, re.I))
    q_around   = bool(re.search(r"words|around|near(?:by)?|surround", prompt_in, re.I))

    cat_results = set()
    for cat, re_cat in RE_CATEGORY.items():
        re_cat = rf"\b(?:(?:{re_cat})s?)\b"
        if re.search(re_cat, prompt_in, re.I|re.X) is not None:
                cat_results.add(cat)

    name_results = pro_get_name_matches(book, prompt_in)
    name_results = [(c,n) for (c,nn) in name_results.items() for n in nn.keys()]

    total_results = len(name_results) + len(cat_results)

    if sum([q_first, q_co_occur, q_co_occur]) != 1 or total_results == 0:
        print("Sorry, but I'm not sure how to answer that.")
        print("Maybe try rephrasing the question.")


    if (q_first):
        if len(name_results) > 1 or len(cat_results) > 1:
            print("That's a lot to answer... ",
                  "One name/category at a time for first occurance questions please.")
        elif len(name_results):
            cat, name = next(iter(name_results))
            matches = book['matches'][cat][name].items()
            resp_name_first_match(name, matches)
        else:
            cat = cat_results.pop()
            resp_category_first_match(book, cat)

    elif (q_around):
        if len(name_results) > 1 or len(cat_results) > 1:
            print("That's a lot to answer... ",
                  "One name/category at a time for surrounding word questions please.")
        elif len(name_results):
            cat, name = next(iter(name_results))
            matches = book['matches'][cat][name].items()
            resp_name_nearby_words(book, name, matches)
        else:
            cat = cat_results.pop()
            resp_category_nearby_words(book, cat)

    elif (q_co_occur):
        if len(name_results) > 2 or len(cat_results) > 2 or total_results < 2:
            print("I'm not sure how to answer that... ",
                  "Two names/categories at a time for co-occurence questions please.")
        elif len(name_results) == 2:
            it = iter(name_results)
            cat1, name1 = next(it)
            cat2, name2 = next(it)
            resp_co_occur(book, name1=name1, category1=cat1,
                                name2=name2, category2=cat2)
        elif len(name_results) == 1:
            cat1, name1 = next(iter(name_results))
            cat2, name2 = cat_results.pop(), None
            while (cat2 == cat1) and len(cat_results):
                cat2 = cat_results.pop()
            resp_co_occur(book, name1=name1, category1=cat1,
                                name2=name2, category2=cat2)
        else:
            cat1, name1 = cat_results.pop(), None
            cat2, name2 = cat_results.pop(), None
            resp_co_occur(book, name1=name1, category1=cat1,
                                name2=name2, category2=cat2)





def main():
    print("\nWelcome to ChatRegex for Detective Novels!")
    print("I'm here to help you analyze your favorite novels.", end="\n\n")

    # Select a book to analyze
    book = prompt_select_book()

    print("\nYou may now ask a question!  ('q' to quit)", end="\n\n")
    while (prompt_in := input("> ").strip()) != 'q':
        prompt_qa(book, prompt_in)
        print("\nIs there anything else I can help with?  ('q' to quit)", end="\n\n")

    return


if __name__ == "__main__":
    main()