import requests
from bs4 import BeautifulSoup  # type: ignore
import os
from tqdm import tqdm  # type: ignore
from multiprocessing import Pool, Manager
import time
import random
import urllib3
from functools import partial

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL dasar untuk scraping
# base_url = "https://kitabhadis.com/sahih-bukhari/"
# base_url = "https://kitabhadis.com/sahih-muslim/"
# base_url = "https://kitabhadis.com/sunan-tirmizi/"
# base_url = "https://kitabhadis.com/sunan-abu-daud/"
# base_url = "https://kitabhadis.com/sunan-ibnu-majah/"
# base_url = "https://kitabhadis.com/sunan-nasai/"
# base_url = "https://kitabhadis.com/musnad-ahmad/"
# base_url = "https://kitabhadis.com/musnad-darimi/"
base_url = "https://kitabhadis.com/muwatho-malik/"

# Folder untuk menyimpan hasil scraping
# output_folder = "sahih_bukhari_data"
# output_folder = "sahih_muslim_data"
# output_folder = "04_sunan_abu_daud_data"
# output_folder = "05_sunan_ibnu_majah_data"
# output_folder = "06_sunan_nasai_data"
# output_folder = "07_musnad_ahmad_data"
# output_folder = "08_musnad_darimi_data"
output_folder = "09_muwatho_malik_data"

os.makedirs(output_folder, exist_ok=True)

# Looping melalui semua halaman
# total_pages = 7008 # total number of pages Sahih Bukhari
# total_pages = 5362 # total number of pages Sahih Muslim
# total_pages = 3891 # total number of pages Sunan Tirmizi
# total_pages = 4590 # total number of pages Sunan Abu Daud
# total_pages = 4332 # total number of pages Sunan Ibnu Majah
# total_pages = 5662 # total number of pages Sunan nasai
# total_pages = 26363 # total number of pages Musnad Ahmad
# total_pages = 3367 # total number of pages Musnad Darimi
total_pages = 1594 # total number of pages Muwatho Malik

# Fungsi untuk menggantikan elemen kosong dengan spasi
def clean_html_content(element):
    if not element:
        return ""
    # Temukan semua elemen span dengan atribut yang kosong (seperti <b></b>)
    for span in element.find_all("span", style="background:#FF9632;"):
        # Jika span hanya memiliki elemen <b> kosong, gantikan dengan spasi
        if span.find("b") and not span.get_text(strip=True):
            span.replace_with("#")  # Gantikan elemen dengan spasi
    return element.get_text(strip=True)

# Fungsi untuk scraping satu halaman
def scrape_page(page_number, base_url, output_folder):
    url = f"{base_url}{page_number}"
    try:
        response = requests.get(url, timeout=10)  # Set timeout 10 detik
        response.raise_for_status()  # Raise error jika HTTP error terjadi
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Ambil bagian div.card-body
        card_body = soup.find("div", class_="card-body")
        if card_body:
            # Ambil konten teks dari elemen-elemen yang diminta
            subtitle = card_body.find("h6", class_="subtitle")
            ayat = card_body.select_one("div.font-kitab.ayat > div.ada_baris")
            terjemahan = card_body.find("div", class_="alert terjemahan")

            # Ambil teks jika elemen ditemukan dan bersihkan elemen terjemahan
            subtitle_text = subtitle.get_text(strip=True) if subtitle else "Subtitle tidak ditemukan"
            ayat_text = ayat.get_text(strip=True) if ayat else "Ayat tidak ditemukan"
            terjemahan_text = clean_html_content(terjemahan) if terjemahan else "Terjemahan tidak ditemukan"

            # Simpan hasil scraping ke file
            output_path = os.path.join(output_folder, f"page_{page_number}.txt")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(f"Subtitle:\n{subtitle_text}\n\n")
                file.write(f"Ayat:\n{ayat_text}\n\n")
                file.write(f"Terjemahan:\n{terjemahan_text}\n\n")
        else:
            print(f"[{page_number}] Konten tidak ditemukan.")
    except requests.exceptions.RequestException as e:
        print(f"[{page_number}] Error: {e}")

# Fungsi wrapper untuk retry jika terjadi error
def scrape_page_with_retry(page_number, base_url, output_folder, max_retries=3):
    for attempt in range(max_retries):
        try:
            scrape_page(page_number, base_url, output_folder)
            return  # Berhasil, keluar dari fungsi
        except Exception as e:
            print(f"[{page_number}] Retry {attempt + 1}/{max_retries} karena error: {e}")
            time.sleep(random.uniform(1, 3))  # Tunggu sebelum mencoba lagi

# Fungsi untuk mengatur delay antar proses
def scrape_with_delay(page_number, base_url, output_folder):
    scrape_page_with_retry(page_number, base_url, output_folder)
    time.sleep(random.uniform(0.5, 1.5))  # Delay antara permintaan

# Fungsi utama untuk scraping dengan parallel processing
def main():
    page_numbers = list(range(1, total_pages + 1))

    # Menggunakan multiprocessing untuk mempercepat proses
    with Pool(processes=8) as pool:  # Sesuaikan jumlah proses dengan CPU Anda
        func = partial(scrape_with_delay, base_url=base_url, output_folder=output_folder)
        list(tqdm(pool.imap(func, page_numbers), total=total_pages, desc="Scraping Pages"))

if __name__ == "__main__":
    main()