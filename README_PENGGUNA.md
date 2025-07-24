# 🎓 Sistem Pendukung Keputusan Penjadwalan Ujian Skripsi

## 🚀 Cara Menjalankan Sistem (MUDAH!)

### **Opsi 1: Otomatis (Direkomendasikan)**

#### **Windows:**
1. Double-click file `jalankan.bat`
2. Tunggu sampai browser terbuka otomatis
3. Sistem siap digunakan!

#### **Mac/Linux:**
1. Buka Terminal
2. Ketik: `./jalankan.sh`
3. Tekan Enter
4. Tunggu sampai browser terbuka otomatis
5. Sistem siap digunakan!

### **Opsi 2: Manual**

1. **Buka 2 Terminal/Command Prompt**

2. **Terminal 1 (Backend):**
   ```bash
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8001
   ```

3. **Terminal 2 (Frontend):**
   ```bash
   PORT=8000 npm run dev
   ```

4. **Buka Browser:**
   - Kunjungi: `http://localhost:8000`

## 📱 Cara Menggunakan Sistem

### **Langkah 1: Pilih Metode**
- Pilih metode MCDM: **SAW** (direkomendasikan) atau **TOPSIS**

### **Langkah 2: Buat Jadwal**
- Klik tombol **"Buat Jadwal dengan Data Contoh"**
- Sistem akan memproses secara otomatis

### **Langkah 3: Lihat Hasil**
- Hasil jadwal akan muncul otomatis
- Atau klik tab **"Jadwal Ujian"** untuk melihat detail lengkap

## 📊 Fitur Sistem

✅ **5 Mahasiswa** dengan berbagai bidang skripsi:
- Machine Learning & AI
- Web Development  
- Blockchain & Security
- Big Data Analytics
- Game Development

✅ **5 Penguji** dengan keahlian beragam:
- Professor dan Associate Professor
- Berbagai spesialisasi akademik

✅ **4 Ruangan** dengan fasilitas lengkap:
- Ruang Sidang A, B, C
- Ruang Seminar

✅ **6 Slot Waktu** (Senin-Selasa):
- Pagi: 08:00-10:00, 10:30-12:30
- Siang: 13:30-15:30

## 🎯 Hasil yang Dihasilkan

Sistem akan menghasilkan jadwal optimal dengan informasi:
- **Nama Mahasiswa** dan NIM
- **Waktu Ujian** (Hari, Jam)
- **Ruangan** yang dialokasikan
- **3 Penguji** yang sesuai keahlian
- **Skor Kualitas** penjadwalan

## 🔧 Troubleshooting

### **Masalah: Port sudah digunakan**
```bash
fuser -k 8000/tcp
fuser -k 8001/tcp
```

### **Masalah: Python tidak ditemukan**
- Install Python dari: https://python.org
- Atau coba: `python3` instead of `python`

### **Masalah: npm tidak ditemukan**
- Install Node.js dari: https://nodejs.org

### **Masalah: Dependencies hilang**
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Install Node.js dependencies  
cd ..
npm install
```

## 📞 Bantuan

**Jika sistem tidak berjalan:**
1. Pastikan kedua terminal tetap terbuka
2. Refresh browser di `http://localhost:8000`
3. Cek pesan error di terminal
4. Restart sistem jika perlu

**Untuk menghentikan sistem:**
- Tekan `Ctrl+C` di terminal
- Atau tutup terminal

---

## 🏆 Tentang Sistem

Sistem ini menggunakan metode **Multi-Criteria Decision Making (MCDM)**:

- **SAW**: Simple Additive Weighting
- **TOPSIS**: Technique for Order Preference by Similarity to Ideal Solution  
- **AHP**: Analytic Hierarchy Process

**Kriteria Evaluasi:**
- Expertise Match (30%)
- Competency Score (25%)
- Availability Score (20%)
- Workload (15%)
- Experience Years (10%)

**Dikembangkan untuk membantu penjadwalan ujian skripsi yang optimal dan efisien.**

---

💡 **Tips:** Bookmark `http://localhost:8000` untuk akses cepat!
