import enchant
import difflib
from pyphonetics import RefinedSoundex
rs = RefinedSoundex()
from difflib import SequenceMatcher

english_lang = enchant.Dict("en_US")


# Checks words at lookup time if the word is spelled wrong, compares to all words we currently have
def simliarityLookup(word, big_dict, phrase):
    times = []
    used_words = []
    words_found = []


    # Gets the word if it is mispelled its not in the dictionary
    if not english_lang.check(word) and word not in big_dict:
        for value in big_dict:
            # Will get anything starting with the word aslong as its not inside a phrase.
            if value.startswith(word) and not phrase:
                used_words.append(value)
                words_found.append(value)
                times += big_dict[value][0]

        #New phonetics method
        test_found = []
        test_times =[]

        suggestion = english_lang.suggest(word)[0]
        possible_words = difflib.get_close_matches(word, big_dict.keys(), len(big_dict))
        for s in possible_words:
            if rs.distance(suggestion,s) <= 2:
                test_found.append(s)
                test_times += big_dict[s][0]

        #End new method

        potential_words = difflib.get_close_matches(word, big_dict.keys(), len(big_dict))
        potential_words = [x for x in potential_words if x not in used_words]
        for value in potential_words:
            words_found.append(value)
            times += big_dict[value][0]

    # If the word is spelled correctly or the NN spelled the word incorrectly in some/all occurences
    elif english_lang.check(word) or word in big_dict:
        for value in big_dict:
            # Will get anything starting with the word aslong as its not inside a phrase.
            if value.startswith(word) and not phrase:
                used_words.append(value)
                words_found.append(value)
                times += big_dict[value][0]

        #New phonetics method
        test_found = []
        test_times =[]

        possible_words = difflib.get_close_matches(word, big_dict.keys(), len(big_dict))
        for s in possible_words:
            if rs.distance(word,s) <= 1:
                test_found.append(s)
                test_times += big_dict[s][0]
        #End new method

        potential_words = difflib.get_close_matches(word, big_dict.keys(), len(big_dict))
        potential_words = [x for x in potential_words if x not in used_words]
        for value in potential_words:
            if value != word:
                if not english_lang.check(value) and word in english_lang.suggest(value):
                    words_found.append(value)
                    times += big_dict[value][0]
            else:
                words_found.append(value)
                times += big_dict[value][0]

    return words_found,times

def simliarityTranscription(word):
    if word:
        new_word = word
        if not english_lang.check(word):
            potential_words = english_lang.suggest(word)
            highest_simliarity = 0
            for value in potential_words:
                if (ratio := difflib.SequenceMatcher(None,word,value).ratio()) > highest_simliarity:
                    new_word = value.lower()
                    highest_simliarity = ratio

            if new_word[0] != word[0]:
                return new_word
            else:
                return word.lower()
        else:
            return word.lower()
    else:
        return word
