import os
import re
import csv

def debug_file_reading(root_folder):
    for folder in sorted(os.listdir(root_folder), key=extract_number):
        folder_path = os.path.join(root_folder, folder)

        if os.path.isdir(folder_path):
            for file in sorted(os.listdir(folder_path), key=extract_number):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path) and file.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = [line.strip() for line in f.readlines() if line.strip()]
                        print(f"=== {file} ===")
                        for line in lines:
                            print(line)
                        print("\n")


# Fungsi untuk mengekstrak angka dari nama file atau folder
def extract_number(name):
    match = re.search(r"(\d+)", name)
    return int(match.group()) if match else 0

# Fungsi utama untuk menggabungkan file ke dalam satu CSV
def merge_files_to_csv(root_folder, output_csv):
    data = []
    id_surat = 1

    # Iterasi melalui folder surah secara numerik
    for folder in sorted(os.listdir(root_folder), key=extract_number):
        folder_path = os.path.join(root_folder, folder)

        if os.path.isdir(folder_path):  # Pastikan ini adalah folder
            no_surat = extract_number(folder)
            nama_surat_parts = folder.split("-")
            nama_surat = "-".join(nama_surat_parts[2:]).replace("-", " ").title()
            nama_surat_arab = ""
            arti_surat = ""
            tempat_turun = ""
            deskripsi = ""

            # Iterasi melalui file ayat secara numerik
            for file in sorted(os.listdir(folder_path), key=extract_number):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path) and file.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = [line.strip() for line in f.readlines() if line.strip()]  # Abaikan baris kosong

                        # Parsing konten file berdasarkan format yang diberikan
                        ayat = ""
                        surat = ""
                        latin = ""
                        terjemahan = ""

                        # for line in lines:
                        #     if line.startswith("no surat :"):
                        #         no_surat = line.split(":", 1)[1].strip()
                        #     elif line.startswith("nama surat arab :"):
                        #         nama_surat_arab = line.split(":", 1)[1].strip()
                        #     elif line.startswith("arti surat :"):
                        #         arti_surat = line.split(":", 1)[1].strip()
                        #     elif line.startswith("tempat turun :"):
                        #         tempat_turun = line.split(":", 1)[1].strip()
                        #     elif line.startswith("deskripsi :"):
                        #         deskripsi = line.split(":", 1)[1].strip()
                        #     elif line.startswith("ayat :"):
                        #         ayat = line.split(":", 1)[1].strip()
                        #     elif line.startswith("surat :"):
                        #         surat = line.split(":", 1)[1].strip()
                        #     elif line.startswith("latin :"):
                        #         latin = line.split(":", 1)[1].strip()
                        #     elif line.startswith("terjemahan :"):
                        #         terjemahan = line.split(":", 1)[1].strip()

                        for line in lines:
                          key, _, value = line.partition(":")
                          key = key.strip().lower()
                          value = value.strip()
                          if key == "no surat":
                              no_surat = value
                          elif key == "nama surat arab":
                              nama_surat_arab = value
                          elif key == "arti surat":
                              arti_surat = value
                          elif key == "tempat turun":
                              tempat_turun = value
                          elif key == "deskripsi":
                              deskripsi = value
                          elif key == "ayat":
                              ayat = value
                          elif key == "surat":
                              surat = value
                          elif key == "latin":
                              latin = value
                          elif key == "terjemahan":
                              terjemahan = value

                        # Tambahkan ke data
                        data.append([
                            id_surat, no_surat, nama_surat, nama_surat_arab, arti_surat,
                            ayat, surat, latin, terjemahan, tempat_turun, deskripsi
                        ])
                        print(f"Appended Data: {data[-1]}")
                        id_surat += 1

    # Tulis ke file CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id_surat", "no_surat", "nama_surat", "nama_surat_arab", "arti_surat",
                        "ayat", "surat", "latin", "terjemahan", "tempat_turun", "deskripsi"])
        writer.writerows(data)

    print(f"Data berhasil disimpan ke {output_csv}")
    print("Final Data to Write:", data)


# Jalankan fungsi
merge_files_to_csv("scraping-quran", "quran_combined.csv")

debug_file_reading("scraping-quran")
