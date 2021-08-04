import warnings
import csv
import numpy as np
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior() 
#print(tf.__version__)

#catches FutureWarnings generated from importing tensorflow stuff
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=FutureWarning)
    from keras.models import Sequential
    from keras.layers import Embedding,LSTM,Activation,Merge

    from keras.preprocessing.text import Tokenizer as tk
    from keras.preprocessing.sequence import pad_sequences as padding    

questions = []
answers = []
#Reads in columns of data file and appends question & answers lists 
with open('data.csv') as csvfile:
    data = csv.reader(csvfile)
    for Q, A in data:
        questions.append(Q)
        answers.append(A)

#print(len(questions)) #both Qs and As are length 196

#Creating word tokens for Qs and As
tokenizer = tk()
tokenizer.fit_on_texts(questions)
tokenizer.fit_on_texts(answers)
word_in = tokenizer.word_index
#print(word_in)

total_word_count = len(tokenizer.word_index) + 1
glove_dimension = 300
print("Total Word Count: ", total_word_count)
print('Glove Dimension: ', glove_dimension)

#Generating sentence sequences to create word-embeddings
question_seqs = tokenizer.texts_to_sequences(questions)
answer_seqs = tokenizer.texts_to_sequences(answers)

#Calculating the maximum length of the seqences
max_seq_length = 0
for seq in question_seqs + answer_seqs:
    if(max_seq_length < len(seq)):
        max_seq_length = len(seq) 

#print(max_seq_length)      


#Padding sequences with zeros (that way all sequences are the same length)
question_seqs = padding(question_seqs, maxlen = max_seq_length)
answer_seqs = padding(answer_seqs, maxlen = max_seq_length)

embedding_dict = {}

#Using Glove word embeddings to create the embedding matrix
with open('glove.6B.300d.txt', encoding='utf8') as glove_embeddings:
    for line in glove_embeddings:
        vals = line.split() #separates strings to individual words
        word = vals[0]
        embedding_vect = np.asarray(vals[1:], dtype = 'float32')
        embedding_dict[word] = embedding_vect


weight_emb_matrix = np.zeros((total_word_count,glove_dimension))
for word,index in word_in.items():
    emb_vector = embedding_dict.get(word)
    if emb_vector is not None:
        weight_emb_matrix[index] = embedding_vect
    

print(weight_emb_matrix.shape)
print(weight_emb_matrix[1].shape)

#Model Construction
question_branch = Sequential([
    Embedding(
    input_dim = total_word_count, 
    output_dim = 300, 
    input_length = max_seq_length, 
    weights = [weight_emb_matrix], 
    mask_zero = True, 
    trainable = False),
    LSTM(output_dim = 256)])

answer_branch = Sequential([
    Embedding(
    input_dim = total_word_count, 
    output_dim = 300, 
    input_length = max_seq_length, 
    weights = [weight_emb_matrix], 
    mask_zero = True, 
    trainable = False),
    LSTM(output_dim = 256)])

#question_branch.summary()

#Merging the branches
final_model = Sequential([
    Merge([question_branch,answer_branch], mode='mul'),
    Activation('softmax')])

final_model.compile(optimizer = 'adam', loss = 'categorical_crossentropy',metrics = ['accuracy'])

print(question_seqs.shape)
print(answer_seqs.shape)

final_model.fit([question_seqs[0], answer_seqs[0]],answer_seqs[0], batch_size = 256,nb_epoch = 5)