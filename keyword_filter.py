import unicodedata
import re
try:
    from word2number import w2n
    use_w2n = True
except ImportError:
    use_w2n = False

def normalize_input(text):
    text = unicodedata.normalize('NFKD', text)  # normalize diacritics
    text = ''.join(c for c in text if not unicodedata.combining(c))  # remove diacritic marks
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation/symbols
    return text.lower()  # convert to lowercase

def checkKeyword(keyword, movies):
    if not isinstance(keyword, str) or not keyword.strip():
        return False

    normalized_keyword = normalize_input(keyword)
    input_words = normalized_keyword.split()

    # list of (word, numeral_equiv) for each input word
    input_word_pairs = []
    for word in input_words:
        numeral = None
        if use_w2n:
            try:
                numeral = str(w2n.word_to_num(word))
            except ValueError:
                pass
        input_word_pairs.append((word, numeral))


    # iterate over each movie in the movies list
    for movie in movies:
        # combine movie name and description
        combined_text = movie.get("name", "") + " " + movie.get("description", "")
        normalized_text = normalize_input(combined_text)
        text_words = normalized_text.split()

        # compute numeric equivalents for text numbers
        text_num_words = set()
        if use_w2n:
            for tw in text_words:
                try:
                    text_num_words.add(str(w2n.word_to_num(tw)))
                except ValueError:
                    continue

        # check if every input word (numeral) is present in text_words
        all_matched = True
        for word, numeral in input_word_pairs:
            if numeral is not None:
                # check if either numeral or spelled number is present
                if not (any(word in tw for tw in text_words) or (numeral in text_num_words)):
                    all_matched = False
                    break
            else:
                # non-numeric: check if substring of word
                if not any(word in tw for tw in text_words):
                    all_matched = False
                    break
        if all_matched:
            print(keyword, "found in movie:", movie)
            return True

    print(keyword, "not found in any movie, please try a less specific input")
    return False