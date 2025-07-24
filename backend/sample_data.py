"""
Sample data generator for testing the Exam Scheduling DSS
"""

from typing import List
from models import Student, Examiner, Room, TimeSlot, ExamSession, Criteria, CriteriaType

def generate_sample_students() -> List[Student]:
    """Generate sample student data"""
    return [
        Student(
            id=1,
            name="Andi Pratama",
            nim="20190001",
            thesis_title="Implementasi Machine Learning untuk Prediksi Cuaca",
            thesis_field="machine learning artificial intelligence data science",
            supervisor_id=1,
            gpa=3.75,
            thesis_quality=4.2,
            preferred_timeslots=[1, 2, 3]
        ),
        Student(
            id=2,
            name="Sari Dewi",
            nim="20190002",
            thesis_title="Pengembangan Aplikasi Web E-Commerce dengan React",
            thesis_field="web development software engineering frontend",
            supervisor_id=2,
            gpa=3.60,
            thesis_quality=4.0,
            preferred_timeslots=[2, 4, 5]
        ),
        Student(
            id=3,
            name="Budi Santoso",
            nim="20190003",
            thesis_title="Sistem Keamanan Jaringan menggunakan Blockchain",
            thesis_field="network security blockchain cybersecurity",
            supervisor_id=3,
            gpa=3.85,
            thesis_quality=4.5,
            preferred_timeslots=[1, 3, 6]
        ),
        Student(
            id=4,
            name="Maya Sari",
            nim="20190004",
            thesis_title="Analisis Big Data untuk Business Intelligence",
            thesis_field="big data analytics business intelligence data mining",
            supervisor_id=4,
            gpa=3.70,
            thesis_quality=4.1,
            preferred_timeslots=[4, 5, 6]
        ),
        Student(
            id=5,
            name="Rudi Hermawan",
            nim="20190005",
            thesis_title="Pengembangan Game Mobile dengan Unity",
            thesis_field="game development mobile programming unity",
            supervisor_id=5,
            gpa=3.55,
            thesis_quality=3.8,
            preferred_timeslots=[1, 2, 4]
        )
    ]

def generate_sample_examiners() -> List[Examiner]:
    """Generate sample examiner data"""
    return [
        Examiner(
            id=1,
            name="Prof. Dr. Ahmad Wijaya, M.Kom",
            title="Professor",
            expertise=["machine learning", "artificial intelligence", "data science", "computer vision"],
            experience_years=15,
            workload=2,
            availability_score=4.0,
            competency_score=4.8,
            available_timeslots=[1, 2, 3, 4]
        ),
        Examiner(
            id=2,
            name="Dr. Rina Kusuma, M.T",
            title="Associate Professor",
            expertise=["web development", "software engineering", "frontend development", "javascript"],
            experience_years=12,
            workload=3,
            availability_score=4.2,
            competency_score=4.5,
            available_timeslots=[2, 3, 4, 5]
        ),
        Examiner(
            id=3,
            name="Dr. Bambang Sutrisno, M.Kom",
            title="Associate Professor",
            expertise=["network security", "cybersecurity", "blockchain", "cryptography"],
            experience_years=10,
            workload=1,
            availability_score=4.5,
            competency_score=4.6,
            available_timeslots=[1, 3, 5, 6]
        ),
        Examiner(
            id=4,
            name="Dr. Indira Sari, M.Sc",
            title="Assistant Professor",
            expertise=["big data", "data analytics", "business intelligence", "data mining"],
            experience_years=8,
            workload=2,
            availability_score=4.3,
            competency_score=4.4,
            available_timeslots=[3, 4, 5, 6]
        ),
        Examiner(
            id=5,
            name="Dr. Fajar Nugroho, M.T",
            title="Assistant Professor",
            expertise=["game development", "mobile programming", "unity", "computer graphics"],
            experience_years=7,
            workload=1,
            availability_score=4.7,
            competency_score=4.2,
            available_timeslots=[1, 2, 4, 6]
        ),
        Examiner(
            id=6,
            name="Prof. Dr. Siti Nurhaliza, M.Kom",
            title="Professor",
            expertise=["database systems", "information systems", "software architecture"],
            experience_years=18,
            workload=4,
            availability_score=3.8,
            competency_score=4.9,
            available_timeslots=[2, 3, 5]
        ),
        Examiner(
            id=7,
            name="Dr. Hendra Wijaya, M.T",
            title="Associate Professor",
            expertise=["algorithms", "data structures", "computational complexity", "optimization"],
            experience_years=11,
            workload=2,
            availability_score=4.1,
            competency_score=4.7,
            available_timeslots=[1, 2, 3, 4, 5, 6]
        ),
        Examiner(
            id=8,
            name="Dr. Lisa Permata, M.Kom",
            title="Assistant Professor",
            expertise=["human computer interaction", "user experience", "interface design"],
            experience_years=6,
            workload=1,
            availability_score=4.6,
            competency_score=4.1,
            available_timeslots=[1, 3, 4, 5]
        )
    ]

def generate_sample_rooms() -> List[Room]:
    """Generate sample room data"""
    return [
        Room(
            id=1,
            name="Ruang Sidang A",
            capacity=25,
            facilities=["projector", "whiteboard", "sound_system", "air_conditioning"],
            location="Gedung Informatika Lt. 3",
            quality_score=4.5
        ),
        Room(
            id=2,
            name="Ruang Sidang B",
            capacity=20,
            facilities=["projector", "whiteboard", "air_conditioning"],
            location="Gedung Informatika Lt. 3",
            quality_score=4.0
        ),
        Room(
            id=3,
            name="Ruang Sidang C",
            capacity=15,
            facilities=["projector", "whiteboard"],
            location="Gedung Informatika Lt. 2",
            quality_score=3.5
        ),
        Room(
            id=4,
            name="Ruang Seminar",
            capacity=30,
            facilities=["projector", "whiteboard", "sound_system", "air_conditioning", "microphone"],
            location="Gedung Informatika Lt. 4",
            quality_score=4.8
        ),
        Room(
            id=5,
            name="Lab Komputer 1",
            capacity=18,
            facilities=["computers", "projector", "whiteboard", "air_conditioning"],
            location="Gedung Informatika Lt. 1",
            quality_score=4.2
        )
    ]

def generate_sample_timeslots() -> List[TimeSlot]:
    """Generate sample timeslot data"""
    return [
        TimeSlot(
            id=1,
            day="Senin",
            start_time="08:00",
            end_time="10:00",
            session="Pagi"
        ),
        TimeSlot(
            id=2,
            day="Senin",
            start_time="10:30",
            end_time="12:30",
            session="Pagi"
        ),
        TimeSlot(
            id=3,
            day="Senin",
            start_time="13:30",
            end_time="15:30",
            session="Siang"
        ),
        TimeSlot(
            id=4,
            day="Selasa",
            start_time="08:00",
            end_time="10:00",
            session="Pagi"
        ),
        TimeSlot(
            id=5,
            day="Selasa",
            start_time="10:30",
            end_time="12:30",
            session="Pagi"
        ),
        TimeSlot(
            id=6,
            day="Selasa",
            start_time="13:30",
            end_time="15:30",
            session="Siang"
        ),
        TimeSlot(
            id=7,
            day="Rabu",
            start_time="08:00",
            end_time="10:00",
            session="Pagi"
        ),
        TimeSlot(
            id=8,
            day="Rabu",
            start_time="10:30",
            end_time="12:30",
            session="Pagi"
        )
    ]

def generate_sample_exam_sessions() -> List[ExamSession]:
    """Generate sample exam session data"""
    return [
        ExamSession(
            id=1,
            student_id=1,
            duration=120,
            required_examiners=3,
            priority=1.0
        ),
        ExamSession(
            id=2,
            student_id=2,
            duration=120,
            required_examiners=3,
            priority=0.9
        ),
        ExamSession(
            id=3,
            student_id=3,
            duration=120,
            required_examiners=3,
            priority=0.95
        ),
        ExamSession(
            id=4,
            student_id=4,
            duration=120,
            required_examiners=3,
            priority=0.85
        ),
        ExamSession(
            id=5,
            student_id=5,
            duration=120,
            required_examiners=3,
            priority=0.8
        )
    ]

def generate_sample_criteria() -> List[Criteria]:
    """Generate sample criteria for evaluation"""
    return [
        Criteria(
            id=1,
            name="expertise_match",
            weight=0.30,
            type=CriteriaType.BENEFIT,
            description="Kesesuaian keahlian penguji dengan bidang skripsi mahasiswa"
        ),
        Criteria(
            id=2,
            name="competency_score",
            weight=0.25,
            type=CriteriaType.BENEFIT,
            description="Tingkat kompetensi dan kualifikasi penguji"
        ),
        Criteria(
            id=3,
            name="availability_score",
            weight=0.20,
            type=CriteriaType.BENEFIT,
            description="Fleksibilitas dan ketersediaan waktu penguji"
        ),
        Criteria(
            id=4,
            name="workload",
            weight=0.15,
            type=CriteriaType.COST,
            description="Beban kerja penguji saat ini (semakin rendah semakin baik)"
        ),
        Criteria(
            id=5,
            name="experience_years",
            weight=0.10,
            type=CriteriaType.BENEFIT,
            description="Pengalaman tahun menguji ujian skripsi"
        )
    ]

def get_complete_sample_data():
    """Get complete sample data for testing"""
    return {
        "students": generate_sample_students(),
        "examiners": generate_sample_examiners(),
        "rooms": generate_sample_rooms(),
        "timeslots": generate_sample_timeslots(),
        "exam_sessions": generate_sample_exam_sessions(),
        "criteria": generate_sample_criteria()
    }

# Example usage and demonstration
if __name__ == "__main__":
    print("=== SAMPLE DATA UNTUK SISTEM PENJADWALAN UJIAN SKRIPSI ===\n")
    
    data = get_complete_sample_data()
    
    print(f"Jumlah Mahasiswa: {len(data['students'])}")
    print(f"Jumlah Penguji: {len(data['examiners'])}")
    print(f"Jumlah Ruangan: {len(data['rooms'])}")
    print(f"Jumlah Slot Waktu: {len(data['timeslots'])}")
    print(f"Jumlah Sesi Ujian: {len(data['exam_sessions'])}")
    print(f"Jumlah Kriteria: {len(data['criteria'])}")
    
    print("\n=== CONTOH DATA MAHASISWA ===")
    for student in data['students'][:2]:
        print(f"- {student.name} ({student.nim})")
        print(f"  Judul: {student.thesis_title}")
        print(f"  Bidang: {student.thesis_field}")
        print(f"  IPK: {student.gpa}")
        print()
    
    print("=== CONTOH DATA PENGUJI ===")
    for examiner in data['examiners'][:3]:
        print(f"- {examiner.name}")
        print(f"  Keahlian: {', '.join(examiner.expertise)}")
        print(f"  Pengalaman: {examiner.experience_years} tahun")
        print(f"  Beban Kerja: {examiner.workload}")
        print()
    
    print("=== KRITERIA EVALUASI ===")
    for criterion in data['criteria']:
        print(f"- {criterion.name} (Bobot: {criterion.weight})")
        print(f"  Tipe: {criterion.type.value}")
        print(f"  Deskripsi: {criterion.description}")
        print()
