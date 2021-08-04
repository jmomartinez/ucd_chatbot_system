import requests
from bs4 import BeautifulSoup
import csv
import re

urls,page,soup_objects,results,answers,questions = [],[],[],[],[],[]
parser = 'html.parser'

#Moderate the amount of times you call this
urls.append('https://campusready.ucdavis.edu/student-faq') #########
urls.append('https://grad.ucdavis.edu/admissions/admission-faqs')
urls.append('https://housing.ucdavis.edu/covid19-faq/')
urls.append('https://cs.ucdavis.edu/graduate/current-students/faqs-current-grads')

#Pages
page.append(requests.get(urls[0])) ##########
page.append(requests.get(urls[1]))
page.append(requests.get(urls[2]))
page.append(requests.get(urls[3]))


#Soup-objects
soup_objects.append(BeautifulSoup(page[0].content, parser)) ############
soup_objects.append(BeautifulSoup(page[1].content, parser))
soup_objects.append(BeautifulSoup(page[2].content, parser))
soup_objects.append(BeautifulSoup(page[3].content, parser))


results.append(soup_objects[0].find(class_ = 'view-content')) ##########
result = soup_objects[1].find_all('ul', class_ = 'list--faq')

results.append(soup_objects[2].find(class_ = 'covid19-faq'))
results.append(soup_objects[3].find(class_ = 'node__content'))




# HTML is TAG based
# <p>   PARENT
#stuff
#<h1> CHILD
#Bullet point list
#<h1>
#<h3> CHILD of P.....SIBLING of <h1>
# Some header
#<h3>
#more stuff
#<p>


element1 = results[0].find_all('h3') ############
element2 = results[1].find_all('h3')
element3 = results[2].find_all('li')
e = results[2].find_all('p')


#Page one extraction
for elem in element1:

    #Data still has unicode characters (might want to clean it up, also might not)
    questions.append(elem.text)
    #Finds the next sibling of each element (p in this case)
    answers.append((elem.findNextSibling('p')).text)

print(len(questions))

#Page two extraction
for i in range(len(result)):
    j=0
    k=0
    for child in result[i].children:
        if j%2!=0:
            if k%2==0:
                questions.append(child.text)
            elif k%2!=0:
                #replaces \n with no space
                answers.append(re.sub(r"(\n)","",child.text))  ##(re.sub(r'(\s+|\n)', ' ', tags))## to remove more than one thing

            k+=1
        j+=1
print(len(questions))

#Page three extraction
for elem in element2:
    questions.append(elem.text)
    answers.append((elem.findNextSibling('p')).text)
questions.pop(196)
answers.pop(196)
  
print(len(questions))

#Page four extraction (maybe need to remove the space before the answers)
i=0
for elem in element3:
    # print(elem.text)
    # print('LENGTH OF STRING:',len(elem.text),'\n')
    # print()

    if i%2==0:
        questions.append(elem.text) #adds questions(even indices)
    elif (i%2!=0 and len(elem.text)<=1179): #adds ans of len<=1179
        answers.append(elem.text)


    if(len(elem.text)>1179 and i%2!=0):
        questions.pop() #removes question before long answer
    i+=1
print(len(questions))



# print(questions[len(questions)-18])
# print(answers[len(answers)-18])

# print(len(questions))
# print(len(answers))

#Creates a csv file with the data
with open('data.csv','w') as file:
    writer = csv.writer(file)
    writer.writerows(zip(questions, answers))

total_chars = 0
for i in range(len(questions)):
    total_chars = total_chars + len(questions[i]) + len(answers[i])

print('Total Characters: ', total_chars)
print('Total QA Pairs: ', len(questions))

print(questions[0])
print(len(questions[0]))