# 🧮 MathKu – Tutor Matematika AI

Aplikasi chatbot AI interaktif untuk membantu siswa **SD & SMP** belajar matematika langkah demi langkah, menggunakan **Streamlit** dan **Google Gemini AI**.

---

## ✨ Fitur Utama

- 💬 **Chat interaktif** – Siswa bisa menyapa dan bertanya seperti ngobrol biasa
- 📝 **Jawaban bertahap** – AI tidak langsung memberi jawaban, melainkan menjelaskan **langkah demi langkah**
- 🎯 **Fokus SD–SMP** – Mencakup operasi hitung, aljabar, geometri, pecahan, statistika
- ⚡ **Streaming response** – Jawaban muncul kata per kata seperti mengetik
- 🎨 **UI ramah anak** – Desain colorful dan menyenangkan
- 💡 **Quick suggestions** – Tombol contoh soal untuk inspirasi

---

## 🚀 Cara Menjalankan (Lokal)

### 1. Clone repo ini
```bash
git clone https://github.com/USERNAME/mathku-tutor.git
cd mathku-tutor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Dapatkan Gemini API Key
- Buka [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- Buat API Key baru (gratis)

### 4. Buat file secrets
```bash
mkdir -p .streamlit
```

Buat file `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "isi_api_key_kamu_di_sini"
```

> ⚠️ **JANGAN** push file ini ke GitHub! Sudah ada di `.gitignore`.

### 5. Jalankan aplikasi
```bash
streamlit run app.py
```

Buka browser di [http://localhost:8501](http://localhost:8501) 🎉

---

## ☁️ Deploy ke Streamlit Cloud (Gratis)

1. Push semua file ke GitHub (**kecuali** `.streamlit/secrets.toml`)
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app** → pilih repo ini → pilih `app.py`
4. Klik **Advanced settings** → tab **Secrets** → masukkan:
   ```toml
   GEMINI_API_KEY = "isi_api_key_kamu"
   ```
5. Klik **Deploy!** ✅

---

## 📁 Struktur File

```
mathku-tutor/
├── app.py              # Aplikasi utama Streamlit
├── style.css           # Styling kustom
├── requirements.txt    # Dependensi Python
├── .gitignore          # File yang dikecualikan dari Git
├── .streamlit/
│   └── secrets.toml    # API Key (JANGAN di-push!)
└── README.md           # Dokumentasi ini
```

---

## 🎓 Contoh Interaksi

**Siswa:** Halo kak, bisa bantu aku?

**Kak Matica:** Halo! Tentu saja bisa! Aku Kak Matica, siap membantumu belajar matematika... 😊

---

**Siswa:** 2x + 5 = 15, nilai x berapa?

**Kak Matica:**

📌 **Langkah 1:** Kita punya persamaan `2x + 5 = 15`

📌 **Langkah 2:** Pindahkan angka 5 ke kanan dengan cara dikurangi kedua sisi:
`2x = 15 - 5 = 10`

📌 **Langkah 3:** Bagi kedua sisi dengan 2:
`x = 10 ÷ 2`

✅ **Jawaban:** `x = 5`

Apakah kamu sudah paham? Mau coba soal serupa? 😊

---

## 🛠️ Teknologi

| Teknologi | Kegunaan |
|-----------|----------|
| [Streamlit](https://streamlit.io) | Framework web app Python |
| [Google Gemini AI](https://ai.google.dev) | Model AI untuk penjelasan |
| CSS Custom | Styling tampilan |

---

## 📄 Lisensi

MIT License – bebas digunakan untuk keperluan pendidikan.
