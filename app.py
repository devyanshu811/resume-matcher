from flask import Flask, request, jsonify, render_template
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
import PyPDF2
import docx
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__, static_url_path='', static_folder='static')

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def preprocess_text(text):
    """Preprocess text by tokenizing and removing stopwords"""
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return " ".join(tokens)

def extract_skills(text):
    """Extract skills from text using NLTK"""
    tokens = word_tokenize(text.lower())
    # This is a simple example. In production, you'd want a comprehensive skills database
    common_skills = [
        "python", "java", "javascript", "html", "css", "sql", "nosql", "react", 
        "angular", "vue", "node", "express", "django", "flask", "spring", 
        "machine learning", "data analysis", "ai", "artificial intelligence",
        "cloud", "aws", "azure", "gcp", "docker", "kubernetes", "devops",
        "agile", "scrum", "git", "ci/cd", "rest", "graphql", "microservices"
    ]
    skills = []
    for skill in common_skills:
        if skill in text.lower():
            skills.append(skill)
    return list(set(skills))

def calculate_match_score(resume_text, job_description):
    """Calculate matching score between resume and job description using TF-IDF and cosine similarity"""
    vectorizer = TfidfVectorizer()
    try:
        # Fit and transform the texts
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity * 100)
    except:
        # Fallback to simpler matching if TF-IDF fails
        resume_tokens = set(word_tokenize(resume_text.lower()))
        job_tokens = set(word_tokenize(job_description.lower()))
        similarity = 1 - jaccard_distance(resume_tokens, job_tokens)
        return float(similarity * 100)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match_resume():
    try:
        print("Received request")  # Debug log
        resume_file = request.files['resume']
        job_description = request.form['job_description']
        
        print(f"File type: {resume_file.filename}")  # Debug log
        
        # Extract text from resume based on file type
        if resume_file.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_file)
        elif resume_file.filename.endswith('.docx'):
            resume_text = extract_text_from_docx(resume_file)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
        
        print(f"Extracted text length: {len(resume_text)}")  # Debug log
        print(f"Job description length: {len(job_description)}")  # Debug log
        
        # Preprocess texts
        processed_resume = preprocess_text(resume_text)
        processed_job = preprocess_text(job_description)
        
        print(f"Processed resume length: {len(processed_resume)}")  # Debug log
        print(f"Processed job length: {len(processed_job)}")  # Debug log
        
        # Calculate match score
        match_score = calculate_match_score(processed_resume, processed_job)
        
        # Extract skills
        resume_skills = extract_skills(resume_text)
        required_skills = extract_skills(job_description)
        
        print(f"Resume skills: {resume_skills}")  # Debug log
        print(f"Required skills: {required_skills}")  # Debug log
        
        # Calculate skills match
        matching_skills = list(set(resume_skills) & set(required_skills))
        missing_skills = list(set(required_skills) - set(resume_skills))
        
        result = {
            'match_score': round(match_score, 2),
            'matching_skills': matching_skills,
            'missing_skills': missing_skills
        }
        print(f"Result: {result}")  # Debug log
        return jsonify(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
