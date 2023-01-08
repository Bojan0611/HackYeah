import re
import openai
from fpdf import FPDF
import os
import json

openai.api_key = "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"

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
    data = [int(s) for s in response['choices'][0]['text'].split() if s.isdigit()]
    return data[0]


json = { "questions": [ { "question": "Dlaczego władze ZSRS nie utrzymywały stosunków z rządem polskim na uchodźstwie?", "answers": [ "Władze ZSRS uważały, że rząd polski na uchodźstwie nie jest władnym i legalnym władzom polskim.", "Władze ZSRS uważały, że rząd polski na uchodźstwie jest zmanipulowany przez wpływy zachodnie i nie jest wiarygodnym partnerem.", "Władze ZSRS uważały, że rząd polski na uchodźstwie jest za słaby, aby utrzymać stosunki z ZSRS." ] }, { "question": "Co spowodowało konieczność podjęcia przez dowództwo AK decyzji o formie wystąpienia zbrojnego przeciw Niemcom?", "answers": [ "Konieczność podjęcia przez dowództwo AK decyzji o formie wystąpienia zbrojnego przeciw Niemcom spowodowała potrzeba obrony polskiego narodu przed niemieckimi agresorami.", "Konieczność podjęcia przez dowództwo AK decyzji o formie wystąpienia zbrojnego przeciw Niemcom spowodowała potrzeba obrony polskiej wolności i niepodległości.", "Konieczność podjęcia przez dowództwo AK decyzji o formie wystąpienia zbrojnego przeciw Niemcom spowodowała potrzeba obrony polskiej demokracji." ] }, { "question": "Jakie zagrożenia wiązały się z planem \"Burza\"?", "answers": [ "Plan \"Burza\" był potencjalnie niebezpieczny dla żołnierzy, którzy mieli brać w nim udział.", "Plan \"Burza\" mógł potencjalnie doprowadzić do eskalacji konfliktu zbrojnego.", "Plan \"Burza\" był potencjalnie niebezpieczny dla cywilów, którzy znajdowali się w obszarze jego zasięgu." ] }, { "question": "Dlaczego Armia Czerwona wkroczyła do Wilna i Lwowa?", "answers": [ "Armia Czerwona wkroczyła do Wilna i Lwowa, ponieważ chciała zapobiec rozprzestrzenianiu się bolszewizmu na tych obszarach.", "Armia Czerwona wkroczyła do Wilna i Lwowa, ponieważ chciała zapobiec rozprzestrzenianiu się nacjonalizmu na tych obszarach.", "Armia Czerwona wkroczyła do Wilna i Lwowa, ponieważ chciała zapobiec rozprzestrzenianiu się faszyzmu na tych obszarach." ] }, { "question": "Jakie były konsekwencje wycofywania się wojsk niemieckich z ZSRS dla Polski?", "answers": [ "W wyniku wycofywania się wojsk niemieckich z ZSRS, Polska odzyskała niepodległość.", "W wyniku wycofywania się wojsk niemieckich z ZSRS, Polska została zmuszona do ponownego uznania wschodniej granicy z ZSRS.", "W wyniku wycofywania się wojsk niemieckich z ZSRS, Polska stała się celem ataków ze strony Armii Czerwonej." ] }, { "question": "Co oznaczało przekroczenie przez Armię Czerwoną przedwojennej granicy Rzeczypospolitej?", "answers": [ "1", "2", "3" ] }, { "question": "Jakie były motywy Polaków w planowaniu \"Burzy\"?", "answers": [ "Chcieli zemścić się za krzywdy wyrządzone przez Rosjan.", "Chcieli zapobiec rozprzestrzenianiu się komunizmu.", "Chcieli ochronić wolność i demokrację." ] }, { "question": "Czy plan \"Burza\" został zrealizowany?", "answers": [ "Tak, plan \"Burza\" został zrealizowany.", "Nie, plan \"Burza\" nie został zrealizowany.", "Nie wiadomo, czy plan \"Burza\" został zrealizowany." ] }, { "question": "Jakie były konsekwencje planu \"Burza\" dla Polski?", "answers": [ "Plan \"Burza\" przyczynił się do wzmocnienia pozycji Polski na arenie międzynarodowej.", "Plan \"Burza\" doprowadził do znacznego wzrostu gospodarczego w Polsce.", "Plan \"Burza\" przyczynił się do zmniejszenia liczby uchodźców przybywających do Polski." ] }, { "question": "Jakie były konsekwencje planu \"Burza\" dla ZSRS?", "answers": [ "1", "2", "3" ] } ] }
# json = json.dumps(json, indent=4)

# with open("static/tmp.json", "w") as outfile:
#     outfile.write(json)


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
    dir_path = 'D:\hackyeah\IPN_Quiz_Gen'
    files = os.listdir(os.path.join(dir_path, 'static'))
    suffix = len(files)
    pdf.output(os.path.join(dir_path, 'static', 'quiz{}.pdf'.format(suffix)), 'F')
    return "path"

# create_pdf(json)


# create_pdf(json['questions'])
from pdf2docx import Converter
dir_path = 'D:\hackyeah\IPN_Quiz_Gen'
pdf_file = os.path.join(dir_path, 'static', 'quiz11.pdf')
docx_file = os.path.join(dir_path, 'static', 'quiz11.docx')
try:
    # Converting PDF to Docx
    cv_obj = Converter(pdf_file)
    cv_obj.convert(docx_file)
    cv_obj.close()

except:
    print('Conversion Failed')
    
else:
    print('File Converted Successfully')

