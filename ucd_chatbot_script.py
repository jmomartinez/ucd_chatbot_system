import ast
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

questions = []
answers = []

for line in open('Datasets/faq_davis.json', 'r'): 
    #ast.literal_eval - safely evaluate an expression node or a string containing a Python literal or container display. 
    data = ast.literal_eval(line)
    questions.append(data['question'].lower())
    answers.append(data['answer'].lower())

# #TF-IDF = Term Frequency-Inverse Document Frequency
vectorizer = TfidfVectorizer(stop_words = 'english',lowercase=True)
X_tfidf = vectorizer.fit_transform(questions)

class chatbot:

    def __init__(self,question,answers,vectorizer,x_tfidf):
        self.q = question
        self.a = answers
        self.vect = vectorizer
        self.x_tfidf = x_tfidf

    def conversation(self,user_input):

        y_tfidf = self.vect.transform(user_input)

        angle = np.rad2deg(np.arccos(max(cosine_similarity(y_tfidf, self.x_tfidf)[0])))
        #The smaller the angle the higher the (cosine) similarity (i.e. the further the answer will be from the question)
        #However a larger angle allows for more user variation
        if angle > 60:
            return "Sorry, I didn't quite understand that"
        else:
            return answers[np.argmax(cosine_similarity(y_tfidf, self.x_tfidf)[0])]


    def main(self):
        user_name = input("Please enter your name: ")
        print("UC Davis Support: Hi, welcome to FAQ support. How can I help you?")

        while True:
            user_input = input("{}: ".format(user_name))
            if user_input.lower() == 'bye':
                print("FAQ Support: Goodbye!")
                break
            else:
                print("FAQ support: " + self.conversation([user_input]).capitalize())

if __name__ == '__main__':
    chatbot_sys = chatbot(answers,questions,vectorizer,X_tfidf)
    chatbot_sys.main()