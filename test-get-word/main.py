import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_thesaurus(keyword):
    url = f"https://tesaurus.kemdikbud.go.id/tematis/lema/{keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    synonyms = []
    # Contoh parsing HTML (sesuaikan dengan struktur website)
    for div in soup.find_all('div', class_='synonym'):
        synonyms.append(div.get_text().strip())
    
    return synonyms

# Contoh penggunaan
thesaurus_data = {
    "mobil": scrape_thesaurus("mobil"),
    "uang": scrape_thesaurus("uang"),
    # ... tambahkan kata lainnya
}

# Simpan ke CSV
pd.DataFrame(thesaurus_data.items(), columns=["keyword", "sinonim"]).to_csv("thesaurus_indonesia.csv", index=False)