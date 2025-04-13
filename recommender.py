import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy
from collections import Counter

# Load spaCy model for Named Entity Recognition (NER) and NLP
nlp = spacy.load("en_core_web_sm")

# Function to process article text and extract keywords using spaCy
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    return keywords

# Function to calculate cosine similarity between two text lists of keywords
def calculate_similarity(keywords_user, keywords_article):
    all_keywords = list(set(keywords_user + keywords_article))
    vec_user = np.array([keywords_user.count(keyword) for keyword in all_keywords])
    vec_article = np.array([keywords_article.count(keyword) for keyword in all_keywords])
    return cosine_similarity([vec_user], [vec_article])[0][0]

# Function to get article scores based on user preferences
def score_articles(user, articles):
    recommended_articles = []
    
    for article in articles:
        keywords_article = extract_keywords(article['title'] + " " + article['summary'])
        
        # Match with user interests (i.e., keyword matching)
        keywords_user = extract_keywords(user['interests'])
        similarity_score = calculate_similarity(keywords_user, keywords_article)
        
        # Preferred sources
        source_score = 1 if article['source'] in user['preferred_sources'] else 0
        
        # Combine scores
        total_score = similarity_score + source_score
        
        # Append article with its score
        recommended_articles.append({'title': article['title'], 'score': total_score, 'source': article['source'], 'keywords': keywords_article})
    
    # Sort articles by score (highest to lowest)
    recommended_articles = sorted(recommended_articles, key=lambda x: x['score'], reverse=True)
    
    # Avoid duplicate topics (using a set of keywords)
    seen_keywords = set()
    final_recommendations = []
    
    for article in recommended_articles:
        if not any(keyword in seen_keywords for keyword in article['keywords']):
            final_recommendations.append(article)
            seen_keywords.update(article['keywords'])
    
    return final_recommendations

# Sample user data
user = {
    'interests': "Artificial Intelligence, Machine Learning, Healthcare, Cybersecurity",
    'preferred_sources': ["TechCrunch", "MIT Technology Review"]
}

# Sample article data
articles = [
    {'title': "AI in Healthcare: Revolutionizing Medicine", 'summary': "AI is changing the healthcare landscape.", 'source': "TechCrunch"},
    {'title': "Cybersecurity Threats in 2025", 'summary': "The rise of cyber threats in modern tech.", 'source': "MIT Technology Review"},
    {'title': "Machine Learning for Business Intelligence", 'summary': "How machine learning can transform businesses.", 'source': "Forbes"},
    {'title': "AI Ethics and Governance", 'summary': "The ethical implications of AI technologies.", 'source': "MIT Technology Review"},
    {'title': "Data Privacy and Security in AI", 'summary': "Ensuring data privacy in AI systems.", 'source': "TechCrunch"}
]

# Get recommended articles
recommended_articles = score_articles(user, articles)

# Display recommended articles
for idx, article in enumerate(recommended_articles):
    print(f"{idx + 1}. {article['title']} (Score: {article['score']}) - Source: {article['source']}")
