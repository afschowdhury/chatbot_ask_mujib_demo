from utils import evaluate
from utils import utils
import pandas as pd
import pickle


       

def add_bangla_questions(file_path="data/with_media/Bangla dataset with image and video link.xlsx"):

    df = pd.read_excel(file_path)

    # q1, q2, q3, q4 = utils.all_questions_from_excel(file_path)
    q1, q2, q3, q4 = utils.mujib_relevant_questions_from_excel(file_path)

    answers_series = df.Answer.dropna()
    images = df['image']
    videos = df['video']

    q1, q1_idx = utils.question_context_splitter(q1)
    q2, q2_idx = utils.question_context_splitter(q2)
    q3, q3_idx = utils.question_context_splitter(q3)
    q4, q4_idx = utils.question_context_splitter(q4)

    answers, ans_idx = utils.question_context_splitter(answers_series)
    ques = []

    ques.extend(q1)
    ques.extend(q2)
    ques.extend(q3)
    ques.extend(q4)

    ques_changed = utils.change_to_mujib(ques)

    idx = []

    idx.extend(q1_idx)
    idx.extend(q2_idx)
    idx.extend(q3_idx)
    idx.extend(q4_idx)

    qna = []
    for q, index in zip(ques_changed, idx):

        for a, image, video, i in zip(answers, images, videos, ans_idx):

            if index == i:
                if type(image) != str:
                    image = "no_data"

                if type(video) != str:
                    video = "no_data"

                qna.append(

                    {
                        "question": q,
                        "answer": a,
                        "image": image,
                        "video": video,
                    }
                )
                

    all_questions = utils.all_questions_from_qna(qna)

    ques_embeddings = evaluate.get_embeddings(all_questions)

    base_dir = 'data/'

    all_ques_path = base_dir+'questions.bin'

    utils.save_list(all_ques_path, all_questions)

    embds_path = base_dir+'ques_embeddings.npy'

    utils.save_embeddings(embds_path, ques_embeddings)

    qna_path = base_dir+'/qna.bin'

    utils.save_list(qna_path, qna)

    print("bangla data added !")
    
    
def add_english_questions(file_path="data/with_media/English DataSet with Image and Video Link.xlsx"):

    df = pd.read_excel(file_path)

    q1, q2, q3, q4 = utils.mujib_relevant_questions_from_excel(file_path)
    answers_series = df.Answer.dropna()
    
    images = df['image']
    videos = df['video']

    q1, q1_idx = utils.question_context_splitter(q1)
    q2, q2_idx = utils.question_context_splitter(q2)
    q3, q3_idx = utils.question_context_splitter(q3)
    q4, q4_idx = utils.question_context_splitter(q4)

    answers, ans_idx = utils.question_context_splitter(answers_series)
    ques = []

    ques.extend(q1)
    ques.extend(q2)
    ques.extend(q3)
    ques.extend(q4)

    ques = [q.lower() for q in ques]
    ques_changed = utils.change_to_mujib_english(ques)

    idx = []

    idx.extend(q1_idx)
    idx.extend(q2_idx)
    idx.extend(q3_idx)
    idx.extend(q4_idx)

    qna = []
    for q, index in zip(ques_changed, idx):

        for a, image, video, i in zip(answers, images, videos, ans_idx):

            if index == i:
                if type(image) != str:
                    image = "no_data"

                if type(video) != str:
                    video = "no_data"
                    
                qna.append(

                    {
                        "question": q,
                        "answer": a,
                        "image": image,
                        "video": video,
                    }
                )
    
    
    with open('data/qna.bin', 'rb') as f:

            qnas = pickle.load(f)
        
        
        
    qnas.extend(qna)
    


    all_questions = utils.all_questions_from_qna(qnas)

    ques_embeddings = evaluate.get_embeddings(all_questions)

    base_dir = 'data/'

    all_ques_path = base_dir+'questions.bin'

    utils.save_list(all_ques_path, all_questions)

    embds_path = base_dir+'ques_embeddings.npy'

    utils.save_embeddings(embds_path, ques_embeddings)

    qna_path = base_dir+'/qna.bin'

    utils.save_list(qna_path, qnas)

    print("english data added !")
    
        
    

def add_question_from_internet(file_path):
    
    
    df = pd.read_excel(file_path)
    questions = df['Question'].tolist()
    answers = df['Answer'].tolist()
    images = df['image'].tolist()
    videos = df['video'].tolist()
    
    qna = []
    for q, a ,i,v in zip(questions, answers,images,videos):
        
        if type(i)!= str:
            i = "no_data"
        if type(v)!= str:
            v = "no_data"

        
        qna.append({
            'question': q,
            'answer': a,
            'image': i,
            'video': v
        })
        

    

    
    with open('data/qna.bin', 'rb') as f:

        qnas = pickle.load(f)
    
    qnas.extend(qna)
    all_questions = utils.all_questions_from_qna(qnas)

    ques_embeddings = evaluate.get_embeddings(all_questions)

    base_dir = 'data/'

    all_ques_path = base_dir+'questions.bin'

    utils.save_list(all_ques_path, all_questions)

    embds_path = base_dir+'ques_embeddings.npy'

    utils.save_embeddings(embds_path, ques_embeddings)

    qna_path = base_dir+'/qna.bin'

    utils.save_list(qna_path, qnas)
    
    print("data added!")
    


if __name__ == '__main__':
    print("adding data ....")
    
    


    add_bangla_questions("data/with_media/Bangla dataset with image and video link.xlsx")
    add_english_questions("data/with_media/English DataSet with Image and Video Link.xlsx")
    add_question_from_internet(
        "data/with_media/Mujib related other question(bangla) with images and video.xlsx")
    add_question_from_internet(
        "data/with_media/Mujib Relevant other Question in English with image & video.xlsx")
    add_question_from_internet(
        "data/with_media/Q&A for Chatbot in Bangla.xlsx")
    add_question_from_internet(
        "data/with_media/Q&A for Chatbot in English.xlsx")

    with open("data/qna.bin", "rb") as f:
        qna = pickle.load(f)
    
    
    df = pd.DataFrame(qna)
    df.to_excel('data/qna.xlsx', index=False)
        
    after_adding_questions_length = len(qna)  
    print("Questions added !")
    print(f"Total number of questions : {after_adding_questions_length}")

