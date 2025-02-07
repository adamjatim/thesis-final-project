import pandas as pd
import re
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def clean_and_tokenize(text):
    """
    Membersihkan teks, mempertahankan kata dalam kurung kurawal, dan melakukan stemming.
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
    
    # Lakukan stemming pada kata-kata umum
    stemmed_words = [stemmer.stem(word) for word in words]
    
    # Gabungkan kata-kata khusus dengan kata-kata lainnya
    stemmed_words.extend(special_words)
    
    return stemmed_words

def process_and_count(file_path):
    """
    Membaca file CSV dan menghitung frekuensi kata pada kolom 'terjemahan'.
    """
    df = pd.read_csv(file_path)
    word_counter = Counter()
    
    for text in df['terjemahan']:
        words = clean_and_tokenize(text)
        word_counter.update(words)
    
    return word_counter

def save_to_csv(counter, output_file):
    """
    Menyimpan hasil word count ke file CSV.
    """
    df = pd.DataFrame(counter.items(), columns=['kata', 'frekuensi'])
    df = df.sort_values(by='frekuensi', ascending=False)
    df.to_csv(output_file, index=False)
    print(f"Hasil disimpan di {output_file}")

# File input dan output
quran_file = "quran_data.csv"
hadis_file = "hadis_data.csv"
output_file = "kata_frekuensi_stemmed.csv"

# Proses kedua file
quran_counter = process_and_count(quran_file)
hadis_counter = process_and_count(hadis_file)

# Gabungkan hasil dari Quran dan Hadis
total_counter = quran_counter + hadis_counter

# Simpan hasil
save_to_csv(total_counter, output_file)
