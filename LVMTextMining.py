import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Leitura dos pdfs
def pdf_reader(folder_path):
    texts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "rb") as file:
                pdf_reader = PdfReader(file)
                text = ""
                for page_number in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_number] 
                    text += page.extract_text()
            texts.append(text)
    return texts

# Mineiração de texto
def process_text(text_pdf):
    # Tokenização
    tokens = word_tokenize(text_pdf.lower())

    # Remove stop words em português, em inglês e stopwords personalizadas
    filtered_tokens = [token for token in tokens if token not in stopwords.words('portuguese') and token not in stopwords.words('english') and token not in custom_stopwords]

    # Remove pontuações
    punctuation = string.punctuation
    filtered_tokens = [token for token in filtered_tokens if token not in punctuation]

    # Remove números e palavras com menos de 2 caracteres
    filtered_tokens = [token for token in filtered_tokens if not token.isdigit() and (token.isalpha() and len(token) > 2)]

    # Lematização
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Converte os tokens para string
    processed_text = ' '.join(lemmatized_tokens)

    return processed_text

# Seleciona as 50 palavras mais citadas em cada pdf
def get_top_words_per_pdf(texts):
    top_words_per_pdf = []
    for text in texts:
        processed_text = process_text(text)
        word_counts = Counter(processed_text.split())
        top_words = word_counts.most_common(50)
        top_words_per_pdf.append(top_words)
    return top_words_per_pdf

# Gera um gráfico com as palavras
def create_dataframe(top_words_per_pdf):
    data = {'PDF': [], 'Palavra': [], 'Frequência': []}
    for i, top_words in enumerate(top_words_per_pdf):
        for word, freq in top_words:
            data['PDF'].append(f'PDF_{i+1}')
            data['Palavra'].append(word)
            data['Frequência'].append(freq)
    return pd.DataFrame(data)

# Exporta o gráfico como arquivo csv
def export_dataframe_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Palavras personalizadas para serem excluídas 
custom_stopwords = ["estudo", "estudos", "pesquisa", "pesquisas", "trabalho", "artigo", "artigos", "autor", "autores", "extensão", "sobre", "projeto"]

folder_path_pdf = "C:\\Users\\Lorena Vasconcellos\\Documents\\Desenvolvimento\\TCC\\TCC\\Documentos\\pdfs"

texts = pdf_reader(folder_path_pdf)

top_words_per_pdf = get_top_words_per_pdf(texts)

df = create_dataframe(top_words_per_pdf)

export_dataframe_to_csv(df, 'tabela.csv')
