import os
import re
import csv

def extract_number(file_name):
    """
    Mengekstrak angka dari nama file, misal ayat_1.txt -> 1.
    """
    match = re.search(r"(\d+)", file_name)
    return int(match.group()) if match else 0

def parse_file(file_path):
    """
    Memparsing file teks menjadi dictionary.
    """
    data_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]  # Hilangkan baris kosong

    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line:  # Jika baris mengandung titik dua
            key, _, value = line.partition(":")
            key = key.strip().lower()
            value = value.strip()
            if not value and i + 1 < len(lines):  # Jika value kosong, ambil dari baris berikutnya
                i += 1
                value = lines[i].strip()
            data_dict[key] = value  # Simpan dalam dictionary
        i += 1

    return d
    ata_dict


def process_folder(base_folder, output_csv):
    """
    Memproses semua file dalam folder secara rekursif dan menyimpannya ke file CSV.
    """
    rows = []
    id_surat = 1

    # Dapatkan daftar folder surat yang terurut secara numerik
    surat_folders = sorted(
        [folder for folder in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, folder))],
        key=extract_number
    )

    for surat_folder in surat_folders:
        surat_path = os.path.join(base_folder, surat_folder)
        
        # Dapatkan daftar file ayat yang terurut secara numerik
        ayat_files = sorted(
            [file for file in os.listdir(surat_path) if file.endswith('.txt')],
            key=extract_number
        )

        for ayat_file in ayat_files:
            file_path = os.path.join(surat_path, ayat_file)
            print(f"Reading file: {file_path}")

            # Parse file
            data = parse_file(file_path)

            # Isi data ke dalam variabel
            no_surat = data.get("no surat", "")
            nama_surat = data.get("nama surat", "")
            nama_surat_arab = data.get("nama surat arab", "")
            arti_surat = data.get("arti surat", "")
            tempat_turun = data.get("tempat turun", "")
            deskripsi = data.get("deskripsi", "")
            ayat = data.get("ayat", "")
            surat = data.get("surat", "")
            latin = data.get("latin", "")
            terjemahan = data.get("terjemahan", "")

            # Jika data minimal lengkap, masukkan ke dalam list
            if no_surat and nama_surat and ayat and surat:
                rows.append([
                    id_surat, no_surat, nama_surat, nama_surat_arab, arti_surat,
                    ayat, surat, latin, terjemahan, tempat_turun, deskripsi
                ])
                id_surat += 1
            else:
                print(f"Skipping incomplete data: {data}")

    # Tulis ke CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "id_surat", "no_surat", "nama_surat", "nama_surat_arab", "arti_surat",
            "ayat", "surat", "latin", "terjemahan", "tempat_turun", "deskripsi"
        ])
        writer.writerows(rows)
    print(f"Data successfully written to {output_csv}")

# Jalankan fungsi
base_folder = "scraping-quran"
output_csv = "quran_data.csv"
process_folder(base_folder, output_csv)
