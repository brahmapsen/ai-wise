import fitz  # PyMuPDF
from fuzzywuzzy import fuzz
import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

from sentence_transformers import SentenceTransformer, util

# Ensure you have downloaded necessary resources for nltk
# nltk.download('punkt')
# nltk.download('stopwords')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    cleaned_text = ' '.join([word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words])
    return cleaned_text

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print("No file:", pdf_path)
        return None
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

## Compare files
def find_resume_match_percent(job_req_content,  resume_content):
    if not resume_content:
        return "Error: resume_content must be provided"
    if not job_req_content:
        return "Error: job_req_content must be provided"

    # Extract text from the PDF files using the provided paths
    # resume_text = extract_text_from_pdf(resume_content)
    # job_req_text = extract_text_from_pdf(job_req_content)

    # Extract and preprocess texts
    resume_text = preprocess_text(extract_text_from_pdf(resume_content))
    job_req_text = preprocess_text(extract_text_from_pdf(job_req_content))

    if resume_text is None or job_req_text is None:
        return "Error: One or both files not found"

    # Get similarity score
    similarity_score = get_similarity(resume_text, job_req_text) * 100

    # print(f"Similarity Score: {similarity_score}")
    # Compare the two texts using FuzzyWuzzy
    # similarity_score = fuzz.ratio(job_req_text,resume_text)

    score2 =  find_resume_match_percent2(job_req_content,  resume_content)  * 100
    print ("Score2:", score2)

    return similarity_score



def find_resume_match_percent2(job_req_content,  resume_content):
  # Load pre-trained model
  model = SentenceTransformer('all-MiniLM-L6-v2')

  # Extract and preprocess texts
  resume_text = preprocess_text(extract_text_from_pdf(resume_content))
  job_req_text = preprocess_text(extract_text_from_pdf(job_req_content))

  # Encode texts to get embeddings
  resume_embedding = model.encode(resume_text)
  job_req_embedding = model.encode(job_req_text)

  # Compute cosine similarity
  similarity_score = util.cos_sim(resume_embedding, job_req_embedding).item()
  print(f"Semantic Similarity Score: {similarity_score}")

  return similarity_score


