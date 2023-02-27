from sentence_transformers import SentenceTransformer
import numpy as np
import torch
from sentence_transformers.util import semantic_search
import pickle



retriever_model = SentenceTransformer('afschowdhury/st_model')

ques_embds = np.load('nlp_core/data/ques_embeddings.npy')

with open('nlp_core/data/questions.bin', 'rb') as f:
    ques = pickle.load(f)

with open('nlp_core/data/qna.bin', 'rb') as f:
    qnas = pickle.load(f)


def reload_data():
    global ques_embds, ques, qnas
    ques_embds = np.load('nlp_core/data/ques_embeddings.npy')

    with open('nlp_core/data/questions.bin', 'rb') as f:
        ques = pickle.load(f)

    with open('nlp_core/data/qna.bin', 'rb') as f:
        qnas = pickle.load(f)


def find_answer_qna(query):

    q_emb = retriever_model.encode(query)
    query_embeddings = torch.FloatTensor(q_emb)
    hits = semantic_search(query_embeddings, ques_embds, top_k=1)

    found_question = ques[hits[0][0]["corpus_id"]]
    confidence_score = hits[0][0]["score"]

    if confidence_score > 0.7:

        for qna in qnas:

            if qna['question'] == found_question:

                return qna['answer'], qna['image'], qna['video'] ,confidence_score, True
    else:
        return "Sorry, I did not understand your question.", "no_data", "no_data", confidence_score, False

    return "Invalid Input. Try with another question !"
