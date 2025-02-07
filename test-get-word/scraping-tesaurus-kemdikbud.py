from playwright.sync_api import sync_playwright
import csv
import time

# URL dasar untuk Tesaurus Kemdikbud
BASE_URL = "https://tesaurus.kemdikbud.go.id/tematis/lema/"

def get_synonyms(word):
    """
    Mengambil sinonim dari Tesaurus Kemdikbud menggunakan Playwright.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE_URL + word)
        time.sleep(2)

        synonym_list = []

        # Cari elemen dengan class "one-par-content"
        elements = page.locator(".one-par-content").all()
        for element in elements:
            words = element.locator("a.lemma-ordinary").all_inner_texts()
            synonym_list.extend(words)

        browser.close()
    
    return list(set(synonym_list))  # Hapus duplikasi

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

        time.sleep(1)  # Jeda agar tidak diblokir

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
kbbi_file = "list_1.0.0.txt"
output_csv = "tesaurus_kbbi.csv"

# Eksekusi proses scraping
scraped_data = process_kbbi_file(kbbi_file)

# Simpan ke CSV
save_to_csv(scraped_data, output_csv)