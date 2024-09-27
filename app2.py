import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import pdfplumber

# Inicializa pdf_path
pdf_path = None

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

# Função para processar o link ou o PDF
def process_data():
    global pdf_path
    url = url_entry.get()
    if url:
        result = scrape_website(url)
        if 'error' in result:
            messagebox.showerror("Erro", result['error'])
        else:
            result_text.set(f"Título: {result['title']}\n\nConteúdo: {result['content']}")
    elif pdf_path:
        pdf_text = extract_pdf_text(pdf_path)
        if pdf_text:
            result_text.set(f"Texto extraído: {pdf_text[:500]}")  # Mostra os primeiros 500 caracteres
        else:
            messagebox.showinfo("Info", "Não foi encontrado texto no PDF.")
    else:
        messagebox.showerror("Erro", "Por favor, insira um link ou faça upload de um PDF.")

# Função para carregar um arquivo PDF
def upload_pdf():
    global pdf_path
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        pdf_label.config(text=f"Arquivo PDF: {pdf_path.split('/')[-1]}")

# Criação da interface
root = tk.Tk()
root.title("Web Scraping e PDF Extractor")

url_label = tk.Label(root, text="Digite o link do site:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

pdf_label = tk.Label(root, text="Ou faça upload de um PDF:")
pdf_label.pack()

pdf_button = tk.Button(root, text="Selecionar PDF", command=upload_pdf)
pdf_button.pack()

process_button = tk.Button(root, text="Processar", command=process_data)
process_button.pack()

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400, justify="left")
result_label.pack()

root.mainloop()