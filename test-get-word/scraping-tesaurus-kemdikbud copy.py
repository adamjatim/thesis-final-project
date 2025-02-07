import requests
import time
import csv
from bs4 import BeautifulSoup

# URL dasar untuk Tesaurus Kemdikbud
BASE_URL = "https://tesaurus.kemdikbud.go.id/tematis/lema/"

def get_synonyms(word):
    """
    Mengambil sinonim dari Tesaurus Kemdikbud berdasarkan kata kunci.
    """
    url = BASE_URL + word
    response = requests.get(url)

    # if response.status_code != 200:
    #     print(f"Gagal mengambil data untuk: {word}")
    #     return []

    soup = BeautifulSoup(response.text, "html.parser")
    synonym_list = []

    # Mencari semua elemen dengan class "one-par-content"
    for div in soup.find_all("div", class_="one-par-content"):
        for link in div.find_all("a", class_="lemma-ordinary"):
            synonym = link.get_text(strip=True)  # Ambil teks sinonim
            synonym_list.append(synonym)

    return list(set(synonym_list))  # Hapus duplikasi sinonim

def process_kbbi_file(kbbi_file):
    """
    Membaca file KBBI dan mengambil sinonimnya.
    """
    results = []

    with open(kbbi_file, "r", encoding="utf-8") as file:
        words = [line.strip() for line in file.readlines()]
    
    for index, word in enumerate(words):
        print(f"Processing {index + 1}/{len(words)}: {word}")
        synonyms = get_synonyms(word)
        if synonyms:
            results.append([word, ", ".join(synonyms)])
        else:
            results.append([word, "Tidak ditemukan"])

        time.sleep(1)  # Beri jeda untuk menghindari rate limit

    return results

def save_to_csv(data, output_file):
    """
    Menyimpan hasil scraping ke file CSV.
    """
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["kata_kunci", "sinonim"])
        writer.writerows(data)

    print(f"Data berhasil disimpan di {output_file}")

# File input dan output
kbbi_file = "list_1.0.0.txt"  # Ganti dengan path file yang sesuai
output_csv = "tesaurus_kbbi.csv"

# Eksekusi proses scraping
scraped_data = process_kbbi_file(kbbi_file)

# Simpan ke CSV
save_to_csv(scraped_data, output_csv)
