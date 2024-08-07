import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://udcsummary.info/php/index.php?id=13358&lang=pt'
driver.get(url)

# Encontrar todos os nós do 27 ao 84 (nesse caso são os de computação para teste inicial)
node_elements = driver.find_elements(By.CLASS_NAME, 'node')[27:84]

results = []

for element in node_elements:
    
    # Pegar os títulos de cada elemento e separar em palavras
    node_title_words = element.get_attribute('title').lower().split()

    # Remoção das stopwords
    filtered_words = [word for word in node_title_words if word not in stopwords.words('portuguese')]

    # Lematização
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_words]
    
    # Encontrar todos os elementos que contém os códigos de cada nó
    nodetag_elements = element.find_elements(By.CLASS_NAME, 'nodetag')
    for nodetag_element in nodetag_elements:

        # Pegar o valor do código e remover os caracteres indesejados
        nodetag_value = nodetag_element.get_attribute('innerHTML').replace('`', '').replace('/', '')
        
        for word in filtered_words:
            results.append({'area': word, 'code': nodetag_value})

df = pd.DataFrame(results)
print(df)
df.to_csv('area-computacao-cdu.csv', index=False)

driver.quit()
