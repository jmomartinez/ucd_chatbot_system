# UC Davis Chatbot System

Novel neural network structures and data pre-processing techniques, along with an increased demand for virtual customer service, have en- abled the proliferation of QA models and chat- bot systems. In this paper, we contribute to the state of the field by constructing a UC Davis chatbot system based on students’ frequently asked questions (FAQs). Our novel UC Davis-based corpus was constructed through our web scraping algorithm and contains QA pairs on over thirty different topics ranging from reg- istration to campus operations. Additionally, through the Keras API and Stanford’s GloVe embedding technique, we successfully constructed a Dual Encoder LSTM network and encoded our QA pairs. However, despite our success in constructing the network and word embeddings we were forced to shift course and were unable to train the model due to time constraints. Nonetheless, we were determined to construct a QA model that would fundamentally mimic the behavior of our original model and were successful in doing so through a cosine similarity model. 

### Libraries Used
- BeautifulSoup & requests: For web scrapping & data collection
- re, numpy: For data wrangling & pre-processing
- matplotlib.pylot: For Visualization
- Keras: For initial dual LSTM constuction
- Sklearn: For Tfidf vectorization and application of cosine_similarity

### Concepts Applied
- Web Scrapping
- Data Wrangling
- Tokenization
- Tfidf Vectorization
- Retrieval-based Chatbot

Overall, we were able to construct a fully functioning chatbot system based on our novel UC Davis FAQ corpus and look forward to continuing our work in hopes of constructing a unified knowledge base for students.
