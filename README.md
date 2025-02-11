# AI Resume Matcher

An AI-powered application that automatically matches resumes to job descriptions using Natural Language Processing and Machine Learning techniques.

## Features

- Upload resume in PDF or DOCX format
- Process job descriptions
- Calculate match percentage using BERT embeddings
- Extract and compare skills
- Identify matching and missing skills
- Modern and responsive user interface

## Installation

1. Clone this repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:8080`
3. Upload a resume (PDF or DOCX format)
4. Enter the job description
5. Click "Analyze Match" to see the results

## Technical Details

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **ML/NLP**: 
  - BERT (DistilBERT) for text embeddings
  - spaCy for NLP tasks
  - Cosine similarity for matching
- **File Processing**: 
  - PyPDF2 for PDF files
  - python-docx for DOCX files

## Note

This is a basic implementation and can be enhanced with:
- More comprehensive skills database
- Advanced text preprocessing
- Additional resume formats support
- Custom scoring algorithms
- User authentication
- Resume and job posting management
