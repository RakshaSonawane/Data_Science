from flask import Flask, render_template, request
import PyPDF2
import language_tool_python
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
tool = language_tool_python.LanguageTool('en-US')

# Define keywords for a sample job role
required_keywords = ['Python', 'Machine Learning', 'Pandas', 'Data Analysis', 'SQL']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    uploaded_file = request.files['resume']
    text = ''

    if uploaded_file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()

    # NLP & Grammar Analysis
    doc = nlp(text)
    grammar_matches = tool.check(text)
    grammar_errors = len(grammar_matches)

    found_keywords = [kw for kw in required_keywords if kw.lower() in text.lower()]
    missing_keywords = list(set(required_keywords) - set(found_keywords))

    result = {
        'total_keywords': len(required_keywords),
        'found_keywords': found_keywords,
        'missing_keywords': missing_keywords,
        'grammar_errors': grammar_errors,
        'word_count': len(text.split())
    }

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
