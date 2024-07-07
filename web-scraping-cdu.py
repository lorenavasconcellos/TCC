import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://udcsummary.info/php/index.php?id=13358&lang=pt'
driver.get(url)

# Encontrar todos os nós do 27 ao 84 (nesse caso são os de computação para teste inicial)
node_elements = driver.find_elements(By.CLASS_NAME, 'node')[27:84]

results = []

for element in node_elements:
    
    node_title = element.get_attribute('title')
    
    # Encontrar todos os elementos que contém os códigos de cada nó
    nodetag_elements = element.find_elements(By.CLASS_NAME, 'nodetag')
    for nodetag_element in nodetag_elements:
        
        nodetag_value = nodetag_element.get_attribute('innerHTML')
        
        results.append({'node_title': node_title, 'nodetag_value': nodetag_value})


df = pd.DataFrame(results)
print(df)
df.to_csv('area-computação-cdu.csv', index=False)

driver.quit()
