import re

from analyze_books import BOOKS


# Chat functions respond to user based on specific prompt
def chat_response_1():
    print("\nfirst prompt")
    print("The first time the investigator(s) are introduced in the novel occurs on chapter ___, sentence ___")

def chat_response_2():
    print("\nsecond prompt")
    print("The crime is first revealed to the readers on chapter ___, sentence ___")

def chat_response_3():
    print("\nthird prompt")
    print("The novel first mentions the perpetrator on chapter ___, sentence ___")

def chat_response_4():
    print("\nforth prompt")
    print("The first three words prior to mentioning the perpetrator are _____")
    print("The last three words after mentioning the perpetrator are _____")

def chat_response_5():
    print("\nfifth prompt")
    print("The investigator and perpetrator first meet in chapter ___, sentence ___")

def chat_response_6():
    print("\nsixth prompt")
    print("The other suspects are introducted on chapter ___, sentence ___")

def chat_response_unknown():
    print("\nWill you please rephrase the question?")

def prompt_determine_book(x: str):
    re_books = [r'|'.join([w for w in b['Title'].split() if len(w)>3]) for b in BOOKS]
    re_books[0] = r'|'.join([re_books[0], r"1|one|first"])
    re_books[1] = r'|'.join([re_books[1], r"2|two|second"])
    re_books[2] = r'|'.join([re_books[2], r"3|three|third"])
    re_books = r'|'.join(fr"({b})" for b in re_books)
    re_books = re.compile(fr"\b(?:{re_books})\b", re.I|re.X)

    matches = [*re_books.finditer(x)]
    possible_results = []
    for i in range(len(BOOKS)):
        if any((m.group(i+1) is not None) for m in matches): 
            possible_results.append(BOOKS[i])
    
    return possible_results

if __name__ == "__main__":
    BOOK_PATTERNS = {
        'book1':  r"murder|links|1|one|first",
        'book2':  r"mysterious|affair|styles|2|two|second",
        'book3':  r"hound|baskervilles|3|three|third",
    }

    books = BOOKS
    selected_book = -1

    print("Welcome to ChatRegex for Detective Novels!")
    print("\nWe are here to help you analyze your favorite novels.")
    print("Here are the books we have on file.\n")
    for i, book in enumerate(BOOKS, 1):
        print(f"{i}) {book['Title']} by {book['Author']}")
    print("\n What book are you interested in analyzing?")
    while True:
        print("> ", end='')
        try:
            prompt = input()
        except:
            exit()
        
        if prompt.lower() == "done":
            break

        print([x['Title'] for x in prompt_determine_book(prompt)])

        book_one = re.search(BOOK_PATTERNS['book1'], prompt, flags=re.IGNORECASE)
        book_two = re.search(BOOK_PATTERNS['book2'], prompt, flags=re.IGNORECASE)
        book_three = re.search(BOOK_PATTERNS['book3'], prompt, flags=re.IGNORECASE)

        if book_one:
            selected_book = 0
        elif book_two:
            selected_book = 1
        elif book_three:
            selected_book = 2
        else:
            print("I'm not sure what book you are refering to. Try giving the exact title of the book you are interested in.")
            continue

        print("\n", books[selected_book]['Title'], "- great choice!")
        break

    # Try to join with specific book
    GENERIC_PATTERNS = {
    'detective':    r"detective|investigator|inspector",
    'perpetrator':  r"perpetrator|killer|criminal|murderer|culprit|evildoer|offender|villian",
    'victim':       r"victim|casualty",
    'crime':        r"crime|kill|murder|dead|offense|misdeed",
    'suspect':      r"suspect|accused|defendant",
    }

    print("\n What would you like to know about your novel?")
    while True:
        print("> ", end='')
        try:
            prompt = input()
        except:
            exit()
        
        if prompt.lower() == "done":
            exit()

        # We might can use these to better refine the search later
        who = re.search(r'who', prompt, flags=re.IGNORECASE)
        what = re.search(r'what', prompt, flags=re.IGNORECASE)
        when = re.search(r'when', prompt, flags=re.IGNORECASE)
        where = re.search(r'where', prompt, flags=re.IGNORECASE)
        how = re.search(r'how', prompt, flags=re.IGNORECASE)

        # Determines which prompt the user refers to
        detective_search = re.search(rf'(?!(.*{GENERIC_PATTERNS["perpetrator"]})).*{GENERIC_PATTERNS["detective"]}(?!(.*{GENERIC_PATTERNS["perpetrator"]})).*(occur|show|first)?', prompt, flags=re.IGNORECASE)
        crime_search = re.search(rf'.*{GENERIC_PATTERNS["crime"]}.*(occur|show|first)?', prompt, flags=re.IGNORECASE)
        perpetrator_search = re.search(rf'(?!(.*{GENERIC_PATTERNS["detective"]}))(?!(.*(three|3).*(words))).*{GENERIC_PATTERNS["perpetrator"]}(?!(.*{GENERIC_PATTERNS["detective"]}))(?!(.*(three|3).*(words))).*(occur|show|first)?', prompt, flags=re.IGNORECASE)
        three_words_search = re.search(rf'(.*{GENERIC_PATTERNS["perpetrator"]}.*(three|3).*(words))|(.*(three|3).*(words).*{GENERIC_PATTERNS["perpetrator"]})', prompt, flags=re.IGNORECASE)
        detective_perpetrator_search = re.search(rf'(.*{GENERIC_PATTERNS["detective"]}.*{GENERIC_PATTERNS["perpetrator"]})|(.*{GENERIC_PATTERNS["perpetrator"]}.*{GENERIC_PATTERNS["detective"]})', prompt, flags=re.IGNORECASE)
        suspect_search = re.search(rf'.*{GENERIC_PATTERNS["suspect"]}.*(occur|show|first)?', prompt, flags=re.IGNORECASE)

        if(detective_search):
            chat_response_1()

        elif(crime_search):
            chat_response_2()

        elif(perpetrator_search):
            chat_response_3()

        elif(three_words_search):
            chat_response_4()

        elif(detective_perpetrator_search):
            chat_response_5()

        elif(suspect_search):
            chat_response_6()

        else:
            chat_response_unknown()
            continue
        
        print("\n What other questions do you have about the novel?")


    # 1. When does the investigator (or a pair) occur for the first time 
    # 2. When is the crime first mentioned
    # 3. When is the perpetrator first mentioned
    # 4. What are the three words that occur around the perpetrator on each mention
    # 5. When and how the detective/detectives and the perpetrators co-occur 
    # 6. When are other suspects first introduced