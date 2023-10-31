import requests
from fastapi import FastAPI, Depends
import uvicorn

BASE_URL = 'https://play.kahoot.it/rest/kahoots/ID'
color = ['Red', 'Blue', 'Yellow', 'Green']

app = FastAPI()

@app.get('/')
def getAnswer(quizId: str):
    url = requests.get(BASE_URL.replace("ID", quizId))
    resp = url.json()
    uuid = resp['uuid']
    questions = resp['questions']
    text = ""
    output = {'quiz': [], 'media': []}
    for i in range(len(questions)):
        try:
            if not 'question' in questions[i]:
                if questions[i]['type'] == 'content':
                    title = questions[i]['title']
                    description = questions[i]['description']
                    media = questions[i]['image']
                    text += (f'Content ({i+1}/{len(questions)}): {title}\nDescription: {description}\nMedia: {media}\n')
                    output['media'].append({'question_number': i+1, 'title': title, 'desc': description, 'media': media})
            else:
                question = questions[i]['question']
                choices = questions[i]['choices']
                answers = list(map(lambda x: x['correct'], choices))
                answer_idx = answers.index(True)
                answer = choices[answer_idx]['answer']

                text += f'Question ({i+1}/{len(questions)}): {question}\nAnswer: {answer} ({color[answer_idx]})'
                output['quiz'].append({'question_number': i+1, 'question': question, 'answer': answer, 'color': color[answer_idx]})
        except:
            continue
    print(text)
    return output

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=13737)