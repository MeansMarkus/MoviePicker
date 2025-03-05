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

def checkKeyword(keyword, descriptions):
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

    # iterate over each description
    for desc in descriptions:
        normalized_desc = normalize_input(desc)
        desc_words = normalized_desc.split()

        # compute numeric equivalents for description words
        desc_num_words = set()
        if use_w2n:
            for d in desc_words:
                try:
                    desc_num_words.add(str(w2n.word_to_num(d)))
                except ValueError:
                    continue

        # check if every input word (or numeral) is present
        all_matched = True
        for word, numeral in input_word_pairs:
            if numeral is not None:
                # check if either numeral or spelled number is present in description
                if not (any(word in d for d in desc_words) or (numeral in desc_num_words)):
                    all_matched = False
                    break
            else:
                # non-numeric: require substring of description word
                if not any(word in d for d in desc_words):
                    all_matched = False
                    break
        if all_matched:
            print(keyword, "found: {desc}")
            return True

    print(keyword, "not found, please try a less specific input")
    return False
