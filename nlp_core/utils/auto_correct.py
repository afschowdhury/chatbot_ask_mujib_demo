import pickle
import avro


with open("nlp_core/utils/auto_correct_dict.bin", "rb") as f:
    auto_correct_dict = pickle.load(f)


def load_data():
    global auto_correct_dict
    with open("nlp_core/utils/auto_correct_dict.bin", "rb") as f:
        auto_correct_dict = pickle.load(f)


def add_data(wrong_spelling, correct_spelling):

    load_data()
    auto_correct_dict.append(
        {
            "wrong_spelling": wrong_spelling,
            "correct_spelling": correct_spelling
        }
    )
    save_dict(auto_correct_dict)
    print("data added!")


def auto_correct(text):

    load_data()

    wrong_spellings = [w['wrong_spelling'] for w in auto_correct_dict]
    correct_spellings = [w['correct_spelling'] for w in auto_correct_dict]

    wrds = text.split(sep=" ")
    changed_query = []
    for word in wrds:
        if word not in wrong_spellings:
            changed_query.append(word)
        for i, w_sp in enumerate(wrong_spellings):
            if word == w_sp:
                changed_query.append(correct_spellings[i])

    query = ""
    for word in changed_query:
        query += word
        query += " "

    return avro.parse(query)


def save_dict(auto_correct_dict):
    load_data()
    with open("nlp_core/utils/auto_correct_dict.bin", "wb") as f:
        pickle.dump(auto_correct_dict, f)
        print("data saved!")
