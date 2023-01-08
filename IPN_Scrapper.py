import requests
from bs4 import BeautifulSoup
from goose3 import Goose
import openai
import re
import json
from fpdf import FPDF
import os
from pdf2docx import Converter

openai.api_key = "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"


class IPN_scrapper():
    base_url = 'https://szukaj.ipn.gov.pl/search?q=keyword&site=pages_przystanek_historia&btnG=Szukaj&client=default_frontend&output=xml_no_dtd&proxystylesheet=default_frontend&sort=date%3AD%3AL%3Ad1&wc=200&wc_mc=1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&tlen=200&size=50&filters=eyJXc3p5c3RraWVfc3Ryb255IjoxMDkyOSwicGFnZXNfemJyb2RuaWF3b2x5bnNrYSI6NTY2OSwicGFnZXNfZW5jeWtsb3BlZGlhX3NvbGlkYXJub3NjaSI6MTExOSwicGFnZXNfd3JvY2xhd2lwbiI6MTEwNiwicGFnZXNfaXBuIjo3OTcsInBhZ2VzX2NlbnRyYWxhaXBuX2VuIjo1MDMsInBhZ2VzX3ByenlzdGFuZWtfaGlzdG9yaWEiOjM1MywicGFnZXNfZ2lnYW5jaV9uYXVraSI6MzA1LCJwYWdlc19wb2xza2llX21pZXNpYWNlIjoyMjQsInBhZ2VzX2VkdWthY2phIjoxMjcsInBhZ2VzX3NsYWR5Ijo4M30='

    def __init__(self, phrase):
        self.phrase = phrase

    def __str__(self):
        return "IPN scrapper"

    def scrap_pages(self):
        g = Goose()
        result = []
        for link in self._get_top_ten_links(self.base_url):
            article = g.extract(url=link, )
            content = article.cleaned_text
            content_sentences = content.split(".")
            if len(content_sentences) > 5:
                result.append(content)
        return result

    def _get_top_ten_links(self, base_url):
        page = requests.get(base_url.replace("keyword", self.phrase.replace(" ", "+")))
        soup = BeautifulSoup(page.content, "html.parser")
        links = [link['href'] for link in soup.find_all('a', href=True) if "http" in link['href']]
        return links[1:11]


class QuizGenerator:

    def __init__(self, text):
        self.text = text

    def create_quiz(self, n_questions, n_answers):
        quiz = []
        questions = self._generate_questions(n_questions)
        for question in questions:
            answers = self._generate_answers(n_answers, question)
            d = {"question": question, "answers": answers}
            quiz.append(d)
        return quiz

    def _generate_questions(self, n):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt="Wygeneruj {n_quest} pytania do tekstu: \n".format(n_quest=n) + self.text,
            temperature=0.25,
            max_tokens=2137,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        questions = response['choices'][0]['text'].split("\n")
        questions = list(filter(None, questions))
        clean_questions = [self._clean_text(question) for question in questions]
        clean_questions = list(filter(None, clean_questions))
        return clean_questions
        # return [question.decode('ascii', 'ignore').encode('ascii') for question in clean_questions]
        
    def _clean_text(self, text):
        regex = '\.(.*)'
        r = re.compile(regex)
        if "." in text[:10]:
            result = r.findall(text)
        else:
            result = text
        return re.sub(r"^\s+", "", result[0])

    def _generate_answers(self, n, question):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt="Wygeneruj {n_quest} odpowiedzi do pytania: \n".format(n_quest=n) + question,
            temperature=0.25,
            max_tokens=2137,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        answers = response['choices'][0]['text'].split("\n")
        answers = list(filter(None, answers))
        return [self._clean_text(answer) for answer in answers]


def clear_phraze(fraza):
    return fraza.replace("_", " ")

def check_when(fraza):
    start_sequence = "\nA:"
    restart_sequence = "\n\nQ: "

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="{} rok".format(fraza),
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    try:   
        data = [int(s) for s in response['choices'][0]['text'].split() if s.isdigit()]
        return data[0]
    except:
        return 0
    
    
def create_quiz(fraza, number_of_questions):
    data = check_when(fraza)
    if data > 1917:
        scrapper = IPN_scrapper(clear_phraze(fraza))
        full_result = ' '.join(scrapper.scrap_pages())
        sentences = full_result.split(".")
        example_result = ' '.join(sentences[:15])
        qg = QuizGenerator(example_result)
        quiz = qg.create_quiz(number_of_questions, 3)
        # json_object = json.dumps(quiz, indent = 4, ensure_ascii=False) 
        # print(json_object)
        return quiz
    else:
        print("Nie znaleziono roku!")
        # return json.dumps({}, indent = 4, ensure_ascii=False) 

def create_pdf(json):
    # quiz = json["quiz"]
    questions = []
    answers = []
    for question in json:
        questions.append(question['question'])
        answers.append(question['answers'])
    
    pdf = FPDF()
    pdf.add_font('ArialLatin', '', 'arial.ttf', uni=True)
    pdf.add_page()
    for idx, question in enumerate(questions):
        pdf.set_font("ArialLatin", '', size = 10)

        if idx == 0:
            ln=0
        pdf.cell(200, 10, txt=question, border = 'C', ln = ln, align = '', fill = False, link = '')
        pdf.set_font('ArialLatin', '', 7)
        
        ln+=1
        qn=0
        pdf.cell(210, 10, txt='{}. '.format(qn+1)+answers[idx][qn], border = 'L', ln=ln)
        ln+=1
        qn+=1
        pdf.cell(210, 10, txt='{}. '.format(qn+1)+answers[idx][qn], border = 'L', ln=ln)
        ln+=1
        qn+=1
        pdf.cell(210, 10, txt='{}. '.format(qn+1)+answers[idx][qn], border = 'L', ln=ln)
        ln+=1
    dir_path = '/home/hakaton/front'
    files = os.listdir(os.path.join(dir_path, 'static'))
    suffix = len(files)
    pdf.output(os.path.join(dir_path, 'static', 'quiz{}.pdf'.format(suffix)), 'F')
    return os.path.join(dir_path, 'static', 'quiz{}.pdf'.format(suffix))

def create_docx(pdf_path):
    docx_path = pdf_path.replace(".pdf", ".docx")
    try:
        # Converting PDF to Docx
        cv_obj = Converter(pdf_path)
        cv_obj.convert(docx_path)
        cv_obj.close()

    except:
        print('Conversion Failed')
    return docx_path

