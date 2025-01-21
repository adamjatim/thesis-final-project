import csv

# Fungsi untuk menghapus semua tanda pagar
def hapus_tanda_pagar(text):
    return text.replace("#", "")

# Membaca CSV, membersihkan, dan menyimpan ulang
def bersihkan_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Bersihkan setiap baris
        for row in reader:
            cleaned_row = [hapus_tanda_pagar(cell) for cell in row]
            writer.writerow(cleaned_row)

# Nama file input dan output
input_file = 'hadis_output.csv'
# output_file = '01_sahih_bukhari.csv'
# output_file = '02_sahih_muslim.csv'
# output_file = '03_sunan_tirmizi.csv'
# output_file = '04_sunan_abu_daud.csv'
# output_file = '05_sunan_ibnu_majah.csv'
# output_file = '06_sunan_nasai_data.csv'
# output_file = '07_musnad_ahmad_data.csv'
# output_file = '08_musnad_darimi_data.csv'
output_file = '09_muwatho_malik_data.csv'

# Memproses file
bersihkan_csv(input_file, output_file)
print("Proses pembersihan selesai, hasil disimpan di", output_file)
