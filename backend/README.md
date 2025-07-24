# Sistem Pendukung Keputusan Penjadwalan Ujian Skripsi

## Deskripsi

Sistem Pendukung Keputusan (SPK) untuk penjadwalan ujian skripsi menggunakan metode Multi-Criteria Decision Making (MCDM). Sistem ini mengimplementasikan beberapa algoritma MCDM untuk membantu dalam pengambilan keputusan optimal dalam penjadwalan ujian skripsi.

### Metode MCDM yang Diimplementasikan

1. **AHP (Analytic Hierarchy Process)**
   - Digunakan untuk menghitung bobot kriteria melalui perbandingan berpasangan
   - Mengukur konsistensi matriks perbandingan
   - Cocok untuk pengambilan keputusan hierarkis

2. **SAW (Simple Additive Weighting)**
   - Metode penjumlahan terbobot sederhana
   - Mudah dipahami dan diimplementasikan
   - Cocok untuk masalah dengan kriteria yang jelas

3. **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)**
   - Berdasarkan konsep solusi ideal positif dan negatif
   - Memberikan ranking yang lebih robust
   - Cocok untuk masalah dengan banyak alternatif

## Fitur Utama

- ✅ **Evaluasi Penguji**: Menilai kesesuaian penguji untuk mahasiswa berdasarkan multiple criteria
- ✅ **Penjadwalan Otomatis**: Menghasilkan jadwal ujian optimal dengan mempertimbangkan constraints
- ✅ **Analisis Kualitas**: Menganalisis kualitas jadwal yang dihasilkan
- ✅ **API RESTful**: Interface API untuk integrasi dengan frontend
- ✅ **Validasi Data**: Validasi input menggunakan Pydantic
- ✅ **Testing**: Unit tests untuk semua komponen utama

## Struktur Proyek

```
backend/
├── requirements.txt          # Dependencies Python
├── models.py                # Data models (Pydantic)
├── mcdm_methods.py          # Implementasi metode MCDM
├── scheduling_engine.py     # Engine penjadwalan utama
├── main.py                  # FastAPI application
├── sample_data.py           # Data contoh untuk testing
├── demo.py                  # Script demo dan contoh penggunaan
├── test_scheduling.py       # Unit tests
└── README.md               # Dokumentasi ini
```

## Instalasi dan Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Jalankan Demo

```bash
python demo.py
```

### 3. Jalankan API Server

```bash
python -m uvicorn main:app --reload --port 8001
```

### 4. Jalankan Tests

```bash
pytest test_scheduling.py -v
```

## Penggunaan API

### Endpoints Utama

#### 1. Generate Schedule
```http
POST /schedule
Content-Type: application/json

{
  "students": [...],
  "examiners": [...],
  "rooms": [...],
  "timeslots": [...],
  "exam_sessions": [...],
  "method": "SAW"
}
```

#### 2. Calculate AHP Weights
```http
POST /ahp-weights
Content-Type: application/json

{
  "ahp_matrix": {
    "criteria": ["expertise", "experience", "workload"],
    "matrix": [
      [1, 2, 3],
      [0.5, 1, 2],
      [0.33, 0.5, 1]
    ]
  }
}
```

#### 3. Evaluate Examiners
```http
POST /evaluate-examiners
Content-Type: application/json

{
  "student": {...},
  "examiners": [...],
  "timeslot_id": 1,
  "method": "SAW"
}
```

#### 4. Get Available Methods
```http
GET /methods
```

#### 5. Get Default Criteria
```http
GET /criteria
```

## Kriteria Evaluasi Default

1. **Expertise Match (30%)** - Kesesuaian keahlian penguji dengan bidang skripsi
2. **Competency Score (25%)** - Tingkat kompetensi penguji
3. **Availability Score (20%)** - Fleksibilitas ketersediaan waktu
4. **Workload (15%)** - Beban kerja saat ini (cost criteria)
5. **Experience Years (10%)** - Pengalaman menguji

## Contoh Penggunaan

### 1. Menggunakan Python Script

```python
from sample_data import get_complete_sample_data
from scheduling_engine import ExamSchedulingDSS

# Load sample data
data = get_complete_sample_data()
dss = ExamSchedulingDSS()

# Generate schedule
solution = dss.generate_schedule(
    students=data['students'],
    examiners=data['examiners'],
    rooms=data['rooms'],
    timeslots=data['timeslots'],
    exam_sessions=data['exam_sessions'],
    method="SAW"
)

print(f"Scheduled exams: {len(solution.schedule)}")
print(f"Success rate: {len(solution.schedule) / len(data['exam_sessions']):.1%}")
```

### 2. Menggunakan API dengan curl

```bash
# Get available methods
curl -X GET http://localhost:8001/methods

# Get default criteria
curl -X GET http://localhost:8001/criteria

# Generate schedule (requires full JSON payload)
curl -X POST http://localhost:8001/schedule \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

## Algoritma dan Metodologi

### 1. Proses Evaluasi Penguji

1. **Perhitungan Expertise Match**: Mencocokkan kata kunci bidang skripsi dengan keahlian penguji
2. **Normalisasi Kriteria**: Mengubah semua kriteria ke skala 0-1
3. **Aplikasi MCDM**: Menggunakan SAW atau TOPSIS untuk ranking
4. **Seleksi Optimal**: Memilih penguji terbaik dengan mempertimbangkan supervisor

### 2. Proses Penjadwalan

1. **Constraint Checking**: Memastikan tidak ada konflik ruangan dan penguji
2. **Optimization**: Memaksimalkan skor total kepuasan
3. **Priority Handling**: Memprioritaskan ujian berdasarkan priority score
4. **Resource Management**: Mengelola beban kerja penguji secara dinamis

### 3. Analisis Kualitas

- **Success Rate**: Persentase ujian yang berhasil dijadwalkan
- **Average Score**: Rata-rata skor kepuasan
- **Score Distribution**: Distribusi kualitas jadwal
- **Resource Utilization**: Pemanfaatan sumber daya

## Konfigurasi dan Customization

### 1. Mengubah Bobot Kriteria

```python
from models import Criteria, CriteriaType

custom_criteria = [
    Criteria(id=1, name="expertise_match", weight=0.40, type=CriteriaType.BENEFIT),
    Criteria(id=2, name="competency_score", weight=0.30, type=CriteriaType.BENEFIT),
    # ... kriteria lainnya
]
```

### 2. Menambah Kriteria Baru

```python
# Dalam scheduling_engine.py, method evaluate_examiner_for_student
def evaluate_examiner_for_student(self, examiner, student, timeslot_id):
    # Tambahkan perhitungan kriteria baru
    new_criterion_score = self.calculate_new_criterion(examiner, student)
    # ...
```

### 3. Menggunakan Metode MCDM Lain

Sistem dapat diperluas untuk menambah metode MCDM lain seperti:
- ELECTRE
- PROMETHEE
- VIKOR
- Grey Relational Analysis

## Troubleshooting

### Common Issues

1. **Import Error**: Pastikan semua dependencies terinstall
   ```bash
   pip install -r requirements.txt
   ```

2. **No Feasible Schedule**: Periksa constraints dan availability
   - Tambah penguji atau slot waktu
   - Kurangi required_examiners per session

3. **Low Quality Scores**: 
   - Sesuaikan bobot kriteria
   - Periksa data input quality

4. **API Connection Error**:
   ```bash
   # Pastikan server berjalan di port yang benar
   python -m uvicorn main:app --reload --port 8001
   ```

## Kontribusi

Untuk berkontribusi pada proyek ini:

1. Fork repository
2. Buat feature branch
3. Implementasikan perubahan
4. Tambahkan tests
5. Submit pull request

## Lisensi

Proyek ini menggunakan lisensi MIT. Lihat file LICENSE untuk detail.

## Kontak

Untuk pertanyaan atau dukungan:
- Email: support@university.edu
- GitHub Issues: [Link to issues]

---

**Catatan**: Sistem ini dikembangkan untuk keperluan akademis dan dapat disesuaikan dengan kebutuhan institusi masing-masing.
