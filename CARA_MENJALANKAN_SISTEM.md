# 🚀 CARA MENJALANKAN SISTEM SETELAH LAPTOP DIHIDUPKAN KEMBALI

## 📋 Langkah-Langkah Mudah

### **1. Buka Terminal/Command Prompt**
- **Windows**: Tekan `Win + R`, ketik `cmd`, tekan Enter
- **Mac**: Tekan `Cmd + Space`, ketik `Terminal`, tekan Enter
- **Linux**: Tekan `Ctrl + Alt + T`

### **2. Masuk ke Folder Proyek**
```bash
cd /path/to/your/project
# Contoh: cd C:\Users\YourName\Desktop\sistem-penjadwalan
# Atau: cd /home/username/sistem-penjadwalan
```

### **3. Jalankan Backend (API Server)**
Buka terminal pertama dan jalankan:
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

**Tunggu sampai muncul pesan:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### **4. Jalankan Frontend (Website)**
Buka terminal kedua (biarkan terminal pertama tetap berjalan) dan jalankan:
```bash
PORT=8000 npm run dev
```

**Tunggu sampai muncul pesan:**
```
✓ Ready in 787ms
- Local:        http://localhost:8000
```

### **5. Buka Browser**
- Buka browser (Chrome, Firefox, Safari, dll)
- Ketik di address bar: `http://localhost:8000`
- Tekan Enter

## 🔧 **Troubleshooting - Jika Ada Masalah**

### **Masalah 1: Port sudah digunakan**
Jika muncul error "address already in use":
```bash
# Untuk port 8001 (Backend)
fuser -k 8001/tcp

# Untuk port 8000 (Frontend)  
fuser -k 8000/tcp
```

### **Masalah 2: Python tidak ditemukan**
```bash
# Coba dengan python3
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### **Masalah 3: npm tidak ditemukan**
Pastikan Node.js sudah terinstall:
- Download dari: https://nodejs.org
- Install, lalu restart terminal

### **Masalah 4: Dependencies hilang**
```bash
# Install ulang dependencies Python
cd backend
pip install -r requirements.txt

# Install ulang dependencies Node.js
cd ..
npm install
```

## 📱 **Cara Cepat - Script Otomatis**

### **Untuk Windows - Buat file `jalankan.bat`:**
```batch
@echo off
echo Menjalankan Sistem Penjadwalan Ujian Skripsi...
echo.

echo [1/2] Menjalankan Backend...
start cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8001"

timeout /t 5

echo [2/2] Menjalankan Frontend...
start cmd /k "PORT=8000 npm run dev"

timeout /t 5

echo Membuka browser...
start http://localhost:8000

echo.
echo ✅ Sistem berhasil dijalankan!
echo Backend: http://localhost:8001
echo Frontend: http://localhost:8000
pause
```

### **Untuk Mac/Linux - Buat file `jalankan.sh`:**
```bash
#!/bin/bash
echo "🚀 Menjalankan Sistem Penjadwalan Ujian Skripsi..."
echo

echo "[1/2] Menjalankan Backend..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

echo "Menunggu backend siap..."
sleep 5

echo "[2/2] Menjalankan Frontend..."
cd ..
PORT=8000 npm run dev &
FRONTEND_PID=$!

echo "Menunggu frontend siap..."
sleep 5

echo "Membuka browser..."
if command -v open &> /dev/null; then
    open http://localhost:8000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000
fi

echo
echo "✅ Sistem berhasil dijalankan!"
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:8000"
echo
echo "Tekan Ctrl+C untuk menghentikan sistem"

# Tunggu sampai user menekan Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
```

**Cara menggunakan script:**
```bash
# Buat file executable (Mac/Linux)
chmod +x jalankan.sh
./jalankan.sh

# Atau double-click file jalankan.bat (Windows)
```

## 🎯 **Ringkasan Singkat**

**Yang Perlu Diingat:**
1. **2 Terminal** - Satu untuk backend, satu untuk frontend
2. **2 Perintah**:
   - Backend: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8001`
   - Frontend: `PORT=8000 npm run dev`
3. **1 URL**: `http://localhost:8000`

## 📞 **Bantuan Cepat**

**Jika sistem tidak jalan:**
1. Pastikan kedua terminal masih berjalan
2. Cek apakah ada pesan error di terminal
3. Restart kedua perintah jika perlu
4. Refresh browser di `http://localhost:8000`

**Untuk menghentikan sistem:**
- Tekan `Ctrl+C` di kedua terminal
- Atau tutup terminal

---

**💡 Tips:** Bookmark `http://localhost:8000` di browser agar mudah diakses!
