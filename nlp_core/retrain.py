from nlp_core.utils import evaluate
from nlp_core.utils import utils
import numpy as np
import pickle
from nlp_core import qna_answer
import pandas as pd


with open('nlp_core/data/qna.bin', 'rb') as f:

    qnas = pickle.load(f)


def retrain(data):
    print("retraining...")
    fields = list(data.keys())
    only_questions = fields[:-1]

    questions = []
    for q in only_questions:
        questions.append(data[q])
    questions = utils.change_to_mujib(questions)

    qna = []

    for q in questions:
        qna.append(
            {
                'question': q,
                'answer': data['answer'],
                'image':'no_data',
                'video':'no_data'
            }
        )

    

    # ----------add to main excel----------
    existing_file = pd.read_excel('nlp_core/data/qna.xlsx')
    new_data = pd.DataFrame(qna)
    # updated_file = existing_file.append(new_data, ignore_index=True)
    updated_file = pd.concat([existing_file,new_data], ignore_index=True)
    updated_file.to_excel('nlp_core/data/qna.xlsx', index=False)
        
        
    # ----------add to add via api excel----------
    existing_file_api = pd.read_excel('nlp_core/data/added_via_api.xlsx')
    # updated_file_api = existing_file_api.append(new_data, ignore_index=True)
    updated_file_api = pd.concat([existing_file_api,new_data], ignore_index=True)
    updated_file_api.to_excel('nlp_core/data/added_via_api.xlsx', index=False)
        
    
    qnas.extend(qna)
    all_questions = utils.all_questions_from_qna(qnas)
    ques_embeddings = evaluate.get_embeddings(all_questions)
    base_dir = 'nlp_core/data/'

    all_ques_path = base_dir+'questions.bin'
    utils.save_list(all_ques_path, all_questions)

    embds_path = base_dir+'ques_embeddings.npy'
    utils.save_embeddings(embds_path, ques_embeddings)

    qna_path = base_dir+'/qna.bin'
    utils.save_list(qna_path, qnas)

    qna_answer.reload_data()
    print("data retrained")
