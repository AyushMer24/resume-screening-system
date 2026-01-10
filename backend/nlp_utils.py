import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLP tools once
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text: str) -> str:
    """
    Cleans and normalizes input text for NLP processing.
    """

    # Lowercase
    text = text.lower()

    # Remove special characters & numbers
    text = re.sub(r"[^a-z\s]", " ", text)

    # Tokenization
    tokens = word_tokenize(text)

    # Stopword removal + lemmatization
    processed_tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token not in stop_words and len(token) > 2
    ]

    return " ".join(processed_tokens)


def match_resume_to_jobs(resume_text: str, jobs: list, top_k: int = 5):
    """
    Matches resume text with job descriptions using TF-IDF + Cosine Similarity.
    """

    job_texts = [job["description"] for job in jobs]

    # Combine resume + jobs for vectorization
    corpus = [resume_text] + job_texts

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Resume vector is index 0
    resume_vector = tfidf_matrix[0]
    job_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(resume_vector, job_vectors)[0]

    results = []

    for idx, score in enumerate(similarities):
        results.append({
            "job_title": jobs[idx]["title"],
            "similarity_score": round(float(score), 3)
        })

    # Sort by similarity score
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)

    return results[:top_k]