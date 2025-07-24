@echo off
echo ========================================
echo   SISTEM PENJADWALAN UJIAN SKRIPSI
echo ========================================
echo.

echo [1/2] Menjalankan Backend API...
start "Backend Server" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8001"

echo Menunggu backend siap...
timeout /t 8

echo [2/2] Menjalankan Frontend Website...
start "Frontend Server" cmd /k "PORT=8000 npm run dev"

echo Menunggu frontend siap...
timeout /t 10

echo Membuka browser...
start http://localhost:8000

echo.
echo ✅ SISTEM BERHASIL DIJALANKAN!
echo.
echo 🌐 Website: http://localhost:8000
echo 🔧 API:     http://localhost:8001
echo.
echo 📝 Cara menggunakan:
echo    1. Pilih metode MCDM (SAW/TOPSIS)
echo    2. Klik "Buat Jadwal dengan Data Contoh"
echo    3. Lihat hasil di tab "Jadwal Ujian"
echo.
echo ⚠️  JANGAN TUTUP KEDUA TERMINAL YANG TERBUKA
echo    (Terminal Backend dan Frontend harus tetap berjalan)
echo.
pause
