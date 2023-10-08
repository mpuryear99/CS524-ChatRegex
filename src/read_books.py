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


def analyze_book(content: list, book_no: int):
    detective_pattern = r'(investigator|detective|inspector)'
    perpetrator_pattern = r'(perpetrator|killer|criminal|murderer|culprit|evildoer|offender|villian)'
    victim_pattern = r'(victim|casualty)'
    crime_pattern = r'(crime|(murder[^a-z])|dead|offense|misdeed)'
    suspect_pattern = r'(suspect|accused|defendant)'

    total_chapters = len(content)

    if(book_no == 1):
        # Key words for The Murder on the Links
        print("----------Analysis for The Murder on the Links----------")
        book_mysterious_detective_pattern = rf'({detective_pattern}|(Hercule(\sPoirot)?)|Poirot|Captain|Arthur|Hastings|(Arthur(\sHastings)?)|Japp|(Chief(\sInspector)?))'
        book_mysterious_perpetrator_pattern = rf'({perpetrator_pattern}|(Eloise(\sRenauld)?))'
        book_mysterious_victim_pattern = rf'({victim_pattern}|(Paul(\sRenauld)?))'
        book_mysterious_crime_pattern = rf'({crime_pattern}|grave|(golf(\scourse)?)|stabbed)'
        book_mysterious_suspect_pattern = rf'({suspect_pattern}|((Madame\s)?Virginie(\sRenauld)?)|(Jack(\sRenauld)?)|(Marthe(\sDaubreuil)?)|Daubreuil|(Monsieur(\sBex)?)|Bex|((Mademoiselle\s)?Dulcie(\sDuveen)?)|Duveen|Cinderella)'
    
    elif(book_no == 2):
        # Key words for The Mysterious Affair at Styles
        print("----------Analysis for The Mysterious Affair at Styles----------")
        book_mysterious_detective_pattern = rf'({detective_pattern}|(Hercule(\sPoirot)?)|Poirot|Captain|Arthur|Hastings|(Arthur(\sHastings)?)|Japp|(Chief(\sInspector)?))'
        book_mysterious_perpetrator_pattern = rf'({perpetrator_pattern}|(Alfred(\sInglethorp)?)|Inglethorp|Evelyn|Howard|(Evelyn(\sHoward)?))'
        book_mysterious_victim_pattern = rf'({victim_pattern}|(Emily(\sInglethorp)?)|Inglethorp|widow)'
        book_mysterious_crime_pattern = rf'({crime_pattern}|strychnine|poison)'
        book_mysterious_suspect_pattern = rf'({suspect_pattern}|(John(\sCavendish)?)|Cavendish|(Mary(\sCavendish)?)|(Lawrence(\sCavendish)?)|(Cynthia(\sMurdoch)?)|Murdoch|(Dr\.(\sBauerstein)?)|Bauerstein)'
        total_chapters -= 1

    elif(book_no == 3):
        # Key words for The Hound of the Baskervilles
        print("----------Analysis for The Hound of the Baskervilles----------")
        book_mysterious_detective_pattern = rf'({detective_pattern}|(Sherlock(\sHolmes)?)|Holmes|(John(\sWatson)?)|Watson)'
        book_mysterious_perpetrator_pattern = rf'({perpetrator_pattern}|(Jack(\sStapleton)?)|Stapleton)'
        book_mysterious_victim_pattern = rf'({victim_pattern}|((Sir\s)?Charles(\sBaskerville)?))'
        book_mysterious_crime_pattern = rf'({crime_pattern}|heart\sattack|hound)'
        book_mysterious_suspect_pattern = rf'({suspect_pattern}|((Sir\s)?Henry(\sBaskerville)?)|(James(\sMortimer)?)|Mortimer|(Laura(\sLyons)?)|Lyons|(Rodger(\sBaskerville)?(\sFrankland)?)|Frankland)'

    detective_match = {}
    perpetrator_match = {}
    perpetrator_paragraph_match = {}
    victim_match = {}
    crime_match = {}
    suspect_match = {}
    detective_perpetrator_match = {}
    detective_perpetrator_paragraph_match = {}

    total_sentence_count = 0
    for i,c in enumerate(content):
        sentence_count = 0
        for j,p in enumerate(c):
            if(i == 0 and j == 0):
                continue

            # Search for keywords for each sentence - WIP issues with mr, mrs, dr, st and quotes
            sentences = re.split(r'(?:")?[\.!?:](?:,?")?\s?[^a-z]', content[i][j], flags=re.IGNORECASE)

            # Wider search with paragraphs for prompts 4 and 5
            perpetrator_search_paragraph = re.search(rf'((\w+\s)(\w+\s)(\w+\s){book_mysterious_perpetrator_pattern}(\s\w+)(\s\w+)(\s\w+))', content[i][j], flags=re.IGNORECASE)
            detective_perpetrator_search_paragraph = re.search(rf'({book_mysterious_detective_pattern}.*{book_mysterious_perpetrator_pattern})|({book_mysterious_perpetrator_pattern}.*{book_mysterious_detective_pattern})', content[i][j], flags=re.IGNORECASE)

            detective_perpetrator_paragraph_match = add_match(detective_perpetrator_paragraph_match, detective_perpetrator_search_paragraph, i+1, j+1)
            perpetrator_paragraph_match = add_match(perpetrator_paragraph_match, perpetrator_search_paragraph, i+1, j+1)

            for sentence in sentences:
                if (sentence):
                    sentence_count += 1
                    detective_search = re.search(rf'(\b{book_mysterious_detective_pattern}\b)', sentence, flags=re.IGNORECASE)
                    perpetrator_search = re.search(rf'((\w+\s)?(\w+\s)?(\w+\s)?\b{book_mysterious_perpetrator_pattern}\b(\s\w+)?(\s\w+)?(\s\w+)?)', sentence, flags=re.IGNORECASE)
                    victim_search = re.search(rf'(\b{book_mysterious_victim_pattern}\b)', sentence, flags=re.IGNORECASE)
                    crime_search = re.search(rf'(\b{book_mysterious_crime_pattern}\b)', sentence, flags=re.IGNORECASE)
                    suspect_search = re.search(rf'(\b{book_mysterious_suspect_pattern}\b)', sentence, flags=re.IGNORECASE)
                    detective_perpetrator_search = re.search(rf'({book_mysterious_detective_pattern}.*{book_mysterious_perpetrator_pattern})|({book_mysterious_perpetrator_pattern}.*{book_mysterious_detective_pattern})', sentence, flags=re.IGNORECASE)

                    # Stores matches in dictionary with key = chapter and value = sentence/paragraph_number, match_words
                    detective_match = add_match(detective_match, detective_search, i+1, sentence_count)
                    perpetrator_match = add_match(perpetrator_match, perpetrator_search, i+1, sentence_count)
                    victim_match = add_match(victim_match, victim_search, i+1, sentence_count)
                    crime_match = add_match(crime_match, crime_search, i+1, sentence_count)
                    suspect_match = add_match(suspect_match, suspect_search, i+1, sentence_count)
                    detective_perpetrator_match = add_match(detective_perpetrator_match, detective_perpetrator_search, i+1, sentence_count)

        total_sentence_count += sentence_count

    print("total sentences:", total_sentence_count)
    print("total chapters:", total_chapters, "\n")
    print_summary(detective_match, "detective", "sentence")
    print_summary(perpetrator_match, "perpetrator", "sentence") # WIP Did not find great match within same sentence
    print_summary(victim_match, "victim", "sentence")
    print_summary(crime_match, "crime", "sentence")
    print_summary(suspect_match, "suspect", "sentence")
    print_summary(detective_perpetrator_match, "detective and perpetrator", "sentence") # WIP Did not find great match within same sentence

    # Prints analysis from paragraphs rather than sentences
    # We would need to determine sentence # when searching via paragraphs
    # Prompt 5 - print 'how' they co-occur
    print_summary(detective_perpetrator_paragraph_match, "detective and perpetrator paragraph", "paragraph")
    print_summary(perpetrator_paragraph_match, "perpetrator paragraph", "paragraph") # Possibly combine paragraphs - all 3 words are not captured


def add_match(matches, match, chapter_no, sentence_no):
    if (match):
        matches.setdefault(chapter_no, []).append([sentence_no, match.group(0)])

    return matches


def print_summary(matches: dict, search: str, location_type: str):
    chapter_no = next(iter(matches))
    location_no = matches[chapter_no][0][0]
    match_words = matches[chapter_no][0][1]

    total_matches = 0
    for chapter in matches:
        total_matches += len(matches[chapter])

    print(search, "first mentioned: chapter", chapter_no, location_type, location_no, "match", match_words)
    print(search, "mentioned total:", total_matches, "\n")


if __name__ == "__main__":

    # Update to your book path
    filename1 = ''
    filename2 = ''
    filename3 = ''

    header, book1 = read_book(filename1)
    header, book2 = read_book(filename2)
    header, book3 = read_book(filename3)

    analyze_book(book1, 1)
    analyze_book(book2, 2)
    analyze_book(book3, 3)
