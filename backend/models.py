from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class CriteriaType(str, Enum):
    BENEFIT = "benefit"  # Higher is better
    COST = "cost"       # Lower is better

class Criteria(BaseModel):
    id: int = Field(..., description="Unique criteria identifier")
    name: str = Field(..., description="Criteria name")
    weight: float = Field(..., ge=0, le=1, description="Criteria weight (0-1)")
    type: CriteriaType = Field(..., description="Benefit or cost criteria")
    description: Optional[str] = Field(None, description="Criteria description")

class TimeSlot(BaseModel):
    id: int = Field(..., description="Unique identifier for the timeslot")
    day: str = Field(..., description="Day of the week")
    start_time: str = Field(..., description="Start time in HH:MM format")
    end_time: str = Field(..., description="End time in HH:MM format")
    session: str = Field(..., description="Session name (e.g., Morning, Afternoon)")

class Room(BaseModel):
    id: int = Field(..., description="Unique room identifier")
    name: str = Field(..., description="Room name or code")
    capacity: int = Field(..., gt=0, description="Room capacity")
    facilities: List[str] = Field(default=[], description="Available facilities")
    location: str = Field(..., description="Room location/building")
    quality_score: float = Field(..., ge=1, le=5, description="Room quality score (1-5)")

class Examiner(BaseModel):
    id: int = Field(..., description="Unique examiner identifier")
    name: str = Field(..., description="Examiner name")
    title: str = Field(..., description="Academic title")
    expertise: List[str] = Field(..., description="Areas of expertise")
    experience_years: int = Field(..., ge=0, description="Years of examination experience")
    workload: int = Field(default=0, description="Current examination workload")
    availability_score: float = Field(..., ge=1, le=5, description="Availability flexibility (1-5)")
    competency_score: float = Field(..., ge=1, le=5, description="Competency level (1-5)")
    available_timeslots: List[int] = Field(..., description="Available timeslot IDs")

class Student(BaseModel):
    id: int = Field(..., description="Unique student identifier")
    name: str = Field(..., description="Student name")
    nim: str = Field(..., description="Student ID number")
    thesis_title: str = Field(..., description="Thesis title")
    thesis_field: str = Field(..., description="Thesis field/area")
    supervisor_id: int = Field(..., description="Supervisor examiner ID")
    gpa: float = Field(..., ge=0, le=4, description="Student GPA")
    thesis_quality: float = Field(..., ge=1, le=5, description="Thesis quality assessment (1-5)")
    preferred_timeslots: Optional[List[int]] = Field(default=[], description="Preferred timeslot IDs")

class ExamSession(BaseModel):
    id: int = Field(..., description="Unique exam session identifier")
    student_id: int = Field(..., description="Student ID")
    duration: int = Field(default=120, description="Exam duration in minutes")
    required_examiners: int = Field(default=3, description="Number of required examiners")
    priority: float = Field(default=1.0, ge=0, le=1, description="Scheduling priority (0-1)")

class ExaminerEvaluation(BaseModel):
    examiner_id: int
    student_id: int
    compatibility_score: float = Field(..., ge=0, le=1, description="Examiner-student compatibility")
    expertise_match: float = Field(..., ge=0, le=1, description="Expertise matching score")
    workload_factor: float = Field(..., ge=0, le=1, description="Workload consideration factor")
    availability_factor: float = Field(..., ge=0, le=1, description="Availability factor")

class ScheduleResult(BaseModel):
    exam_id: int
    student_name: str
    timeslot_id: int
    room_id: int
    assigned_examiners: List[int]
    total_score: float
    criteria_scores: Dict[str, float]

class AHPMatrix(BaseModel):
    criteria: List[str] = Field(..., description="List of criteria names")
    matrix: List[List[float]] = Field(..., description="Pairwise comparison matrix")
    
class DSSSolution(BaseModel):
    schedule: List[ScheduleResult]
    method_used: str
    total_satisfaction: float
    criteria_weights: Dict[str, float]
    infeasible_exams: List[int] = Field(default=[], description="Exams that couldn't be scheduled")
