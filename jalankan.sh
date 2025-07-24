#!/bin/bash

echo "========================================"
echo "   SISTEM PENJADWALAN UJIAN SKRIPSI"
echo "========================================"
echo

echo "[1/2] Menjalankan Backend API..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!
cd ..

echo "Menunggu backend siap..."
sleep 8

echo "[2/2] Menjalankan Frontend Website..."
PORT=8000 npm run dev &
FRONTEND_PID=$!

echo "Menunggu frontend siap..."
sleep 10

echo "Membuka browser..."
if command -v open &> /dev/null; then
    open http://localhost:8000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000
else
    echo "Silakan buka browser dan kunjungi: http://localhost:8000"
fi

echo
echo "✅ SISTEM BERHASIL DIJALANKAN!"
echo
echo "🌐 Website: http://localhost:8000"
echo "🔧 API:     http://localhost:8001"
echo
echo "📝 Cara menggunakan:"
echo "   1. Pilih metode MCDM (SAW/TOPSIS)"
echo "   2. Klik 'Buat Jadwal dengan Data Contoh'"
echo "   3. Lihat hasil di tab 'Jadwal Ujian'"
echo
echo "⚠️  JANGAN TUTUP TERMINAL INI"
echo "   (Sistem akan berhenti jika terminal ditutup)"
echo
echo "Tekan Ctrl+C untuk menghentikan sistem"

# Tunggu sampai user menekan Ctrl+C
trap "echo; echo 'Menghentikan sistem...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
