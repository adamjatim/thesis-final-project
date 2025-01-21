import csv
import re
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory # type: ignore

# Inisialisasi Stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def clean_and_tokenize(text):
    """
    Membersihkan teks dan memecah menjadi kata-kata, 
    termasuk mempertahankan kata khusus dalam kurung kurawal [].
    """
    # Cari kata-kata khusus dalam kurung kurawal
    special_words = re.findall(r"\[(.*?)\]", text)
    
    # Hapus kurung kurawal dari teks utama
    text = re.sub(r"\[.*?\]", "", text)
    
    # Bersihkan teks lainnya
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    
    # Pecah menjadi kata-kata
    words = text.split()
    
    # Gabungkan kata-kata khusus dengan kata-kata lainnya
    words.extend(special_words)
    
    return words

def process_file(file_path, column_name):
    """
    Membaca file CSV dan menghitung kata-kata pada kolom tertentu.
    """
    word_counter = Counter()
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if column_name in row and row[column_name]:
                words = clean_and_tokenize(row[column_name])
                # Lakukan stemming untuk setiap kata
                stemmed_words = [stemmer.stem(word) for word in words]
                word_counter.update(stemmed_words)
    return word_counter

def merge_and_rank(word_counts_list):
    """
    Menggabungkan hasil dari beberapa Counter dan mengurutkan berdasarkan frekuensi.
    """
    total_counter = Counter()
    for word_counter in word_counts_list:
        total_counter.update(word_counter)
    return total_counter.most_common()

def save_to_csv(data, output_file):
    """
    Menyimpan data ke file CSV.
    """
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["kata", "frekuensi"])
        writer.writerows(data)

# File input dan output
quran_file = "quran_data.csv"
hadis_file = "hadis_data.csv"
output_file = "kata_frekuensi_stemmed.csv"

# Kolom yang akan diproses
column_name = "terjemahan"

# Proses kedua file
quran_word_counts = process_file(quran_file, column_name)
hadis_word_counts = process_file(hadis_file, column_name)

# Gabungkan dan urutkan hasilnya
ranked_words = merge_and_rank([quran_word_counts, hadis_word_counts])

# Simpan ke file CSV
save_to_csv(ranked_words, output_file)

print(f"Data berhasil disimpan di {output_file}")
