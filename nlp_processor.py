# nlp_processor.py

import nltk
nltk.download('punkt')


import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Lowercase and remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    tokens = word_tokenize(text)
    # Remove stopwords
    filtered = [w for w in tokens if w not in stop_words]
    return " ".join(filtered)

def extract_keywords_tfidf(articles, top_n=5):
    # Combine title and summary for better representation
    texts = [clean_text(article['title'] + " " + article['summary']) for article in articles]

    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)

    keywords = []
    feature_names = vectorizer.get_feature_names_out()

    for i in range(X.shape[0]):
        row = X[i].toarray().flatten()
        top_indices = row.argsort()[-top_n:][::-1]
        top_keywords = [feature_names[j] for j in top_indices if row[j] > 0]
        keywords.append(top_keywords)

    for i, kw in enumerate(keywords):
        articles[i]["keywords"] = kw

    return articles

# Example run
if __name__ == "__main__":
    from rss_reader import fetch_articles
    articles = fetch_articles()
    processed = extract_keywords_tfidf(articles[:10])  # Use first 10 for test
    for art in processed:
        print(f"\nTitle: {art['title']}\nKeywords: {art['keywords']}")
