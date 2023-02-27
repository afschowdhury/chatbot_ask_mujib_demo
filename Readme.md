# 🧪 Mujib Jiggasa Chatbot Server 🧠 
This repository contains the backend server code for a chatbot that can answer any question related to Sheikh Mujibur Rahman, built using FastAPI.



## Getting Started
<hr>
To get started, follow the instructions below:

### Prerequisites
- Python 3.6 or higher
- pip package manager

## Installation
<hr>

### Clone the repository:

```bash
git clone https://github.com/your-username//chatbot_ask_mujib_demo.git
```

### Create a virtual environment and activate it:

```bash
cd chatbot_ask_mujib_demo
python3 -m venv env
source env/bin/activate 
```
### Install the dependencies:

```pip install -r requirements.txt```



### Start the server:

```python main.py```

The server is now running on http://localhost:8080/.

## API Endpoints
<hr>
POST /chat
This endpoint expects a JSON payload in the following format:

```json
{
  "question": "<user-question>"
}
```

Replace <user-question> with the question sent by the user.

The server will respond with a JSON payload in the following format:

```json
{
    "question": "user question ?",
    "changedQuestion": "pre processed question",
    "answer": "chatbot answer",
    "score": "confidence_score",
    "isSuccessful": "succesfull_or_not",
    "image": "image_url",
    "video": "video_url"
}

```
