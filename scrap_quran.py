import os
import requests
import re
from bs4 import BeautifulSoup # type: ignore

# Fungsi untuk membersihkan tag HTML
def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text()

# Fungsi untuk membuat folder dan file
def create_folder_and_files(surah_data):
    # Nama folder
    folder_name = f"scraping-quran/surah-{surah_data['nomor']}-{surah_data['nama_latin'].replace(' ', '-').lower()}"
    os.makedirs(folder_name, exist_ok=True)
    
    # Loop melalui ayat-ayat
    for ayat in surah_data["ayat"]:
        file_name = f"{folder_name}/ayat-{ayat['nomor']}.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"no surat :\n{surah_data['nomor']}\n\n")
            file.write(f"nama surat :\n{surah_data['nama_latin']}\n\n")
            file.write(f"nama surat arab :\n{surah_data['nama']}\n\n")
            file.write(f"arti surat :\n{surah_data['arti']}\n\n")
            file.write(f"tempat turun :\n{surah_data['tempat_turun']}\n\n")
            file.write(f"deskripsi :\n{clean_html(surah_data['deskripsi'])}\n\n")
            file.write(f"ayat :\n{ayat['nomor']}\n\n")
            file.write(f"surat :\n{ayat['ar']}\n\n")
            clean_ayat = re.sub(r"<strong>.*?</strong>", "", ayat['tr'])
            file.write(f"latin :\n{clean_html(clean_ayat)}\n\n")
            file.write(f"terjemahan :\n{ayat['idn']}\n\n")

# Fungsi utama
def main():
    base_url = "https://quran-api.santrikoding.com/api/surah/"
    output_folder = "scraping-quran"
    os.makedirs(output_folder, exist_ok=True)

    # Loop untuk setiap surat (1-114)
    for surah_number in range(1, 115):
        try:
            # Ambil data dari API
            response = requests.get(f"{base_url}{surah_number}")
            response.raise_for_status()  # Untuk memastikan tidak ada error HTTP
            surah_data = response.json()
            
            # Jika status true, proses data
            if surah_data["status"]:
                create_folder_and_files(surah_data)
                print(f"Surah {surah_number} - {surah_data['nama_latin']} selesai dibuat.")
            else:
                print(f"Gagal memproses Surah {surah_number}.")
        except Exception as e:
            print(f"Terjadi kesalahan pada Surah {surah_number}: {e}")

if __name__ == "__main__":
    main()
