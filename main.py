from fastapi import FastAPI, Request
from nlp_core import qna_answer as qna
import uvicorn
from nlp_core.utils import utils
from nlp_core import retrain
from fastapi.responses import JSONResponse
from threading import Thread
from langdetect import detect
from nlp_core.utils import auto_correct


app = FastAPI()


def check_language(text):
    try:
        language = detect(text)
        if language == 'bn':
            return 'Bengali'
        elif language == 'en':
            return 'English'
        else:
            return 'Other'
    except:
        return 'Error'


def is_english(text):
    english_words = ['who', 'what', 'whom', 'when', 'may', 'where', 'why', 'which', 'how', 'do', 'does', 'did', 'is', 'liked', 'loved',
                     'are', 'will', 'would', 'could', 'should', 'can', 'might', 'the', 'of', 'was', 'in', 'about', 'during', 'were', 'get', 'anybody']
    text = text.lower().split()
    for word in english_words:
        if word in text:
            return True
    return False


def banglish_to_bangla(data):

    return auto_correct.auto_correct(data)


@app.post("/ask_question")
async def read_root(request: Request):
    data = await request.json()

    print(data)
    if 'question' in data:
        user_input = data['question']
        if check_language(user_input) != 'Bengali':
            user_input = user_input.lower()
            if not is_english(user_input):
                user_input = banglish_to_bangla(user_input)

        user_input = utils.add_question_mark(user_input)
        query = utils.change_to_mujib([user_input])[0]
        answer, image, video, confidence_score, succesfully_answered = qna.find_answer_qna(
            query)

        print(image, video, answer)

        if image != "no_data" and video != "no_data":
            response = {"question": user_input,
                        "changedQuestion": query,
                        "answer": answer,
                        "score": confidence_score,
                        "isSuccessful": succesfully_answered,
                        "image": image,
                        "video": video}
        elif image != "no_data":
            response = {"question": user_input,
                        "changedQuestion": query,
                        "answer": answer,
                        "score": confidence_score,
                        "isSuccessful": succesfully_answered,
                        "image": image}
        elif video != "no_data":
            response = {
                "question": user_input,
                "changedQuestion": query,
                "answer": answer,
                "score": confidence_score,
                "isSuccessful": succesfully_answered,
                "video": video
            }
        else:
            response = {"question": user_input,
                        "changedQuestion": query,
                        "answer": answer,
                        "score": confidence_score,
                        "isSuccessful": succesfully_answered}

        return JSONResponse(content=response, status_code=200)

    else:
        response = {"message": "Please provide a question"}
        return JSONResponse(content=response, status_code=400)


# -------------------------- data add --------------------

def check_data(list2, elem1, elem2):
    if elem1 in list2 and elem2 in list2:
        return True
    else:
        return False


@app.post("/add_question")
async def read_root(request: Request):
    data = await request.json()
    print(data)
    data_fields = list(data.keys())

    data_dict = {}

    if not check_data(data_fields, "question1", "answer"):
        response = {
            "message": "Data not added! Please check the data format and try again"
        }

        return JSONResponse(content=response, status_code=400)

    data_dict["question1"] = data["question1"]
    if 'question2' in data_fields:
        data_dict["question2"] = data["question2"]
    if 'question3' in data_fields:
        data_dict["question3"] = data["question3"]
    if 'question4' in data_fields:
        data_dict["question4"] = data["question4"]
    data_dict["answer"] = data["answer"]

    response = {"data": data_dict}

    t1 = Thread(target=retrain.retrain, args=(data_dict,))
    t1.start()

    return JSONResponse(content=response, status_code=200)


@app.post("/add_auto_correction")
async def read_root(request: Request):
    data = await request.json()

    wrong_spelling = data["wrong_spelling"]
    correct_spelling = data["correct_spelling"]

    auto_correct.add_data(wrong_spelling, correct_spelling)

    response = {
        "message": "Data  added!"
    }

    return JSONResponse(content=response, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)
