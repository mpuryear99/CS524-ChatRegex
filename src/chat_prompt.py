import re


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


if __name__ == "__main__":
    # We could add functionality to determine which book the user is interested in
    detective_pattern = r'(\s(investigator|detective|inspector))'
    perpetrator_pattern = r'(\s(perpetrator|killer|criminal|murderer|culprit|evildoer|offender|villian))'
    victim_pattern = r'(victim|casualty)'
    crime_pattern = r'(crime|(murder[^a-z])|dead|offense|misdeed)'
    suspect_pattern = r'(suspect|accused|defendant)'

    print("Welcome to ChatRegex for Detective Novels!")
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
        detective = re.search(rf'{detective_pattern}', prompt, flags=re.IGNORECASE)
        perpetrator = re.search(rf'{perpetrator_pattern}', prompt, flags=re.IGNORECASE)

        # Determines which prompt the user refers to
        detective_search = re.search(rf'(?!(.*{perpetrator_pattern})).*{detective_pattern}(?!(.*{perpetrator_pattern})).*(occur|show|first)?', prompt, flags=re.IGNORECASE)
        crime_search = re.search(rf'.*{crime_pattern}.*(occur|show|first)?', prompt, flags=re.IGNORECASE)
        perpetrator_search = re.search(rf'(?!(.*{detective_pattern}))(?!(.*(three|3).*(words))).*{perpetrator_pattern}(?!(.*{detective_pattern}))(?!(.*(three|3).*(words))).*(occur|show|first)?', prompt, flags=re.IGNORECASE)
        three_words_search = re.search(rf'(.*{perpetrator_pattern}.*(three|3).*(words))|(.*(three|3).*(words).*{perpetrator_pattern})', prompt, flags=re.IGNORECASE)
        detective_perpetrator_search = re.search(rf'(.*{detective_pattern}.*{perpetrator_pattern})|(.*{perpetrator_pattern}.*{detective_pattern})', prompt, flags=re.IGNORECASE)
        suspect_search = re.search(rf'.*{suspect_pattern}.*(occur|show|first)?', prompt, flags=re.IGNORECASE)

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