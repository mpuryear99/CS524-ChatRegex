# Core methods for structuring prompt responses
import re
from typing import Iterable
from analyze_books import get_surrounding_words


PROMPT_THRESH = 10

def output_missing_instance_warning():
    print("Please note that some instances may have been missed.")
    print("This is due to a lack of context knowledge often needed to disambiguate names.")


def output_name_cooccurrence(book: dict,
                            name1: str, locs1: Iterable[tuple[int, int]],
                            name2: str, locs2: Iterable[tuple[int, int]]):
    """ Handle the response for two character co-occurrences given index of matches.
        Co-occurrences are found at the sentence and chapter scope.
    """
    # Process sentence scope
    st_locs_dict = {}
    for ch, st in sorted(set(locs1).intersection(locs2)):
        st_locs_dict.setdefault(ch+1, []).append(st)

    # Process chapter scope
    ch_locs = set(k[0]+1 for k in locs1)
    ch_locs.intersection_update(k[0]+1 for k in locs2)
    ch_locs = sorted(ch_locs)

    ### Print results

    # Chapter scope
    if not len(ch_locs):
        print(f"{name1} and {name2} do not co-occur in any chapters of the book.")
        return
    if len(ch_locs) > 1:
        chs = f"s {', '.join(str(x) for x in ch_locs[:-1])}, and {ch_locs[-1]}"
    else:
        chs = f" {ch_locs[0]}"
    print(f"{name1} and {name2} can both be found in chapter{chs}.")

    # Sentence scope
    if len(st_locs_dict):
        print("They can also be found together in the same sentence.")
    else:
        print("However, they do not appear to share any sentences.")
    for ch, sts in st_locs_dict.items():
        if len(sts) > 1:
            sts_str = f"s {', '.join(str(x) for x in sts[:-1])}, and {sts[-1]}"
        else:
            sts_str = f" {sts[0]}"
        print(f"  In chapter {ch}, they co-occur in sentence{sts_str}.")
        for st in sts:
            print(f"  {st:>3}:  {book['content'][ch-1][st]}")



def output_nearby_words(content: list[list[str]],
                        name:    str,
                        matches: Iterable[tuple[tuple[int, int], re.Match]],
                        prompt_thresh: int = PROMPT_THRESH):
    """ Output words surrounding matches in sets of `prompt_thresh`. """

    print(f"{name} was identified a total of {len(matches)} times in various forms.")

    if prompt_thresh < 2:
        prompt_thresh = len(matches)
        print("All instances are shown below:")
    else:
        print(f"The first {prompt_thresh} instances are shown below with surrounding words:")

    next_thresh = prompt_thresh

    for i, (loc, match) in enumerate(matches):
        if i == next_thresh:
            print("", end="", flush=True)
            next_thresh = min(i + prompt_thresh, len(matches))
            m_rem = len(matches)-i
            sx = input(f"Show {next_thresh-i} more ({m_rem} left)?  (Y/n)>  ") + ' '
            if (not sx.isspace()) and ('n' in sx.lower()):  # blank == yes
                break
        prev_words, next_words = get_surrounding_words(content, match, loc)
        prev_words = ' '.join(prev_words)
        next_words = ' '.join(next_words)
        ch_num, st_num = loc[0]+1, loc[1]
        print(f"  Chapter {ch_num:>2}, Sentence {st_num:>3}: ",
              prev_words, "~", match.group(), "~", next_words)


def output_first_match(name: str,
                       matches: Iterable[tuple[tuple[int, int], re.Match]],
                       print_match: bool | None = None):
    """
    Output the location (chapter, sentence) of first match.

    Params:
        name : str
            Title associated with the set of matches.
            Used to start each sentence response.
        matches : Iterable[tuple[tuple[int, int], re.Match]]
            Iterable of (loc, re.Match) tuples from which the first match is found.
        print_match : bool | None
            If True, print the term actually matched.
            If None, print the matched term if it is different from `name`.
    """

    loc, match = min(matches, key=lambda kv: kv[0])
    ch_idx, st_idx = loc[0]+1, loc[1]
    print(f"{name} is first introduced in sentence {st_idx} of chapter {ch_idx}.")

    if print_match or (print_match is None and match.group() != name):
        print(f"{name} is introduced as '{match.group()}' in the sentence.")
    
    return loc