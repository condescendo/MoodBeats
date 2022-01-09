import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle
from nltk.stem.porter import PorterStemmer
df = pd.read_csv("/home/shrek/Desktop/projects/moodbeats/Train.csv")
corpus = []
texts = df['text']
stopwords_set = stopwords.words("english")
stemmer = PorterStemmer()
for i in texts:
    filtered = []
    filtered = [stemmer.stem(word) for word in i if word not in stopwords_set]
    filtered = " ".join(filtered)
    corpus.append(filtered)
stop = set(stopwords.words("english"))
vector = TfidfVectorizer(use_idf=True, lowercase =True, strip_accents = 'ascii', stop_words = stop)
x = vector.fit_transform(df.text)
pickle.dump(vector, open("transform.pkl", 'wb'))
y = df.label
X_train, X_test, Y_train, Y_test = train_test_split(x,y, test_size = 0.5, )

clf = MultinomialNB()
sentiment_analyse = clf.fit(X_train, Y_train)
pickle.dump(sentiment_analyse, open('model.pkl', "wb"))
model = pickle.load(open('model.pkl', 'rb'))




