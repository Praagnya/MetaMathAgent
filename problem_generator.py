import random
from typing import Dict, Tuple, Any

class MathProblemGenerator:
    """Generates simple linear equation problems."""
    
    def __init__(self, difficulty_range: Tuple[int, int] = (1, 10)):
        self.difficulty_range = difficulty_range
    
    def generate_linear_equation(self) -> Dict[str, Any]:
        """Generate a linear equation problem of the form ax + b = c."""
        a = random.randint(*self.difficulty_range)
        b = random.randint(*self.difficulty_range)
        x = random.randint(*self.difficulty_range)
        c = a * x + b
        
        equation = f"{a}x + {b} = {c}"
        solution = x
        
        return {
            "problem_type": "linear_equation",
            "problem_text": f"Solve for x: {equation}",
            "equation": equation,
            "correct_solution": solution,
            "difficulty": a  # Using coefficient as a simple proxy for difficulty
        }