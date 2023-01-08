from flask import Flask

import IPN_Scrapper
from IPN_Scrapper import create_quiz, create_pdf, create_docx
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello test'

@app.route('/api')
def hello_world2():
    return 'hello test2'

@app.route("/api/<string:fraza>/<int:number_of_questions>")
def get_questions(fraza, number_of_questions):
    quiz = create_quiz(fraza, number_of_questions)
    # return json.dumps({"questions": quiz}, indent=4, ensure_ascii=False)
    return {"questions": quiz, "pdf_url": create_pdf(quiz), "docx_url": create_docx(create_pdf(quiz))}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
