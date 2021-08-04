import requests
import pprint as pp
from bs4 import BeautifulSoup

URL = 'https://studentaffairs.ucdavis.edu/news/counseling-services-frequently-asked-questions'
page = requests.get(URL)

#print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(class_ = 'l-content')

#print(results)

elements = results.find_all('dt')
elements2 = results.find_all('div')
#print(type(elements))
results1 = soup.find(class_ = 'clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')
elements3 = results1.find_all('div')


i=0
questions = []
answers = []
#print(type(questions))
#question = list, elements = str

for ques in elements:
    a = ques.text
    if i<9: 
        a = a[4:]
        questions.append(a)
    else:
        a = a[5:]
        questions.append(a)


    print(questions[i])
    print()
    i+=1

j=0
for elem in elements2:
    answers.append((elem.findNextSibling('p')))
    print(answers[j])
    j+=1

#print(answers)
#i = 0
#for elem in e:
    #answers.append((elem.findChildren('p')).text)
    ##print(answers[i])
    #i+=1

