import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from models import Criteria, CriteriaType, AHPMatrix
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AHPMethod:
    """
    Analytic Hierarchy Process (AHP) implementation for multi-criteria decision making
    """
    
    def __init__(self):
        self.consistency_ratio_threshold = 0.1
        self.random_index = {
            1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 
            7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
        }
    
    def calculate_weights(self, pairwise_matrix: List[List[float]]) -> Tuple[List[float], float]:
        """
        Calculate criteria weights from pairwise comparison matrix
        Returns: (weights, consistency_ratio)
        """
        matrix = np.array(pairwise_matrix)
        n = matrix.shape[0]
        
        # Calculate eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        
        # Find the principal eigenvalue and corresponding eigenvector
        max_eigenvalue_index = np.argmax(eigenvalues.real)
        max_eigenvalue = eigenvalues[max_eigenvalue_index].real
        principal_eigenvector = eigenvectors[:, max_eigenvalue_index].real
        
        # Normalize the eigenvector to get weights
        weights = principal_eigenvector / np.sum(principal_eigenvector)
        weights = np.abs(weights)  # Ensure positive weights
        
        # Calculate consistency ratio
        consistency_index = (max_eigenvalue - n) / (n - 1)
        consistency_ratio = consistency_index / self.random_index.get(n, 1.49)
        
        return weights.tolist(), consistency_ratio
    
    def is_consistent(self, consistency_ratio: float) -> bool:
        """Check if the pairwise comparison matrix is consistent"""
        return consistency_ratio <= self.consistency_ratio_threshold
    
    def validate_matrix(self, matrix: List[List[float]]) -> bool:
        """Validate pairwise comparison matrix"""
        matrix = np.array(matrix)
        n = matrix.shape[0]
        
        # Check if matrix is square
        if matrix.shape[0] != matrix.shape[1]:
            return False
        
        # Check diagonal elements are 1
        if not np.allclose(np.diag(matrix), 1):
            return False
        
        # Check reciprocal property
        for i in range(n):
            for j in range(n):
                if not np.isclose(matrix[i][j] * matrix[j][i], 1, rtol=1e-5):
                    return False
        
        return True

class SAWMethod:
    """
    Simple Additive Weighting (SAW) method implementation
    """
    
    def normalize_matrix(self, decision_matrix: np.ndarray, criteria_types: List[CriteriaType]) -> np.ndarray:
        """
        Normalize decision matrix based on criteria types
        """
        normalized_matrix = np.zeros_like(decision_matrix)
        
        for j, criteria_type in enumerate(criteria_types):
            column = decision_matrix[:, j]
            
            if criteria_type == CriteriaType.BENEFIT:
                # For benefit criteria: higher is better
                max_val = np.max(column)
                normalized_matrix[:, j] = column / max_val if max_val != 0 else column
            else:
                # For cost criteria: lower is better
                min_val = np.min(column)
                normalized_matrix[:, j] = min_val / column if np.all(column != 0) else 1 - (column / np.max(column))
        
        return normalized_matrix
    
    def calculate_scores(self, decision_matrix: np.ndarray, weights: List[float], 
                        criteria_types: List[CriteriaType]) -> List[float]:
        """
        Calculate SAW scores for alternatives
        """
        # Normalize the decision matrix
        normalized_matrix = self.normalize_matrix(decision_matrix, criteria_types)
        
        # Calculate weighted scores
        weights_array = np.array(weights)
        scores = np.dot(normalized_matrix, weights_array)
        
        return scores.tolist()

class TOPSISMethod:
    """
    Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)
    """
    
    def normalize_matrix(self, decision_matrix: np.ndarray) -> np.ndarray:
        """
        Normalize decision matrix using vector normalization
        """
        # Calculate the norm for each column
        norms = np.sqrt(np.sum(decision_matrix**2, axis=0))
        
        # Avoid division by zero
        norms[norms == 0] = 1
        
        return decision_matrix / norms
    
    def calculate_scores(self, decision_matrix: np.ndarray, weights: List[float], 
                        criteria_types: List[CriteriaType]) -> List[float]:
        """
        Calculate TOPSIS scores for alternatives
        """
        # Normalize the decision matrix
        normalized_matrix = self.normalize_matrix(decision_matrix)
        
        # Apply weights
        weights_array = np.array(weights)
        weighted_matrix = normalized_matrix * weights_array
        
        # Determine ideal and negative-ideal solutions
        ideal_solution = np.zeros(len(criteria_types))
        negative_ideal_solution = np.zeros(len(criteria_types))
        
        for j, criteria_type in enumerate(criteria_types):
            if criteria_type == CriteriaType.BENEFIT:
                ideal_solution[j] = np.max(weighted_matrix[:, j])
                negative_ideal_solution[j] = np.min(weighted_matrix[:, j])
            else:
                ideal_solution[j] = np.min(weighted_matrix[:, j])
                negative_ideal_solution[j] = np.max(weighted_matrix[:, j])
        
        # Calculate distances to ideal and negative-ideal solutions
        distances_to_ideal = np.sqrt(np.sum((weighted_matrix - ideal_solution)**2, axis=1))
        distances_to_negative_ideal = np.sqrt(np.sum((weighted_matrix - negative_ideal_solution)**2, axis=1))
        
        # Calculate relative closeness to ideal solution
        scores = distances_to_negative_ideal / (distances_to_ideal + distances_to_negative_ideal)
        
        # Handle division by zero
        scores = np.nan_to_num(scores, nan=0.0)
        
        return scores.tolist()

class MCDMEngine:
    """
    Multi-Criteria Decision Making Engine that combines different methods
    """
    
    def __init__(self):
        self.ahp = AHPMethod()
        self.saw = SAWMethod()
        self.topsis = TOPSISMethod()
    
    def evaluate_alternatives(self, decision_matrix: List[List[float]], 
                            criteria: List[Criteria], 
                            method: str = "SAW") -> Tuple[List[float], Dict[str, float]]:
        """
        Evaluate alternatives using specified MCDM method
        
        Args:
            decision_matrix: Matrix of alternatives vs criteria values
            criteria: List of criteria with weights and types
            method: MCDM method to use ("SAW", "TOPSIS")
        
        Returns:
            Tuple of (scores, criteria_weights_dict)
        """
        matrix = np.array(decision_matrix)
        weights = [c.weight for c in criteria]
        criteria_types = [c.type for c in criteria]
        criteria_names = [c.name for c in criteria]
        
        # Normalize weights to sum to 1
        weights = np.array(weights)
        weights = weights / np.sum(weights)
        
        if method.upper() == "SAW":
            scores = self.saw.calculate_scores(matrix, weights.tolist(), criteria_types)
        elif method.upper() == "TOPSIS":
            scores = self.topsis.calculate_scores(matrix, weights.tolist(), criteria_types)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        criteria_weights_dict = dict(zip(criteria_names, weights.tolist()))
        
        logger.info(f"MCDM evaluation completed using {method} method")
        logger.info(f"Criteria weights: {criteria_weights_dict}")
        
        return scores, criteria_weights_dict
    
    def rank_alternatives(self, scores: List[float]) -> List[int]:
        """
        Rank alternatives based on scores (descending order)
        Returns list of indices sorted by score
        """
        return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    
    def calculate_ahp_weights(self, ahp_matrix: AHPMatrix) -> Tuple[List[float], float, bool]:
        """
        Calculate AHP weights from pairwise comparison matrix
        
        Returns:
            Tuple of (weights, consistency_ratio, is_consistent)
        """
        if not self.ahp.validate_matrix(ahp_matrix.matrix):
            raise ValueError("Invalid pairwise comparison matrix")
        
        weights, consistency_ratio = self.ahp.calculate_weights(ahp_matrix.matrix)
        is_consistent = self.ahp.is_consistent(consistency_ratio)
        
        return weights, consistency_ratio, is_consistent
