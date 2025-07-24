import pytest
import numpy as np
from typing import List

from models import (
    Student, Examiner, Room, TimeSlot, ExamSession, 
    Criteria, CriteriaType, AHPMatrix
)
from scheduling_engine import ExamSchedulingDSS
from mcdm_methods import MCDMEngine, AHPMethod, SAWMethod, TOPSISMethod

class TestMCDMMethods:
    """Test cases for MCDM methods"""
    
    def setup_method(self):
        """Setup test data"""
        self.mcdm_engine = MCDMEngine()
        self.ahp = AHPMethod()
        self.saw = SAWMethod()
        self.topsis = TOPSISMethod()
        
        # Sample criteria
        self.criteria = [
            Criteria(id=1, name="expertise", weight=0.4, type=CriteriaType.BENEFIT),
            Criteria(id=2, name="experience", weight=0.3, type=CriteriaType.BENEFIT),
            Criteria(id=3, name="workload", weight=0.3, type=CriteriaType.COST)
        ]
        
        # Sample decision matrix (3 alternatives, 3 criteria)
        self.decision_matrix = [
            [0.8, 5, 2],  # Alternative 1
            [0.6, 8, 4],  # Alternative 2
            [0.9, 3, 1]   # Alternative 3
        ]
    
    def test_ahp_weight_calculation(self):
        """Test AHP weight calculation"""
        # Sample pairwise comparison matrix (3x3)
        pairwise_matrix = [
            [1, 2, 3],
            [0.5, 1, 2],
            [0.33, 0.5, 1]
        ]
        
        weights, consistency_ratio = self.ahp.calculate_weights(pairwise_matrix)
        
        # Check if weights sum to approximately 1
        assert abs(sum(weights) - 1.0) < 0.01
        
        # Check if consistency ratio is reasonable
        assert consistency_ratio >= 0
        
        # Check if weights are positive
        assert all(w > 0 for w in weights)
    
    def test_ahp_matrix_validation(self):
        """Test AHP matrix validation"""
        # Valid matrix (perfectly reciprocal)
        valid_matrix = [
            [1.0, 2.0, 3.0],
            [0.5, 1.0, 2.0],
            [1.0/3.0, 0.5, 1.0]
        ]
        assert self.ahp.validate_matrix(valid_matrix)
        
        # Invalid matrix (not reciprocal)
        invalid_matrix = [
            [1.0, 2.0, 3.0],
            [0.5, 1.0, 2.0],
            [0.5, 0.5, 1.0]  # Should be 1/3, not 0.5
        ]
        assert not self.ahp.validate_matrix(invalid_matrix)
    
    def test_saw_method(self):
        """Test SAW method calculation"""
        weights = [0.4, 0.3, 0.3]
        criteria_types = [CriteriaType.BENEFIT, CriteriaType.BENEFIT, CriteriaType.COST]
        
        scores = self.saw.calculate_scores(
            np.array(self.decision_matrix), 
            weights, 
            criteria_types
        )
        
        # Check if scores are calculated
        assert len(scores) == 3
        
        # Check if scores are between 0 and 1
        assert all(0 <= score <= 1 for score in scores)
    
    def test_topsis_method(self):
        """Test TOPSIS method calculation"""
        weights = [0.4, 0.3, 0.3]
        criteria_types = [CriteriaType.BENEFIT, CriteriaType.BENEFIT, CriteriaType.COST]
        
        scores = self.topsis.calculate_scores(
            np.array(self.decision_matrix), 
            weights, 
            criteria_types
        )
        
        # Check if scores are calculated
        assert len(scores) == 3
        
        # Check if scores are between 0 and 1
        assert all(0 <= score <= 1 for score in scores)
    
    def test_mcdm_engine_evaluation(self):
        """Test MCDM engine evaluation"""
        # Test SAW method
        scores_saw, weights_dict = self.mcdm_engine.evaluate_alternatives(
            self.decision_matrix, self.criteria, "SAW"
        )
        
        assert len(scores_saw) == 3
        assert len(weights_dict) == 3
        
        # Test TOPSIS method
        scores_topsis, _ = self.mcdm_engine.evaluate_alternatives(
            self.decision_matrix, self.criteria, "TOPSIS"
        )
        
        assert len(scores_topsis) == 3
    
    def test_ranking(self):
        """Test alternative ranking"""
        scores = [0.8, 0.6, 0.9]
        ranking = self.mcdm_engine.rank_alternatives(scores)
        
        # Check if ranking is correct (descending order)
        assert ranking == [2, 0, 1]  # Indices of alternatives in descending score order

class TestSchedulingEngine:
    """Test cases for scheduling engine"""
    
    def setup_method(self):
        """Setup test data"""
        self.dss = ExamSchedulingDSS()
        
        # Sample students
        self.students = [
            Student(
                id=1, name="Alice", nim="123456", 
                thesis_title="Machine Learning in Healthcare",
                thesis_field="machine learning artificial intelligence",
                supervisor_id=1, gpa=3.8, thesis_quality=4.5
            ),
            Student(
                id=2, name="Bob", nim="123457",
                thesis_title="Web Development Framework",
                thesis_field="web development software engineering",
                supervisor_id=2, gpa=3.6, thesis_quality=4.0
            )
        ]
        
        # Sample examiners
        self.examiners = [
            Examiner(
                id=1, name="Dr. Smith", title="Professor",
                expertise=["machine learning", "artificial intelligence"],
                experience_years=10, workload=2,
                availability_score=4.0, competency_score=4.5,
                available_timeslots=[1, 2, 3]
            ),
            Examiner(
                id=2, name="Dr. Johnson", title="Associate Professor",
                expertise=["web development", "software engineering"],
                experience_years=8, workload=1,
                availability_score=4.5, competency_score=4.0,
                available_timeslots=[1, 2, 4]
            ),
            Examiner(
                id=3, name="Dr. Brown", title="Assistant Professor",
                expertise=["computer science", "algorithms"],
                experience_years=5, workload=0,
                availability_score=5.0, competency_score=3.5,
                available_timeslots=[1, 3, 4]
            )
        ]
        
        # Sample rooms
        self.rooms = [
            Room(
                id=1, name="Room A", capacity=20,
                facilities=["projector", "whiteboard"],
                location="Building 1", quality_score=4.0
            ),
            Room(
                id=2, name="Room B", capacity=15,
                facilities=["projector"],
                location="Building 2", quality_score=3.5
            )
        ]
        
        # Sample timeslots
        self.timeslots = [
            TimeSlot(id=1, day="Monday", start_time="08:00", end_time="10:00", session="Morning"),
            TimeSlot(id=2, day="Monday", start_time="10:00", end_time="12:00", session="Morning"),
            TimeSlot(id=3, day="Tuesday", start_time="08:00", end_time="10:00", session="Morning"),
            TimeSlot(id=4, day="Tuesday", start_time="13:00", end_time="15:00", session="Afternoon")
        ]
        
        # Sample exam sessions
        self.exam_sessions = [
            ExamSession(id=1, student_id=1, duration=120, required_examiners=3, priority=1.0),
            ExamSession(id=2, student_id=2, duration=120, required_examiners=3, priority=0.8)
        ]
    
    def test_expertise_matching(self):
        """Test expertise matching calculation"""
        student = self.students[0]  # Alice - machine learning
        examiner = self.examiners[0]  # Dr. Smith - machine learning expert
        
        match_score = self.dss.calculate_expertise_match(examiner, student)
        
        # Should have high match score
        assert match_score > 0.5
        
        # Test with non-matching examiner
        non_matching_examiner = self.examiners[1]  # Dr. Johnson - web development
        low_match_score = self.dss.calculate_expertise_match(non_matching_examiner, student)
        
        # Should have lower match score
        assert low_match_score < match_score
    
    def test_examiner_evaluation(self):
        """Test examiner evaluation for student"""
        student = self.students[0]
        examiner = self.examiners[0]
        timeslot_id = 1
        
        evaluation = self.dss.evaluate_examiner_for_student(examiner, student, timeslot_id)
        
        assert evaluation.examiner_id == examiner.id
        assert evaluation.student_id == student.id
        assert 0 <= evaluation.expertise_match <= 1
        assert 0 <= evaluation.workload_factor <= 1
        assert evaluation.availability_factor in [0.0, 1.0]
    
    def test_examiner_selection(self):
        """Test best examiner selection"""
        student = self.students[0]
        timeslot_id = 1
        
        selected_examiners = self.dss.select_best_examiners(
            student, self.examiners, timeslot_id, required_count=3
        )
        
        # Should select examiners (including supervisor)
        assert len(selected_examiners) > 0
        
        # Check if supervisor is included
        supervisor_ids = [e[0].id for e in selected_examiners]
        assert student.supervisor_id in supervisor_ids
    
    def test_room_evaluation(self):
        """Test room suitability evaluation"""
        student = self.students[0]
        room = self.rooms[0]
        
        suitability_score = self.dss.evaluate_room_suitability(room, student)
        
        assert 0 <= suitability_score <= 1
    
    def test_constraint_checking(self):
        """Test scheduling constraint checking"""
        # Create sample schedule results
        existing_schedule = [
            type('ScheduleResult', (), {
                'timeslot_id': 1,
                'room_id': 1,
                'assigned_examiners': [1, 2, 3]
            })()
        ]
        
        # Test room conflict
        conflicting_exam = type('ScheduleResult', (), {
            'timeslot_id': 1,
            'room_id': 1,  # Same room
            'assigned_examiners': [4, 5, 6]
        })()
        
        assert not self.dss.check_scheduling_constraints(existing_schedule, conflicting_exam)
        
        # Test examiner conflict
        examiner_conflict = type('ScheduleResult', (), {
            'timeslot_id': 1,
            'room_id': 2,  # Different room
            'assigned_examiners': [1, 4, 5]  # Examiner 1 conflict
        })()
        
        assert not self.dss.check_scheduling_constraints(existing_schedule, examiner_conflict)
        
        # Test valid scheduling
        valid_exam = type('ScheduleResult', (), {
            'timeslot_id': 2,  # Different timeslot
            'room_id': 1,
            'assigned_examiners': [4, 5, 6]
        })()
        
        assert self.dss.check_scheduling_constraints(existing_schedule, valid_exam)
    
    def test_schedule_generation(self):
        """Test complete schedule generation"""
        solution = self.dss.generate_schedule(
            students=self.students,
            examiners=self.examiners,
            rooms=self.rooms,
            timeslots=self.timeslots,
            exam_sessions=self.exam_sessions,
            method="SAW"
        )
        
        # Check if solution is generated
        assert solution is not None
        assert solution.method_used == "SAW"
        assert isinstance(solution.schedule, list)
        assert isinstance(solution.infeasible_exams, list)
        
        # Check if some exams are scheduled (depending on constraints)
        total_exams = len(solution.schedule) + len(solution.infeasible_exams)
        assert total_exams == len(self.exam_sessions)
    
    def test_schedule_analysis(self):
        """Test schedule quality analysis"""
        # Generate a sample solution
        solution = self.dss.generate_schedule(
            students=self.students,
            examiners=self.examiners,
            rooms=self.rooms,
            timeslots=self.timeslots,
            exam_sessions=self.exam_sessions,
            method="SAW"
        )
        
        analysis = self.dss.analyze_schedule_quality(solution)
        
        # Check if analysis contains expected metrics
        expected_metrics = [
            "overall_quality", "average_score", "min_score", 
            "max_score", "score_std", "scheduled_exams", 
            "infeasible_exams", "success_rate"
        ]
        
        for metric in expected_metrics:
            assert metric in analysis

class TestIntegration:
    """Integration tests"""
    
    def test_ahp_integration(self):
        """Test AHP integration with scheduling"""
        mcdm_engine = MCDMEngine()
        
        # Sample AHP matrix for 3 criteria (perfectly reciprocal)
        ahp_matrix = AHPMatrix(
            criteria=["expertise", "experience", "workload"],
            matrix=[
                [1.0, 2.0, 3.0],
                [0.5, 1.0, 2.0],
                [1.0/3.0, 0.5, 1.0]
            ]
        )
        
        weights, consistency_ratio, is_consistent = mcdm_engine.calculate_ahp_weights(ahp_matrix)
        
        assert len(weights) == 3
        assert abs(sum(weights) - 1.0) < 0.01
        assert consistency_ratio >= 0
    
    def test_method_comparison(self):
        """Test comparison between SAW and TOPSIS methods"""
        dss = ExamSchedulingDSS()
        
        # Sample data (minimal)
        students = [
            Student(
                id=1, name="Test Student", nim="123456",
                thesis_title="Test Thesis", thesis_field="computer science",
                supervisor_id=1, gpa=3.5, thesis_quality=4.0
            )
        ]
        
        examiners = [
            Examiner(
                id=1, name="Dr. Test", title="Professor",
                expertise=["computer science"], experience_years=10,
                workload=0, availability_score=5.0, competency_score=5.0,
                available_timeslots=[1]
            ),
            Examiner(
                id=2, name="Dr. Test2", title="Professor",
                expertise=["computer science"], experience_years=8,
                workload=1, availability_score=4.0, competency_score=4.0,
                available_timeslots=[1]
            ),
            Examiner(
                id=3, name="Dr. Test3", title="Professor",
                expertise=["computer science"], experience_years=6,
                workload=2, availability_score=3.0, competency_score=3.0,
                available_timeslots=[1]
            )
        ]
        
        rooms = [
            Room(id=1, name="Test Room", capacity=20, facilities=[], 
                 location="Test", quality_score=4.0)
        ]
        
        timeslots = [
            TimeSlot(id=1, day="Monday", start_time="08:00", 
                    end_time="10:00", session="Morning")
        ]
        
        exam_sessions = [
            ExamSession(id=1, student_id=1, duration=120, 
                       required_examiners=3, priority=1.0)
        ]
        
        # Test SAW method
        solution_saw = dss.generate_schedule(
            students, examiners, rooms, timeslots, exam_sessions, method="SAW"
        )
        
        # Test TOPSIS method
        solution_topsis = dss.generate_schedule(
            students, examiners, rooms, timeslots, exam_sessions, method="TOPSIS"
        )
        
        # Both methods should produce solutions
        assert solution_saw.method_used == "SAW"
        assert solution_topsis.method_used == "TOPSIS"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
