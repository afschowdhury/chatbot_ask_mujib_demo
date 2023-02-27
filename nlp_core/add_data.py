import add_question_from_excel
import pickle
import pandas as pd


if __name__ == '__main__':
    print("adding data ....")
    
    
    with open("data/qna.bin", "rb") as f:
        qna = pickle.load(f)
        
    initial_questions_length = len(qna)
    add_question_from_excel.add_bangla_questions()
    add_question_from_excel.add_english_questions()
    add_question_from_excel.add_question_from_internet(
        "data/Mujib Relevant Other Question(bangla).xlsx")
    add_question_from_excel.add_question_from_internet(
        "data/Mujib Relevant Other Question(English).xlsx")
    add_question_from_excel.add_question_from_internet(
        "data/Q&A for Chatbot in Bangla.xlsx")
    add_question_from_excel.add_question_from_internet(
        "data/Q&A for Chatbot in English.xlsx")

    with open("data/qna.bin", "rb") as f:
        qna = pickle.load(f)
    
    
    df = pd.DataFrame(qna)
    df.to_excel('data/qna.xlsx', index=False)
        
    after_adding_questions_length = len(qna)  
    print("Questions added !")
    print(f"Total number of questions : {after_adding_questions_length}")
    print(f"Total new questions added : {after_adding_questions_length-initial_questions_length}")
