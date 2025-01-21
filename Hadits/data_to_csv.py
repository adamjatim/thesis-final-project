import os
import csv
import re

def filter_hastags(text):
    """Menghapus atau mengganti tanda pagar sesuai aturan."""
    if "##" in text:
        return text.replace("##", " ")
    return text.replace("#", "")

def extract_number_from_filename(filename):
    """Ekstrak angka dari nama file untuk pengurutan manual."""
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

def process_file(filepath):
    """Proses file untuk mengambil nomor hadis, hadis, dan terjemahan."""
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    no_hadis = None
    hadis_lines = []
    terjemahan_lines = []
    is_hadis = False
    is_terjemahan = False

    for line in lines:
        line = line.strip()

        # Deteksi nomor hadis
        if line.startswith("Nombor hadis:"):
            match = re.search(r'Nombor hadis:\s*\((\d+)\)', line)
            if match:
                no_hadis = match.group(1)

        # Deteksi awal hadis
        elif line.startswith("Ayat:"):
            is_hadis = True
            is_terjemahan = False
            continue

        # Deteksi awal terjemahan
        elif line.startswith("Terjemahan:"):
            is_hadis = False
            is_terjemahan = True
            continue

        # Tambahkan baris ke hadis atau terjemahan sesuai konteks
        if is_hadis:
            hadis_lines.append(line)
        elif is_terjemahan:
            terjemahan_lines.append(line)

    # Gabungkan semua baris hadis dan terjemahan
    hadis = " ".join(hadis_lines).strip()
    terjemahan = " ".join(terjemahan_lines).strip()

    # Bersihkan tanda pagar dari terjemahan
    if terjemahan:
        terjemahan = filter_hastags(terjemahan)

    return no_hadis, hadis, terjemahan

# Folder input
# input_folder = "01_sahih_bukhari_data"
# input_folder = "02_sahih_muslim_data"
# input_folder = "03_sunan_tirmizi_data"
# input_folder = "04_sunan_abu_daud_data"
# input_folder = "05_sunan_ibnu_majah_data"
# input_folder = "06_sunan_nasai_data"
# input_folder = "07_musnad_ahmad_data"
# input_folder = "08_musnad_darimi_data"
input_folder = "09_muwatho_malik_data"

# Folder output
output_file = "hadis_output.csv"

# Dapatkan daftar file dan urutkan berdasarkan nomor dalam nama file
files = os.listdir(input_folder)
files_with_numbers = [(file, extract_number_from_filename(file)) for file in files if file.endswith(".txt")]
files_sorted = [file[0] for file in sorted(files_with_numbers, key=lambda x: x[1])]

# Proses semua file dan simpan hasilnya ke dalam CSV
data = []
id_counter = 1

for file in files_sorted:
    filepath = os.path.join(input_folder, file)
    no_hadis, hadis, terjemahan = process_file(filepath)
    if no_hadis and hadis and terjemahan:
        data.append([id_counter, no_hadis, hadis, terjemahan])
        id_counter += 1

# Tulis ke dalam file CSV
with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'no_hadis', 'hadis', 'terjemahan'])  # Header
    writer.writerows(data)

print(f"Proses selesai! Data telah disimpan ke file: {output_file}")