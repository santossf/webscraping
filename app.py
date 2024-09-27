from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import pdfplumber
import os

app = Flask(__name__)

# Função para realizar scraping de um site
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'Sem título'
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        return {'title': title, 'content': ' '.join(paragraphs)}
    except Exception as e:
        return {'error': str(e)}

# Função para extrair texto de um PDF
def extract_pdf_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if url:
        result = scrape_website(url)
        return jsonify(result)
    return jsonify({'error': 'URL não fornecida.'})

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['file']
    pdf_path = os.path.join('static', pdf_file.filename)
    pdf_file.save(pdf_path)
    pdf_text = extract_pdf_text(pdf_path)
    return jsonify({'text': pdf_text})

if __name__ == '__main__':
    app.run(debug=True)
