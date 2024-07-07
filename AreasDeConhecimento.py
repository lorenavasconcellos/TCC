from PyPDF2 import PdfReader
import re

# Leitura do pdf
def pdf_reader(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()
    return text

def process_text(text_pdf):
    # Remover números e caracteres especiais do texto
    text_without_numbers = re.sub(r'[\d:]', '', text_pdf)

    processed_text = re.sub('ÁREA DE AVALIAÇÃO', '', text_without_numbers)

    processed_text = re.sub('FUNDAÇÃO COORDENAÇÃO DE APERFEIÇOAMENTO DE PESSOAL DE NÍVEL SUPERIOR', '', processed_text)
    
    return processed_text

def extract_areas(processed_text):
    # Dividindo o texto em linhas
    linhas = processed_text.split('\n')

    # Removendo linhas em branco e espaços em branco em excesso
    linhas = [linha.strip() for linha in linhas if linha.strip()]

    # Retornando a lista de áreas
    return linhas

file_path = "C:\\Users\\Lorena Vasconcellos\\Documents\\Desenvolvimento\\TCC\\TCC\\Documentos\\24102022_Tabela_1844948_TabelaAreasConhecimento_atualizada_2022.pdf"

pdf_text = pdf_reader(file_path)

processed_text = process_text(pdf_text)

areas = extract_areas(processed_text)


