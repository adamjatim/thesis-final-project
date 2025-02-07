import json
import urllib.parse

# Baca daftar kata dari file list_1.0.0.txt
def read_words_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        words = [line.strip() for line in file.readlines() if line.strip()]
    return words

# Fungsi untuk mengubah teks menjadi URL-encoded

def encode_url(word):
    word = word.replace(" ", "%2B")  # Ganti spasi dengan %2B
    return urllib.parse.quote(word, safe="%2B")  # Encode karakter non-ASCII

# Buat struktur JSON
def generate_json(words, output_filename):
    sitemap = {
        "_id": "tesaurus_kemdikbud",
        "startUrl": [f"https://tesaurus.kemdikbud.go.id/tematis/lema/{encode_url(word)}" for word in words],
        "selectors": [
            {
                "id":"get",
                "multiple":True, # type: ignore
                "parentSelectors":["_root"],
                "regex":"",
                "selector":"#search > div.search-result-area > div.note-resultintro > b, div.result-postag, .article-label a, .one-par-content",
                "type":"SelectorText"
            }
        ]
    }

    # Simpan ke file JSON
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(sitemap, json_file, indent=2, ensure_ascii=False)
    
    print(f"File JSON berhasil dibuat: {output_filename}")

# Jalankan fungsi
input_file = "list_1.0.0.txt"  # Nama file yang berisi daftar kata
output_file = "tesaurus_sitemap_001.json"  # Nama output JSON

words = read_words_from_file(input_file)
generate_json(words, output_file)
