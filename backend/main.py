from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging

from models import (
    Student, Examiner, Room, TimeSlot, ExamSession, 
    Criteria, AHPMatrix, DSSSolution, ScheduleResult
)
from scheduling_engine import ExamSchedulingDSS
from mcdm_methods import MCDMEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sistem Pendukung Keputusan Penjadwalan Ujian Skripsi",
    description="Decision Support System for Thesis Examination Scheduling using MCDM methods",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DSS engine
dss_engine = ExamSchedulingDSS()
mcdm_engine = MCDMEngine()

class SchedulingRequest(BaseModel):
    students: List[Student]
    examiners: List[Examiner]
    rooms: List[Room]
    timeslots: List[TimeSlot]
    exam_sessions: List[ExamSession]
    criteria: Optional[List[Criteria]] = None
    method: str = "SAW"

class AHPWeightRequest(BaseModel):
    ahp_matrix: AHPMatrix

class ExaminerEvaluationRequest(BaseModel):
    student: Student
    examiners: List[Examiner]
    timeslot_id: int
    criteria: Optional[List[Criteria]] = None
    method: str = "SAW"

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Selamat datang di Sistem Pendukung Keputusan Penjadwalan Ujian Skripsi",
        "description": "Decision Support System menggunakan metode MCDM (AHP, SAW, TOPSIS)",
        "version": "1.0.0",
        "endpoints": {
            "schedule": "/schedule - Generate exam schedule",
            "ahp-weights": "/ahp-weights - Calculate AHP weights",
            "evaluate-examiners": "/evaluate-examiners - Evaluate examiners for student",
            "criteria": "/criteria - Get default criteria",
            "methods": "/methods - Get available MCDM methods"
        }
    }

@app.get("/methods")
async def get_available_methods():
    """Get available MCDM methods"""
    return {
        "methods": [
            {
                "name": "SAW",
                "full_name": "Simple Additive Weighting",
                "description": "Metode penjumlahan terbobot sederhana"
            },
            {
                "name": "TOPSIS",
                "full_name": "Technique for Order Preference by Similarity to Ideal Solution",
                "description": "Teknik untuk urutan preferensi berdasarkan kemiripan dengan solusi ideal"
            },
            {
                "name": "AHP",
                "full_name": "Analytic Hierarchy Process",
                "description": "Proses hierarki analitik untuk perbandingan berpasangan"
            }
        ]
    }

@app.get("/criteria")
async def get_default_criteria():
    """Get default evaluation criteria"""
    return {
        "criteria": dss_engine.default_criteria,
        "description": "Kriteria default untuk evaluasi penguji ujian skripsi"
    }

@app.post("/ahp-weights")
async def calculate_ahp_weights(request: AHPWeightRequest):
    """Calculate criteria weights using AHP method"""
    try:
        weights, consistency_ratio, is_consistent = mcdm_engine.calculate_ahp_weights(request.ahp_matrix)
        
        return {
            "weights": weights,
            "consistency_ratio": consistency_ratio,
            "is_consistent": is_consistent,
            "criteria": request.ahp_matrix.criteria,
            "message": "Konsisten" if is_consistent else "Tidak konsisten - perlu revisi matriks perbandingan"
        }
    
    except Exception as e:
        logger.error(f"Error calculating AHP weights: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error dalam perhitungan bobot AHP: {str(e)}"
        )

@app.post("/evaluate-examiners")
async def evaluate_examiners(request: ExaminerEvaluationRequest):
    """Evaluate examiners for a specific student"""
    try:
        selected_examiners = dss_engine.select_best_examiners(
            student=request.student,
            examiners=request.examiners,
            timeslot_id=request.timeslot_id,
            required_count=3,
            criteria=request.criteria,
            method=request.method
        )
        
        result = []
        for examiner, score in selected_examiners:
            result.append({
                "examiner": examiner,
                "score": score,
                "rank": len(result) + 1
            })
        
        return {
            "student_name": request.student.name,
            "timeslot_id": request.timeslot_id,
            "method_used": request.method,
            "selected_examiners": result,
            "total_selected": len(result)
        }
    
    except Exception as e:
        logger.error(f"Error evaluating examiners: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error dalam evaluasi penguji: {str(e)}"
        )

@app.post("/schedule", response_model=DSSSolution)
async def generate_schedule(request: SchedulingRequest):
    """Generate optimal exam schedule using DSS"""
    try:
        # Validate method
        if request.method.upper() not in ["SAW", "TOPSIS"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Metode tidak didukung: {request.method}. Gunakan SAW atau TOPSIS"
            )
        
        # Validate input data
        if not request.students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data mahasiswa tidak boleh kosong"
            )
        
        if not request.examiners:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data penguji tidak boleh kosong"
            )
        
        if not request.rooms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data ruangan tidak boleh kosong"
            )
        
        if not request.timeslots:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data slot waktu tidak boleh kosong"
            )
        
        # Generate schedule
        logger.info(f"Generating schedule using {request.method} method")
        solution = dss_engine.generate_schedule(
            students=request.students,
            examiners=request.examiners,
            rooms=request.rooms,
            timeslots=request.timeslots,
            exam_sessions=request.exam_sessions,
            criteria=request.criteria,
            method=request.method
        )
        
        logger.info(f"Schedule generated successfully: {len(solution.schedule)} exams scheduled")
        return solution
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error dalam pembuatan jadwal: {str(e)}"
        )

@app.post("/analyze-schedule")
async def analyze_schedule(solution: DSSSolution):
    """Analyze the quality of a generated schedule"""
    try:
        analysis = dss_engine.analyze_schedule_quality(solution)
        
        return {
            "analysis": analysis,
            "recommendations": _generate_recommendations(analysis),
            "method_used": solution.method_used
        }
    
    except Exception as e:
        logger.error(f"Error analyzing schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error dalam analisis jadwal: {str(e)}"
        )

def _generate_recommendations(analysis: Dict[str, float]) -> List[str]:
    """Generate recommendations based on schedule analysis"""
    recommendations = []
    
    if analysis.get("success_rate", 0) < 0.8:
        recommendations.append("Tingkatkan jumlah penguji atau slot waktu yang tersedia")
    
    if analysis.get("score_std", 0) > 0.3:
        recommendations.append("Distribusi kualitas jadwal tidak merata, pertimbangkan penyesuaian kriteria")
    
    if analysis.get("average_score", 0) < 0.6:
        recommendations.append("Kualitas jadwal rendah, pertimbangkan menambah penguji berkualitas")
    
    if analysis.get("infeasible_exams", 0) > 0:
        recommendations.append(f"Ada {analysis['infeasible_exams']} ujian yang tidak dapat dijadwalkan")
    
    if not recommendations:
        recommendations.append("Jadwal sudah optimal dengan kualitas yang baik")
    
    return recommendations

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Exam Scheduling DSS",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
