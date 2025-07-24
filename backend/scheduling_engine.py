import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from models import (
    Student, Examiner, Room, TimeSlot, ExamSession, 
    ExaminerEvaluation, ScheduleResult, Criteria, CriteriaType, DSSSolution
)
from mcdm_methods import MCDMEngine
import logging
from itertools import combinations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExamSchedulingDSS:
    """
    Decision Support System for Thesis Examination Scheduling
    Combines MCDM methods with constraint-based scheduling
    """
    
    def __init__(self):
        self.mcdm_engine = MCDMEngine()
        self.default_criteria = self._get_default_criteria()
    
    def _get_default_criteria(self) -> List[Criteria]:
        """Define default criteria for examiner evaluation"""
        return [
            Criteria(
                id=1, 
                name="expertise_match", 
                weight=0.30, 
                type=CriteriaType.BENEFIT,
                description="Kesesuaian keahlian penguji dengan bidang skripsi"
            ),
            Criteria(
                id=2, 
                name="competency_score", 
                weight=0.25, 
                type=CriteriaType.BENEFIT,
                description="Tingkat kompetensi penguji"
            ),
            Criteria(
                id=3, 
                name="availability_score", 
                weight=0.20, 
                type=CriteriaType.BENEFIT,
                description="Fleksibilitas ketersediaan waktu penguji"
            ),
            Criteria(
                id=4, 
                name="workload", 
                weight=0.15, 
                type=CriteriaType.COST,
                description="Beban kerja penguji saat ini"
            ),
            Criteria(
                id=5, 
                name="experience_years", 
                weight=0.10, 
                type=CriteriaType.BENEFIT,
                description="Pengalaman tahun menguji"
            )
        ]
    
    def calculate_expertise_match(self, examiner: Examiner, student: Student) -> float:
        """
        Calculate expertise matching score between examiner and student
        """
        student_field_keywords = student.thesis_field.lower().split()
        examiner_expertise = [exp.lower() for exp in examiner.expertise]
        
        matches = 0
        for keyword in student_field_keywords:
            for expertise in examiner_expertise:
                if keyword in expertise or expertise in keyword:
                    matches += 1
                    break
        
        # Normalize to 0-1 scale
        max_possible_matches = len(student_field_keywords)
        return min(matches / max_possible_matches, 1.0) if max_possible_matches > 0 else 0.0
    
    def evaluate_examiner_for_student(self, examiner: Examiner, student: Student, 
                                    timeslot_id: int) -> ExaminerEvaluation:
        """
        Evaluate an examiner for a specific student using multiple criteria
        """
        expertise_match = self.calculate_expertise_match(examiner, student)
        
        # Normalize competency score to 0-1
        competency_factor = examiner.competency_score / 5.0
        
        # Availability factor based on timeslot availability
        availability_factor = 1.0 if timeslot_id in examiner.available_timeslots else 0.0
        
        # Workload factor (inverse relationship - lower workload is better)
        max_workload = 10  # Assume maximum reasonable workload
        workload_factor = max(0, (max_workload - examiner.workload) / max_workload)
        
        return ExaminerEvaluation(
            examiner_id=examiner.id,
            student_id=student.id,
            compatibility_score=expertise_match,
            expertise_match=expertise_match,
            workload_factor=workload_factor,
            availability_factor=availability_factor
        )
    
    def select_best_examiners(self, student: Student, examiners: List[Examiner], 
                            timeslot_id: int, required_count: int = 3,
                            criteria: Optional[List[Criteria]] = None,
                            method: str = "SAW") -> List[Tuple[Examiner, float]]:
        """
        Select best examiners for a student using MCDM methods
        """
        if criteria is None:
            criteria = self.default_criteria
        
        # Filter available examiners for the timeslot
        available_examiners = [e for e in examiners if timeslot_id in e.available_timeslots]
        
        if len(available_examiners) < required_count:
            logger.warning(f"Not enough available examiners for student {student.name} at timeslot {timeslot_id}")
            return []
        
        # Exclude supervisor from regular examiner selection (supervisor is mandatory)
        regular_examiners = [e for e in available_examiners if e.id != student.supervisor_id]
        supervisor = next((e for e in available_examiners if e.id == student.supervisor_id), None)
        
        if not supervisor:
            logger.error(f"Supervisor not available for student {student.name}")
            return []
        
        # Build decision matrix for regular examiners
        decision_matrix = []
        examiner_evaluations = []
        
        for examiner in regular_examiners:
            evaluation = self.evaluate_examiner_for_student(examiner, student, timeslot_id)
            examiner_evaluations.append(evaluation)
            
            # Create row for decision matrix based on criteria
            row = []
            for criterion in criteria:
                if criterion.name == "expertise_match":
                    row.append(evaluation.expertise_match)
                elif criterion.name == "competency_score":
                    row.append(examiner.competency_score)
                elif criterion.name == "availability_score":
                    row.append(examiner.availability_score)
                elif criterion.name == "workload":
                    row.append(examiner.workload)
                elif criterion.name == "experience_years":
                    row.append(examiner.experience_years)
                else:
                    row.append(0.5)  # Default value
            
            decision_matrix.append(row)
        
        if not decision_matrix:
            return []
        
        # Apply MCDM method
        scores, criteria_weights = self.mcdm_engine.evaluate_alternatives(
            decision_matrix, criteria, method
        )
        
        # Combine examiners with their scores
        examiner_scores = list(zip(regular_examiners, scores))
        
        # Sort by score (descending)
        examiner_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select top examiners (excluding supervisor)
        selected_regular = examiner_scores[:required_count-1]
        
        # Add supervisor with a high score
        supervisor_evaluation = self.evaluate_examiner_for_student(supervisor, student, timeslot_id)
        supervisor_score = 0.9  # High score for supervisor
        
        result = [(supervisor, supervisor_score)] + selected_regular
        
        logger.info(f"Selected {len(result)} examiners for student {student.name}")
        return result
    
    def evaluate_room_suitability(self, room: Room, student: Student, 
                                required_capacity: int = 10) -> float:
        """
        Evaluate room suitability for an exam session
        """
        # Capacity factor
        capacity_factor = min(room.capacity / required_capacity, 1.0)
        
        # Quality factor
        quality_factor = room.quality_score / 5.0
        
        # Facility factor (basic scoring)
        facility_score = len(room.facilities) / 10.0  # Assume max 10 facilities
        facility_factor = min(facility_score, 1.0)
        
        # Combined score
        total_score = (capacity_factor * 0.5 + quality_factor * 0.3 + facility_factor * 0.2)
        
        return total_score
    
    def check_scheduling_constraints(self, schedule: List[ScheduleResult], 
                                   new_exam: ScheduleResult) -> bool:
        """
        Check if adding a new exam violates scheduling constraints
        """
        for existing_exam in schedule:
            # Same timeslot conflicts
            if existing_exam.timeslot_id == new_exam.timeslot_id:
                # Room conflict
                if existing_exam.room_id == new_exam.room_id:
                    return False
                
                # Examiner conflict
                if set(existing_exam.assigned_examiners) & set(new_exam.assigned_examiners):
                    return False
        
        return True
    
    def generate_schedule(self, students: List[Student], examiners: List[Examiner],
                         rooms: List[Room], timeslots: List[TimeSlot],
                         exam_sessions: List[ExamSession],
                         criteria: Optional[List[Criteria]] = None,
                         method: str = "SAW") -> DSSSolution:
        """
        Generate optimal exam schedule using DSS approach
        """
        if criteria is None:
            criteria = self.default_criteria
        
        schedule = []
        infeasible_exams = []
        total_satisfaction = 0.0
        
        # Create student lookup
        student_lookup = {s.id: s for s in students}
        room_lookup = {r.id: r for r in rooms}
        
        # Sort exam sessions by priority (descending)
        sorted_sessions = sorted(exam_sessions, key=lambda x: x.priority, reverse=True)
        
        for session in sorted_sessions:
            student = student_lookup.get(session.student_id)
            if not student:
                infeasible_exams.append(session.id)
                continue
            
            best_schedule = None
            best_score = -1
            
            # Try each timeslot
            for timeslot in timeslots:
                # Select best examiners for this timeslot
                selected_examiners = self.select_best_examiners(
                    student, examiners, timeslot.id, 
                    session.required_examiners, criteria, method
                )
                
                if len(selected_examiners) < session.required_examiners:
                    continue
                
                # Try each room
                for room in rooms:
                    room_score = self.evaluate_room_suitability(room, student)
                    
                    # Calculate examiner scores
                    examiner_ids = [e[0].id for e in selected_examiners]
                    examiner_score = np.mean([e[1] for e in selected_examiners])
                    
                    # Combined score
                    combined_score = (examiner_score * 0.7 + room_score * 0.3)
                    
                    # Create potential schedule result
                    potential_result = ScheduleResult(
                        exam_id=session.id,
                        student_name=student.name,
                        timeslot_id=timeslot.id,
                        room_id=room.id,
                        assigned_examiners=examiner_ids,
                        total_score=combined_score,
                        criteria_scores={
                            "examiner_quality": examiner_score,
                            "room_suitability": room_score,
                            "combined_score": combined_score
                        }
                    )
                    
                    # Check constraints
                    if self.check_scheduling_constraints(schedule, potential_result):
                        if combined_score > best_score:
                            best_score = combined_score
                            best_schedule = potential_result
            
            if best_schedule:
                schedule.append(best_schedule)
                total_satisfaction += best_score
                
                # Update examiner workloads
                for examiner_id in best_schedule.assigned_examiners:
                    for examiner in examiners:
                        if examiner.id == examiner_id:
                            examiner.workload += 1
                            break
                
                logger.info(f"Scheduled exam for {student.name} with score {best_score:.3f}")
            else:
                infeasible_exams.append(session.id)
                logger.warning(f"Could not schedule exam for {student.name}")
        
        # Calculate average satisfaction
        avg_satisfaction = total_satisfaction / len(schedule) if schedule else 0.0
        
        # Get criteria weights
        _, criteria_weights = self.mcdm_engine.evaluate_alternatives(
            [[1] * len(criteria)], criteria, method
        )
        
        return DSSSolution(
            schedule=schedule,
            method_used=method,
            total_satisfaction=avg_satisfaction,
            criteria_weights=criteria_weights,
            infeasible_exams=infeasible_exams
        )
    
    def analyze_schedule_quality(self, solution: DSSSolution) -> Dict[str, float]:
        """
        Analyze the quality of generated schedule
        """
        if not solution.schedule:
            return {"overall_quality": 0.0}
        
        scores = [result.total_score for result in solution.schedule]
        
        analysis = {
            "overall_quality": solution.total_satisfaction,
            "average_score": np.mean(scores),
            "min_score": np.min(scores),
            "max_score": np.max(scores),
            "score_std": np.std(scores),
            "scheduled_exams": len(solution.schedule),
            "infeasible_exams": len(solution.infeasible_exams),
            "success_rate": len(solution.schedule) / (len(solution.schedule) + len(solution.infeasible_exams))
        }
        
        return analysis
