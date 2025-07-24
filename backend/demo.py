"""
Demo script untuk menjalankan Sistem Pendukung Keputusan Penjadwalan Ujian Skripsi
"""

import json
from typing import Dict, Any
from sample_data import get_complete_sample_data
from scheduling_engine import ExamSchedulingDSS
from mcdm_methods import MCDMEngine
from models import AHPMatrix

def print_separator(title: str):
    """Print formatted separator"""
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60)

def print_schedule_result(solution, data):
    """Print formatted schedule results"""
    print(f"\nMetode yang digunakan: {solution.method_used}")
    print(f"Total kepuasan: {solution.total_satisfaction:.3f}")
    print(f"Ujian terjadwal: {len(solution.schedule)}")
    print(f"Ujian tidak dapat dijadwalkan: {len(solution.infeasible_exams)}")
    
    if solution.schedule:
        print("\n--- JADWAL UJIAN YANG DIHASILKAN ---")
        
        # Create lookup dictionaries
        student_lookup = {s.id: s for s in data['students']}
        examiner_lookup = {e.id: e for e in data['examiners']}
        room_lookup = {r.id: r for r in data['rooms']}
        timeslot_lookup = {t.id: t for t in data['timeslots']}
        
        for i, exam in enumerate(solution.schedule, 1):
            student = student_lookup.get(exam.exam_id)  # exam_id corresponds to student_id in this demo
            room = room_lookup.get(exam.room_id)
            timeslot = timeslot_lookup.get(exam.timeslot_id)
            
            print(f"\n{i}. {exam.student_name}")
            if student:
                print(f"   NIM: {student.nim}")
                print(f"   Judul: {student.thesis_title}")
            
            if timeslot:
                print(f"   Waktu: {timeslot.day}, {timeslot.start_time}-{timeslot.end_time}")
            
            if room:
                print(f"   Ruangan: {room.name} ({room.location})")
            
            print(f"   Penguji:")
            for examiner_id in exam.assigned_examiners:
                examiner = examiner_lookup.get(examiner_id)
                if examiner:
                    print(f"     - {examiner.name}")
            
            print(f"   Skor Total: {exam.total_score:.3f}")
    
    if solution.infeasible_exams:
        print(f"\n--- UJIAN YANG TIDAK DAPAT DIJADWALKAN ---")
        for exam_id in solution.infeasible_exams:
            student = next((s for s in data['students'] if s.id == exam_id), None)
            if student:
                print(f"- {student.name} ({student.nim})")

def demo_ahp_calculation():
    """Demo perhitungan bobot AHP"""
    print_separator("DEMO PERHITUNGAN BOBOT AHP")
    
    print("Contoh matriks perbandingan berpasangan untuk 5 kriteria:")
    print("1. Expertise Match")
    print("2. Competency Score") 
    print("3. Availability Score")
    print("4. Workload")
    print("5. Experience Years")
    
    # Contoh matriks perbandingan berpasangan 5x5
    ahp_matrix = AHPMatrix(
        criteria=["expertise_match", "competency_score", "availability_score", "workload", "experience_years"],
        matrix=[
            [1,    2,    3,    4,    5],      # expertise_match
            [0.5,  1,    2,    3,    4],      # competency_score
            [0.33, 0.5,  1,    2,    3],      # availability_score
            [0.25, 0.33, 0.5,  1,    2],      # workload
            [0.2,  0.25, 0.33, 0.5,  1]       # experience_years
        ]
    )
    
    mcdm_engine = MCDMEngine()
    
    try:
        weights, consistency_ratio, is_consistent = mcdm_engine.calculate_ahp_weights(ahp_matrix)
        
        print(f"\nHasil perhitungan AHP:")
        print(f"Consistency Ratio: {consistency_ratio:.4f}")
        print(f"Konsisten: {'Ya' if is_consistent else 'Tidak'}")
        
        print(f"\nBobot kriteria:")
        for i, (criterion, weight) in enumerate(zip(ahp_matrix.criteria, weights)):
            print(f"{i+1}. {criterion}: {weight:.4f} ({weight*100:.1f}%)")
        
        return weights if is_consistent else None
        
    except Exception as e:
        print(f"Error dalam perhitungan AHP: {e}")
        return None

def demo_examiner_evaluation():
    """Demo evaluasi penguji untuk mahasiswa"""
    print_separator("DEMO EVALUASI PENGUJI")
    
    data = get_complete_sample_data()
    dss = ExamSchedulingDSS()
    
    # Pilih mahasiswa pertama
    student = data['students'][0]
    timeslot_id = 1
    
    print(f"Evaluasi penguji untuk mahasiswa: {student.name}")
    print(f"Bidang skripsi: {student.thesis_field}")
    print(f"Slot waktu: {timeslot_id}")
    
    # Evaluasi dengan metode SAW
    print(f"\n--- MENGGUNAKAN METODE SAW ---")
    selected_examiners_saw = dss.select_best_examiners(
        student, data['examiners'], timeslot_id, 
        required_count=3, method="SAW"
    )
    
    print(f"Penguji terpilih (SAW):")
    for i, (examiner, score) in enumerate(selected_examiners_saw, 1):
        print(f"{i}. {examiner.name} - Skor: {score:.3f}")
        print(f"   Keahlian: {', '.join(examiner.expertise[:2])}")
        print(f"   Pengalaman: {examiner.experience_years} tahun")
        print(f"   Beban kerja: {examiner.workload}")
    
    # Evaluasi dengan metode TOPSIS
    print(f"\n--- MENGGUNAKAN METODE TOPSIS ---")
    selected_examiners_topsis = dss.select_best_examiners(
        student, data['examiners'], timeslot_id, 
        required_count=3, method="TOPSIS"
    )
    
    print(f"Penguji terpilih (TOPSIS):")
    for i, (examiner, score) in enumerate(selected_examiners_topsis, 1):
        print(f"{i}. {examiner.name} - Skor: {score:.3f}")
        print(f"   Keahlian: {', '.join(examiner.expertise[:2])}")
        print(f"   Pengalaman: {examiner.experience_years} tahun")
        print(f"   Beban kerja: {examiner.workload}")

def demo_complete_scheduling():
    """Demo penjadwalan lengkap"""
    print_separator("DEMO PENJADWALAN LENGKAP")
    
    data = get_complete_sample_data()
    dss = ExamSchedulingDSS()
    
    print("Menjalankan algoritma penjadwalan...")
    print(f"Data input:")
    print(f"- Mahasiswa: {len(data['students'])}")
    print(f"- Penguji: {len(data['examiners'])}")
    print(f"- Ruangan: {len(data['rooms'])}")
    print(f"- Slot waktu: {len(data['timeslots'])}")
    print(f"- Sesi ujian: {len(data['exam_sessions'])}")
    
    # Test dengan metode SAW
    print(f"\n--- HASIL DENGAN METODE SAW ---")
    solution_saw = dss.generate_schedule(
        students=data['students'],
        examiners=data['examiners'],
        rooms=data['rooms'],
        timeslots=data['timeslots'],
        exam_sessions=data['exam_sessions'],
        criteria=data['criteria'],
        method="SAW"
    )
    
    print_schedule_result(solution_saw, data)
    
    # Test dengan metode TOPSIS
    print(f"\n--- HASIL DENGAN METODE TOPSIS ---")
    solution_topsis = dss.generate_schedule(
        students=data['students'],
        examiners=data['examiners'],
        rooms=data['rooms'],
        timeslots=data['timeslots'],
        exam_sessions=data['exam_sessions'],
        criteria=data['criteria'],
        method="TOPSIS"
    )
    
    print_schedule_result(solution_topsis, data)
    
    # Analisis kualitas
    print(f"\n--- ANALISIS KUALITAS JADWAL ---")
    analysis_saw = dss.analyze_schedule_quality(solution_saw)
    analysis_topsis = dss.analyze_schedule_quality(solution_topsis)
    
    print(f"Perbandingan metode:")
    print(f"SAW - Success Rate: {analysis_saw['success_rate']:.1%}, Avg Score: {analysis_saw['average_score']:.3f}")
    print(f"TOPSIS - Success Rate: {analysis_topsis['success_rate']:.1%}, Avg Score: {analysis_topsis['average_score']:.3f}")
    
    return solution_saw, solution_topsis

def demo_criteria_sensitivity():
    """Demo analisis sensitivitas kriteria"""
    print_separator("DEMO ANALISIS SENSITIVITAS KRITERIA")
    
    data = get_complete_sample_data()
    dss = ExamSchedulingDSS()
    
    # Test dengan bobot kriteria yang berbeda
    scenarios = [
        {
            "name": "Fokus Keahlian",
            "weights": [0.50, 0.20, 0.15, 0.10, 0.05]
        },
        {
            "name": "Fokus Ketersediaan",
            "weights": [0.20, 0.20, 0.40, 0.15, 0.05]
        },
        {
            "name": "Fokus Pengalaman",
            "weights": [0.25, 0.25, 0.20, 0.10, 0.20]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- SKENARIO: {scenario['name']} ---")
        
        # Update bobot kriteria
        custom_criteria = data['criteria'].copy()
        for i, weight in enumerate(scenario['weights']):
            custom_criteria[i].weight = weight
        
        solution = dss.generate_schedule(
            students=data['students'],
            examiners=data['examiners'],
            rooms=data['rooms'],
            timeslots=data['timeslots'],
            exam_sessions=data['exam_sessions'],
            criteria=custom_criteria,
            method="SAW"
        )
        
        analysis = dss.analyze_schedule_quality(solution)
        
        print(f"Bobot kriteria: {scenario['weights']}")
        print(f"Success Rate: {analysis['success_rate']:.1%}")
        print(f"Average Score: {analysis['average_score']:.3f}")
        print(f"Ujian terjadwal: {analysis['scheduled_exams']}")

def main():
    """Main demo function"""
    print("🎓 SISTEM PENDUKUNG KEPUTUSAN PENJADWALAN UJIAN SKRIPSI")
    print("📊 Menggunakan Metode MCDM (AHP, SAW, TOPSIS)")
    print("🏛️  Universitas XYZ - Fakultas Teknik Informatika")
    
    try:
        # Demo 1: AHP Calculation
        demo_ahp_calculation()
        
        # Demo 2: Examiner Evaluation
        demo_examiner_evaluation()
        
        # Demo 3: Complete Scheduling
        demo_complete_scheduling()
        
        # Demo 4: Criteria Sensitivity
        demo_criteria_sensitivity()
        
        print_separator("DEMO SELESAI")
        print("✅ Semua demo berhasil dijalankan!")
        print("📝 Sistem siap digunakan untuk penjadwalan ujian skripsi")
        print("\n💡 Untuk menjalankan API server:")
        print("   python -m uvicorn main:app --reload --port 8001")
        
    except Exception as e:
        print(f"\n❌ Error dalam demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
